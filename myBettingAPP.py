import urllib
import urllib.request
import urllib.error
import requests
import json
import datetime
import sys



# url to betfair exchange
urlExchange = "https://api.betfair.com/exchange/betting/json-rpc/v1"
urlAccount = "https://api.betfair.com/exchange/account/json-rpc/v1"

# need appkey and session token to use Api
appKey = input("Enter your Application key ")
sessionToken = input("Enter your session Token/SSOID :")

# Request Header, must contain X-Application, X-Authentication and content type
headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}

# Makes API_NG call
# returs encoded Json data
def apiCall(request,url):
    # request to get listEventTypes from API-NG
    response = requests.post(url, data=request, headers=headers)
    # json form
    a = json.loads(response.text)
    return a

def eventPrinter():
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    for event in result:
        name = event['eventType']['name']
        print(name)

def accountFunds():
    r = '{"jsonrpc": "2.0", "method": "AccountAPING/v1.0/getAccountFunds"}'
    json_dat = apiCall(r,urlAccount)
    result = json_dat['result']
    print(result['availableToBetBalance'])

eventPrinter()






