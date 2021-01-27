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

def eventTypesPrinter():
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    for event in result:
        print(event['eventType']['name'] + " " + event['eventType']['id'])

def competitionPrinter(eventNumber):
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listCompetitions", "params": {"filter":{ "eventTypeIds" : [ ' + eventNumber + ']  }}, "id": 1}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    result.sort(key = marketCountSort,reverse = True)
    for comp in result:
        print(comp['competition']['name'] + " " + comp['competition']['id'])

def marketCountSort(json_data):
    try:
        return int(json_data['marketCount'])
    except KeyError:
        return 0

def eventPrinter(compId):
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{ "competitionIds" : [' + compId + ']  }}, "id": 1}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    for event in result:
       print(event['event']['name'] + " " + event['event']['id'])

def getMarketData(eventId):
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventIds" : [' + eventId + '],"marketTypeCodes" : ["MATCH_ODDS"]},"marketProjection" :["RUNNER_METADATA"], "maxResults":"1"}, "id": 1}'
    json_dat = apiCall(r,urlExchange)
    market = json_dat['result']
    return market

def getMarketID(marketResults):
    for market in marketResults:
        return market['marketId']

def getRunnerIDs(marketResults):
    IDs = []
    ind = 0
    for market in marketResults:
        IDs.append(market['runners'][0]['selectionId'])
    for market in marketResults:
        IDs.append(market['runners'][1]['selectionId'])
    for market in marketResults:
        IDs.append(market['runners'][2]['selectionId'])
    return IDs


def accountFunds():
    r = '{"jsonrpc": "2.0", "method": "AccountAPING/v1.0/getAccountFunds"}'
    json_dat = apiCall(r,urlAccount)
    result = json_dat['result']
    print(result['availableToBetBalance'])


def start():
    choose = 1
    eventNumber = 1
    while choose != 0:
        choose = int(input("Do you want watch 1) event types, 2) competitions 3) events 4) odds 0) quit\n"))
        if choose == 1:
            eventTypesPrinter()
        if choose == 2:
            eventNumber = input("Please give a eventNumber\n")
            competitionPrinter(eventNumber)
        if choose == 3:
            competitionNumber = input("Please give a competition number\n")
            eventPrinter(competitionNumber)
        if choose == 4:
            eventId = input("Please give a eventId \n")
            

market_data = getMarketData("30244620")
getMarketID(market_data)



