# Copyright (c) 2024 Michael Macklin All Rights Reserved



from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages



def home(request):
	import requests
	import json

	global long_name
	global price
	global open_price
	global close_price
	global market_cap
	global fiftytwowkhigh
	global fiftytwowklow

	def market_cap():
		if api["price"]["marketCap"] == {}:
			return(0)
		else:
			market_cap = api["price"]["marketCap"]["raw"]
			market_cap = "{:,.0f}".format(market_cap)
			return(market_cap)



	if request.method == 'POST':
		ticker = request.POST['ticker']

		url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

		querystring = {"symbol":ticker,"region":"au"}

		headers = {
			"X-RapidAPI-Key": "6ca0d26861msh72de52afa5b260ap1996c3jsn61aa37f0a35f",
			"X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
		}


		api_request = requests.get(url, headers=headers, params=querystring)
		#api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/" + ticker + "?token=pk_48c9b1468b6a4ffebf19bd5fef7e87a2")
		#api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_48c9b1468b6a4ffebf19bd5fef7e87a2")

		try:
			api = json.loads(api_request.content)
			market_cap = market_cap()


		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api': api, 'market_cap': market_cap })


	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})


	


def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests
	import json

	

	def market_cap():
		if api["price"]["marketCap"] == {}:
			return(0)
		else:
			market_cap = api["price"]["marketCap"]["raw"]
			market_cap = "{:,.0f}".format(market_cap)
			return(market_cap)


	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added!"))
			return redirect('add_stock')
	
	else:
		ticker = Stock.objects.all()
		output = []
		

		
		for ticker_item in ticker:

			url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

			querystring = {"symbol":ticker_item,"region":"au"}

			headers = {
			"X-RapidAPI-Key": "6ca0d26861msh72de52afa5b260ap1996c3jsn61aa37f0a35f",
			"X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
			}


			api_request = requests.get(url, headers=headers, params=querystring)

			try:
				api = json.loads(api_request.content)
				api['price']['marketCap']['raw'] = market_cap()
				#market_cap = market_cap()
				output.append(api)
				


				
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted!"))
	return redirect(delete_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})
 
