#  Realizzare un sito web che permette all'utente di visualizzare una serie di info riguardanti la societa bike store.
#  la homepage del sito deve permettere all'utente di sciegliere una fra le seguenti 4 opzioni:
#  1. il numero di prodotti per ogni categoria, sia in formato tabellare, sia in sottoforma di graffico a barre verticale
#  2. il numero di ordini per ogni store , sia in formato tabellare e in sotto forma di grafica a barre orrizzontale
#  3. il numero di prodotti per ogni brand sia in formato tabellare sia in sottoforma di grafico a torta
#  4. elenco dei prodotti che cominciano con una certa stringa di caratteri
#  una volta effettuata la scelta, l'utente clicca su un bottone che fornisce le info richieste.
#  Utilizzare bootstrap per l'interfaccia grafica

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/', methods=['GET'])
def search():
    return render_template("homepage.html")

@app.route('/scelta', methods=['GET'])
def scelta():
    servizioscelto = request.args["servizio"]

    if servizioscelto == "1servizio":
        return redirect(url_for('1servizio'))
    elif servizioscelto == "2servizio":
        return redirect(url_for('2servizio'))
    elif servizioscelto == "3servizio":
        return redirect(url_for('3servizio'))
    else :
        return redirect(url_for('4servizio'))

@app.route('/1servizio', methods=['GET'])
def servzio1():
    return render_template("1servizio.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)