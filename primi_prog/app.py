from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET'])
def search():
    return render_template("search.html")

@app.route('/result', methods=['GET'])
def result():
  # collegamento al DB
  import pandas as pd
  import pymssql
  #connessione con il database
  password = "xxx123##"
  connection = pymssql.connect(server="213.140.22.237\SQLEXPRESS", user="basco.luke",password=password,database="basco.luke")

  # invio query al DB e ricezione informazioni
  nomedelprodotto = request.args['nomeprodotto']
  # si mette f(format) all'inizio per avere la possibiltà di mettere una variabile in una stringa {nomedelprodotto}
  query = f"select * from production.products where production.products.product_name like'{nomedelprodotto}%'"
  dfprodotti = pd.read_sql(query,connection)

  # visualizzare le informazione 
  return render_template("result.html", nomicolonne = dfprodotti.columns.values, dati = list(dfprodotti.values.tolist()))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)