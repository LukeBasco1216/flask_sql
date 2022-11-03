#  Realizzare un sito web che permette all'utente di visualizzare una serie di info riguardanti la societa bike store.
#  la homepage del sito deve permettere all'utente di sciegliere una fra le seguenti 4 opzioni:
#  1. nomi dei clienti che hanno una mail di gmail, tabella
#  2. ordini non ancora spediti, tabella
#  3. prodotti acquistati da martin spencer, tabella
#  4. prodotti aquistati dalla persona inserita dall'utente, tabella
#  5. nome dello store con piu dipendenti, tabella e grafica a torta
#  una volta effettuata la scelta, l'utente clicca su un bottone che fornisce le info richieste.
#  Utilizzare bootstrap per l'interfaccia grafica

from flask import Flask, render_template, request, redirect, url_for, Response, redirect
app = Flask(__name__)

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import pymssql


connection = pymssql.connect(server="213.140.22.237\SQLEXPRESS", user="basco.luke",password="xxx123##",database="basco.luke")

@app.route('/', methods=['GET'])
def search():
  return render_template("homepage.html")

@app.route('/scelta', methods=['GET'])
def scelta():
    servizio = request.args["servizio"]
    if servizio == "servizio1":
        return redirect(url_for("servizio1"))
    if servizio == "servizio2":
        return redirect(url_for("servizio2"))
    if servizio == "servizio3":
        return redirect(url_for("servizio3"))
    if servizio == "servizio4":
        return redirect(url_for("inputval"))
    else:
        return redirect(url_for("servizio5"))


#  1. nomi dei clienti che hanno una mail di gmail, tabella
@app.route('/servizio1', methods=['GET'])
def servizio1():
    query= "select first_name, email from sales.customers where email like '%@gmail.%'"
    df1 = pd.read_sql(query,connection)
    return render_template("serviziosansgrafico.html", nomicolonne = df1.columns.values, dati = list(df1.values.tolist()))


#  2. ordini non ancora spediti, tabella
@app.route('/servizio2', methods=['GET'])
def servizio2():
    query= "select * from sales.orders where shipped_date is null"
    df2 = pd.read_sql(query,connection)
    return render_template("serviziosansgrafico.html", nomicolonne = df2.columns.values, dati = list(df2.values.tolist()))



#  3. prodotti acquistati da martin spencer, tabella
@app.route('/servizio3', methods=['GET'])
def servizio3():
    query= "select production.products.* from sales.customers inner join sales.orders on sales.customers.customer_id = sales.orders.customer_id inner join sales.order_items on sales.orders.order_id = sales.order_items.order_id inner join production.products on sales.order_items.product_id = production.products.product_id where first_name = 'Johnathan' and last_name = 'Velazquez'"
    df3 = pd.read_sql(query,connection)
    return render_template("serviziosansgrafico.html", nomicolonne = df3.columns.values, dati = list(df3.values.tolist()))


#  4. prodotti aquistati dalla persona inserita dall'utente, tabella
@app.route('/inputval', methods=['GET'])
def inputval():
    return render_template("valperserv4.html")

@app.route('/servizio4', methods=['GET'])
def servizio4():
    nome = request.args["nome"]
    cognome = request.args["cognome"]
    query = f"select production.products.* from sales.customers inner join sales.orders on sales.customers.customer_id = sales.orders.customer_id inner join sales.order_items on sales.orders.order_id = sales.order_items.order_id inner join production.products on sales.order_items.product_id = production.products.product_id where first_name = '{nome}' and last_name = '{cognome}'"
    df4 = pd.read_sql(query, connection)
    return render_template("serviziosansgrafico.html", nomicolonne = df4.columns.values, dati = list(df4.values.tolist()))



#  5. nome dello store con piu dipendenti, tabella e grafica a torta
@app.route('/servizio5', methods=['GET'])
def servizio5():
    global df5
    query= "select store_name, count(first_name) as totdip from sales.stores inner join sales.staffs on sales.stores.store_id = sales.staffs.store_id group by store_name having count(first_name) = (select max(totdip) from (select store_name, count(first_name) as totdip from sales.stores inner join sales.staffs on sales.stores.store_id = sales.staffs.store_id group by store_name) as tot)"
    df5 = pd.read_sql(query,connection)
    return render_template("serviziocongraficobarrenormale.html", nomicolonne = df5.columns.values, dati = list(df5.values.tolist()))


@app.route('/graficoserv5', methods=['GET'])
def graficoserv5():
    plt.rcParams.update({"font.size" : 12})

    fig = plt.figure(figsize=(12,12))
    ax = plt.axes()

    
    #  autopct = "%1.1f%%"  ----->    nelle virgolette il primo 1 è la lontananza dei percentuali
    #  startangle = 90   ------>    per ruotare il grafico
    #  colors = ["yellow", "red","purple"]    ------->   per colorare il grafico e si alternano
    #  si scrive con l'= perche possiamo scrivere le funzioni senza ordine
    ax.pie(df5.totdip,labels = df5.store_name, autopct="%1.2f%%",startangle = 90, colors = ["lavender", "lightblue","lightgreen"])

    fig.suptitle("numero di dipendenti per ogni store")
      
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/graficoserv5_2', methods=['GET'])
def graficoserv5_2():
    plt.rcParams.update({"font.size" : 12})

    fig = plt.figure(figsize=(12,12))
    ax = plt.axes()



    ###   per far vedere il suo valore assoluto
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d}'.format(p=pct,v=val)
        return my_autopct

    values = list(df5["totdip"])

    #  autopct = "%1.1f%%"  ----->    nelle virgolette il primo 1 è la lontananza dei percentuali
    #  startangle = 90   ------>    per ruotare il grafico
    #  colors = ["yellow", "red","purple"]    ------->   per colorare il grafico e si alternano
    #  si scrive con l'= perche possiamo scrivere le funzioni senza ordine
    ax.pie(df5.totdip,labels = df5.store_name, autopct=make_autopct(values),startangle = 90, colors = ["lavender", "lightblue","lightgreen"])

    fig.suptitle("numero di dipendenti per ogni store")
      
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)