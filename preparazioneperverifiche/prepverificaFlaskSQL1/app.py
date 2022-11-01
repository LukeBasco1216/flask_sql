#  Realizzare un sito web che permette all'utente di visualizzare una serie di info riguardanti la societa bike store.
#  la homepage del sito deve permettere all'utente di sciegliere una fra le seguenti 4 opzioni:
#  1. i nomi dei prodotti con il brand, sia in formato tabellare, sia in sottoforma di graffico a barre verticale
#  2. i nomi dei prodotti che hanno uno stock superiore a 10 , sia in formato tabellare e in sotto forma di grafica a barre orrizzontale
#  3. i nomi dei prodotti che hanno la parola cruiser nel nome , sia in formato tabellare 
#  4. i nomi dei prodotti che hanno la parola inserita dall'utente nel nome in formato tabellare 
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



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)