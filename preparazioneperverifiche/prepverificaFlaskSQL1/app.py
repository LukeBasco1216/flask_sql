#  Realizzare un sito web che permette all'utente di visualizzare una serie di info riguardanti la societa bike store.
#  la homepage del sito deve permettere all'utente di sciegliere una fra le seguenti 4 opzioni:
#  1. i nomi dei prodotti con il brand, in formato tabellare
#  2. i nomi dei prodotti che hanno uno stock superiore a 10 , sia in formato tabellare e in sotto forma di grafica a barre verticale
#  3. i nomi dei prodotti che hanno la parola cruiser nel nome , in formato tabellare 
#  4. i nomi dei prodotti che hanno la parola inserita dall'utente nel nome in formato tabellare 
#  5. i nomi dei brand contando il numero di prodotti che ha, sia in formato tabellare e in sotto forma di grafica a barre verticale
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
  servscelto = request.args["servizio"]
  if servscelto == '1servizio':
    return redirect(url_for('servizio1'))
  elif servscelto == '2servizio':
    return redirect(url_for('servizio2'))
  elif servscelto == '3servizio':
    return redirect(url_for('servizio3'))
  elif servscelto == '4servizio':
    return redirect(url_for('servizio4'))
  else:
    return redirect(url_for('servizio5'))



#  1. i nomi dei prodotti con il brand, in formato tabellare
@app.route('/servizio1', methods=['GET'])
def servizio1():
  global df1
  query ='select production.products.product_name, production.brands.brand_name from production.products inner join production.brands on production.products.brand_id = production.brands.brand_id'
  df1 = pd.read_sql(query,connection)
  return render_template("servizio1.html", nomicolonne = df1.columns.values, dati = list(df1.values.tolist()))


#  2. i nomi dei prodotti che hanno uno stock superiore a 10 , sia in formato tabellare e in sotto forma di grafica a barre verticale
@app.route('/servizio2', methods=['GET'])
def servizio2():
  global df2
  query ="select production.products.product_name, production.stocks.quantity from production.products inner join production.stocks on production.products.product_id = production.stocks.product_id where quantity >= 10"
  df2 = pd.read_sql(query, connection)
  return render_template("servizio2.html", nomicolonne = df2.columns.values, dati = list(df2.values.tolist()))


@app.route('/grafico1', methods=['GET'])
def grafico1():
      #  crea la figura
    fig = plt.figure(figsize=(20,20))
    #grandezza del grafico
    fig.set_size_inches(14,9)
    #  crea gli assi
    ax = plt.axes()
    #  crea le barre
    #  color = "chocolate" per cambiare il colore delle barre
    #  dentro le virgolette mettere nome di un colore dalla tabella di cssdegli colori
    ax.bar(df2['product_name'], df2['quantity'], color="chocolate")
    #  ruota i label o i nomi dell'asse x
    fig.autofmt_xdate(rotation=60) 
    #  crea un titolo nell'asse x
    ax.set_xlabel("product_name")
    #  crea un titolo nell'asse y
    ax.set_ylabel("quantity")
    #  crea un titolo
    fig.suptitle("quantita prodotti che hanno uno stock maggiore di 10")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


#  3. i nomi dei prodotti che hanno la parola cruiser nel nome 
@app.route('/servizio3', methods=['GET'])
def servizio3():
  query = "select production.products.product_name from production.products where product_name like '%cruiser%'"
  df3 = pd.read_sql(query, connection)
  return render_template("servizio3.html", nomicolonne = df3.columns.values, dati = list(df3.values.tolist())) 


#  4. i nomi dei prodotti che hanno la parola inserita dall'utente nel nome
@app.route('/servizio4', methods=['GET'])
def servizio4():
  return render_template("input.html")

@app.route('/input', methods=['GET'])
def inputt():
  valoreins = request.args["input"]
  query = f"select production.products.product_name from production.products where production.products.product_name like '%{valoreins}%'"
  df4 = pd.read_sql(query, connection)
  return render_template("servizio4.html", nomicolonne = df4.columns.values, dati = list(df4.values.tolist()))



#  5. nomi dei brand contando il numero di prodotti che ha
@app.route('/servizio5', methods=['GET'])
def servizio5():
  query = "select production.brands.brand_name, count(*) as totprod from production.products inner join production.brands on production.products.brand_id = production.brands.brand_id group by production.brands.brand_name"
  df5 = pd.read_sql(query, connection)
  return render_template("servizio5.html", nomicolonne = df5.columns.values, dati = list(df5.values.tolist()))



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)