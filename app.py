from flask import Flask, render_template, request, redirect, Markup
from datetime import date
from bokeh.charts import TimeSeries
from bokeh.embed import components
import Quandl
import sys
import pandas as pd

app = Flask(__name__)
k = "hef543vCbGaBpRT3Hg4bW1T-zyhtipu54"[::-1][7:-6]

@app.route('/')
def main():
	return render_template('index.html')


@app.route('/stock/<ticker>/<date>', methods=["GET"])
def getStock(ticker,date):
	dataToday = Quandl.get("WIKI/"+ ticker, trim_start=date, trim_end=date, authtoken=k)[0]
	close = dataToday['Close']

	return render_template('stock.json', date=date, close=close, ticker=ticker)


@app.route('/stock/<ticker>/graph', methods=["GET"])
def getGraph(ticker):

	today = date.today()
	lastYear = date(today.year - 1, today.month, today.day)

	#gets the data
	dataFrame = Quandl.get("WIKI/"+ ticker +".4",  trim_start=lastYear, trim_end=today, authtoken=k)

	#creates the timeseries chart
	chart = TimeSeries(dataFrame['Close'], title=ticker, ylabel="Closing Price ($)")

	#generates the script and div HTML element
	script, div = components(chart)

	return render_template("stock_graph.html", script=Markup(script), div=Markup(div))


if __name__ == '__main__':
	app.debug = True

	#production vs development environment
	if (len(sys.argv) > 1):
		app.run(port=33507, debug=True)
	else:
		app.run(host='0.0.0.0')