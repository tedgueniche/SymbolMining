from flask import Flask, render_template, request, redirect
import Quandl

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/stock/<ticker>/<date>', methods=["GET"])
def getStock(ticker,date):
	dataToday = Quandl.get("WIKI/AAPL", returns="numpy",  trim_start=date, trim_end=date)[0]
	close = dataToday['Close']

	return render_template('stock.json', date=date, close=close, ticker=ticker)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
