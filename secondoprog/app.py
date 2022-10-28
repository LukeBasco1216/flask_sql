#  Realizzare un sito web che permette all'utente di visualizzare una serie di info riguardanti la societa bike store.
#  la homepage del sito deve permettere all'utente di sciegliere una fra le seguenti 4 opzioni:
#  1. il numero di prodotti per ogni categoria, sia in formato tabellare, sia in sottoforma di graffico a barre verticale
#  2. il numero di ordini per ogni store , sia in formato tabellare e in sotto forma di grafica a barre orrizzontale
#  3. il numero di prodotti per ogni brand sia in formato tabellare sia in sottoforma di grafico a torta
#  4. elenco dei prodotti che cominciano con una certa stringa di caratteri
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
    servizioscelto = request.args["servizio"]

    if servizioscelto == "1servizio":
        return redirect(url_for('servizio1'))
    elif servizioscelto == "2servizio":
        return redirect(url_for('servizio2'))
    elif servizioscelto == "3servizio":
        return redirect(url_for('servizio3'))
    else :
        return redirect(url_for('servizio4'))

@app.route('/servizio1', methods=['GET'])
def servizio1():
    global df1
    query = "select production.categories.category_name, count(*) as tot_prod from production.products inner join production.categories on production.products.category_id = production.categories.category_id group by production.categories.category_name,production.categories.category_id"
    df1 = pd.read_sql(query,connection)
    return render_template("1servizio.html", nomicolonne = df1.columns.values, dati = list(df1.values.tolist()))

@app.route('/grafico1', methods=['GET'])
def grafico1():
    #  crea la figura
    fig = plt.figure(figsize=(11,8))
    #grandezza del grafico
    fig.set_size_inches(14,9)
    #  crea gli assi
    ax = plt.axes()

    x = df1['category_name']
    y = df1['tot_prod']
    #  crea le barre
    #  color = "chocolate" per cambiare il colore delle barre
    #  dentro le virgolette mettere nome di un colore dalla tabella di cssdegli colori
    ax.bar(x, y, color="chocolate")
    #  ruota i label o i nomi dell'asse x
    fig.autofmt_xdate(rotation=60) 
    #  crea un titolo nell'asse x
    ax.set_xlabel("categoria")
    #  crea un titolo nell'asse y
    ax.set_ylabel("numero prodotti")
    #  crea un titolo
    fig.suptitle("quantita prodotti")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/servizio2', methods=['GET'])
def servizio2():
    global df2
    # query si scrive in formato string
    query = "select sales.stores.store_name, count(*) as num_ordini from sales.stores inner join sales.orders on sales.stores.store_id = sales.orders.store_id group by sales.stores.store_name"
    df2 = pd.read_sql(query,connection)
    return render_template("2servizio.html", nomicolonne = df2.columns.values, dati = list(df2.values.tolist()))

@app.route('/grafico2', methods=['GET'])
def grafico2():
    #  crea la figura
    fig = plt.figure(figsize=(11,8))
    #grandezza del grafico
    fig.set_size_inches(14,9)
    #  crea gli assi
    ax = plt.axes()
    #  crea le barre
    #  color = "chocolate" per cambiare il colore delle barre
    #  dentro le virgolette mettere nome di un colore dalla tabella di cssdegli colori
    ax.barh(df2["store_name"], df2["num_ordini"], color="chocolate")
    #  ruota i label o i nomi dell'asse x
    fig.autofmt_xdate(rotation=60) 
    #  crea un titolo nell'asse x
    ax.set_xlabel("numero orders")
    #  crea un titolo nell'asse y
    ax.set_ylabel("store")
    #  crea un titolo
    fig.suptitle("numero ordini")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/servizio3', methods=['GET'])
def servizio3():
    global df3
    # query si scrive in formato string
    query = "select production.brands.brand_name, count(*) as num_prod from production.brands inner join production.products on production.products.brand_id = production.brands.brand_id group by production.brands.brand_name"
    df3 = pd.read_sql(query,connection)
    return render_template("3servizio.html", nomicolonne = df3.columns.values, dati = list(df3.values.tolist()))

@app.route('/grafico3', methods=['GET'])
def grafico3():
    plt.rcParams.update({"font.size" : 12})

    fig = plt.figure(figsize=(12,12))
    ax = plt.axes()

    #  autopct = "%1.1f%%"  ----->    nelle virgolette il primo 1 è la lontananza dei percentuali
    #  startangle = 90   ------>    per ruotare il grafico
    #  colors = ["yellow", "red","purple"]    ------->   per colorare il grafico e si alternano
    #  si scrive con l'= perche possiamo scrivere le funzioni senza ordine
    ax.pie(df3["num_prod"],labels = df3.brand_name, autopct = "%0.2f%%",startangle = 90, colors = ["lavender", "lightblue","lightgreen"])

    fig.suptitle("quantita prodotti")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/servizio4', methods=['GET'])
def servizio4():
    return render_template("input4servizio.html")

@app.route('/var-input', methods=['GET'])
def inputresponse():
    global df4
    variabile = request.args["inputt"]
    query= f"select * from production.products where product_name like '{variabile}%'" # si mette f(format) all'inizio per avere la possibiltà di mettere una variabile in una stringa {nomedelprodotto}
    df4 = pd.read_sql(query, connection)
    return render_template("4servizio.html", nomicolonne = df4.columns.values, dati = list(df4.values.tolist()))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)