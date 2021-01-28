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

def getEventTypeData():
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    return result

def eventTypesPrinter(eventData):
    for event in eventData:
        print(event['eventType']['name'] + " " + event['eventType']['id'])

def getEventTypeNumber(eventTypeName, eventData):
    for event in eventData:
        if eventTypeName.lower() in (str(event['eventType']['name']).lower()):
            return event['eventType']['id']
    return None


def marketCountSort(json_data):
    try:
        return int(json_data['marketCount'])
    except KeyError:
        return None

def getCompetitionData(eventNumber):
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listCompetitions", "params": {"filter":{ "eventTypeIds" : [ ' + str(eventNumber) + ']  }}, "id": 1}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    result.sort(key = marketCountSort,reverse = True)
    return result

def getCompetitionId(eventName, eventData):
    for event in eventData:
        if eventName.lower() in str(event['competition']['name']).lower():
            return event['competition']['id'] 
    return None

def competitionPrinter(competitionData):
    for competition in competitionData:
        print(competition['competition']['name'])



def getEventData(competitionId):
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{ "competitionIds" : [' + str(competitionId) + ']  }}, "id": 1}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    return result

def eventPrinter(eventData):
    for event in eventData:
       print(event['event']['name'])

def getEventId(eventName, eventData):
    for event in eventData:
        if(eventName.lower() in str(event['event']['name']).lower()):
            return event['event']['id']
    return None


def printOddsTypes(marketData):
    print(marketData)

def getMarketData(eventId, oddsType):
    print(oddsType)
    r = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventIds" : [' + eventId + '],"marketTypeCodes" : ["' + oddsType + '"]},"marketProjection" :["RUNNER_METADATA"], "maxResults":"1"}, "id": 1}'
    json_dat = apiCall(r,urlExchange)
    market = json_dat['result']
    return market


def getOddsData(marketId):
    r = '{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketBook","params": {"marketIds": [' + marketId + '],"priceProjection": {"priceData": ["EX_BEST_OFFERS", "EX_TRADED"],"virtualise": "true"}},"id": 1}'
    json_dat = apiCall(r,urlExchange)
    result = json_dat['result']
    return result

def printOdds(odds_data,market_data):
    for market in market_data:
        marks = market['runners']
        for mark in marks:
            print(mark['runnerName'])
            for odd in odds_data:
                runners = odd['runners']
                for runner in runners:
                    if(runner['status'] == 'ACTIVE'):
                        if(str(runner['selectionId']) ==  str(mark['selectionId'])):
                            print ('Available to back price :' + str(runner['ex']['availableToBack']))
                            print ('Available to lay price :' + str(runner['ex']['availableToLay']))
                #else:
                    #print ('This runner is not active')



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
    eventTypeData = getEventTypeData()
    competitionData = ""
    eventData = ""
    oddsTypes = ["Odds"]
    oddsDict = {"Odds" : "MATCH_ODDS"}
    while choose != 0:
        choose = int(input("Do you want watch 1) event types, 2) competitions 3) events 4) odds 0) quit\n"))
        if choose == 1:
            eventTypesPrinter(eventTypeData)
        if choose == 2:
            eventTypeName = input("Please give a event Type\n")
            # get eventNumber
            eventTypeNumber = getEventTypeNumber(eventTypeName,eventTypeData)

            # get event data
            competitionData = getCompetitionData(eventTypeNumber)
            # print competitions
            competitionPrinter(competitionData)
        if choose == 3:
            competitionName = input("Please, give a competition name\n")
            # get competition Id
            competitionId = getCompetitionId(competitionName,competitionData)
            # get events Data
            eventData = getEventData(competitionId)
            # print events
            eventPrinter(eventData)

        if choose == 4:
            eventName = input("Please, give a event name\n")
            # get Event id
            eventId = getEventId(eventName,eventData)
            print(eventId)
            print("Choose which odds to look at:")
            for a in oddsTypes:
                print(a + "\n")
            oddsType = input()
            print(oddsDict[oddsType])
            marketData = getMarketData(eventId, oddsDict[oddsType])
            marketId = getMarketID(marketData)
            odds_dat = getOddsData(marketId)
            printOdds(odds_dat, marketData)
            
start()





