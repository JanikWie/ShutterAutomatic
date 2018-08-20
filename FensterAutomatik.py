import urllib.request as request
import urllib.parse as parsen
from urllib.parse import quote
import bs4 as bs
import re
import datetime as dt
import re
def getResponseData(url):

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"    #deceve blocker
    source = request.urlopen(url).read()
    soup = bs.BeautifulSoup(source,'lxml')
    return soup

def Parser(soup, tryal, tosearch):  
    toTry = str(tryal)
    if tosearch == 'temp':          
        #allDivs = soup.find_all('li', 'data-num="1"', class_="vhs")
        allDivs = soup.find_all('div', class_="vhs-text--large portable-hide")

    elif tosearch == 'time':
         allDivs = soup.find_all('div',class_="[ delta ] [ portable-hide ] nowrap text--blue-dark")
    return allDivs

def getDoStuffTime(soup,TypeToFind):
    
    amountTries = 0                   # reset amount tries
    WhereToLook = 0               #reset where to look
    allTemps = Parser(soup,amountTries,'temp')    #starts Parser
    while amountTries <= 23:
        TempContent = allTemps[amountTries].contents
        TempStr = str(TempContent[0])
        Temp = TempStr[0:2]
        if TypeToFind == "shutDown" :
             if int(Temp) > 23:
                WhereToLook = amountTries
                amountTries = 90
        if TypeToFind == "shutUp":
            if int(Temp) <= 23:
                WhereToLook = amountTries
                amountTries = 90
                pass
            pass       
       
        amountTries+=1
    allTimes = Parser(soup, WhereToLook,'time')
    TimeContent = allTimes[WhereToLook].contents
    TimeStr = str(TimeContent[0])
    timeToShut = TimeStr[25:27]
    return timeToShut

def foundsite(soup):
    pass





#Url =
#'https://www.wetter.com/deutschland/schemmerhofen/schemmerberg/DE0009432010.html'
UrlBegin = 'https://www.wetter.com/suche/?q='
#Values = {'s':'basics', 'submit':'search'}
succesfullyFoundSite = False

while succesfullyFoundSite != True:  
    Place = input('Enter your Place: ')         #gets the place to look at
    Url = UrlBegin + quote(Place)               #makes a working url because url req doesn't like non ascii char
    soup = getResponseData(Url)                 # gets da soup
    if Parser(soup,0,'temp'):                   # checks if the url is actually working by looking if there
                                                # is stuff coming back,
                                                #that it can work with
        succesfullyFoundSite = True
    else:    
        print('no such Place found')            #if not than try again :)
    
while True:

    now = dt.datetime.now()         # saves date and time
    Day = now.day                   # gets the day and saves it
   
    timeToShut = getDoStuffTime(soup,"shutDown")    #gets the time to shut the blast shields
    timeToOpen = getDoStuffTime(soup,"shutUp")      #gets the time to open them again
    
    once = True                                     # so that the time, time to shut and time to open are only printet once
    shut = False                                    # we have to initialize with something
    manualShutdown = False                          # if i want them down they should stay down
    while Day == now.day :                          # this is just to make sure it gets updatet every day by looking at the date that the data
                                                    # was scraped and making sure that this was today
        
        if once:        
            print(now)                             # prints some interresting stuff
            print('time to shut: ' ,timeToShut)
            print('time to open: ', timeToOpen)
            once = False
        now = dt.datetime.now()
        
        if now.hour == int(timeToShut) and shut != True:        # checks if its time to shut the blastshields
            print('Shutdown')
            shut = True
        if now.hour == int(timeToOpen) and shut != False and manualshutdown != True:        # can we open them now?
            print('ShutUp')
            shut = False
                
        time.sleep(300)                                     #we dont have to check every milisec, do we?
