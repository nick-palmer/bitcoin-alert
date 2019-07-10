#!/usr/bin/python
#
# This is a simple python script that periodically gets bitcon price data
# and if the price has risen or dropped beyond the percentage threshold,
# then a sound clip is played.


import schedule
import requests
import json
import time
import os

checkIntervalMinute = 1
bitcoinPriceUrl = 'https://api.coindesk.com/v1/bpi/currentprice.json'
priceChangeThreshold = 0.01
lastPrice = 0.0

def check_price():
	resp = requests.get(bitcoinPriceUrl)
	data = resp.json()
	global lastPrice
	
	# TODO handle exception if the response is bad
	
	newPrice = data['bpi']['USD']['rate_float']
	
	if lastPrice == 0.0:
		lastPrice = newPrice
		
	percentChange = abs( ( lastPrice - newPrice ) / lastPrice * 100 )
	
	print('Current price: ', newPrice)
	print('Last price: ', lastPrice)
	print('------------------------------')
	print('Percent change: ', percentChange)
	
	if percentChange > priceChangeThreshold:
		print('Price change threshold exceeded, PANIC!')
		os.system('mpg123 nd-ys.mp3')
		#os.system("start nd-ys.mp3")
		#os.system("powershell -c (New-Object Media.SoundPlayer 'nd-ys.mp3').PlaySync();")
	else:
		print('Nothing to see here...')
		
	lastPrice = newPrice
	
# Schedule the price check job
schedule.every(checkIntervalMinute).seconds.do(check_price)
	
# Run the job
while True:
	schedule.run_pending()
	time.sleep(10)