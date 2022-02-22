from flask import Flask
import requests
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def coronavirus_summary_search():
    r = requests.get('https://api.covid19api.com/summary')
    
    if 'json' in r.headers.get('Content-Type'):
        j = json.loads(r.text)
    
        countryList = j["Countries"]
        CountryCount = 186	

        for i in range(CountryCount):	
            x = countryList[i]
            countryCode = x["CountryCode"] 
            url = "https://www.countryflags.io/" + countryCode + "/shiny/64.png"        
            x["CountryCode"] = url

        return countryList

    else:
        return False


def coronavirusCountryLive(country):
#http://127.0.0.1:5000/countryLive?country=Turkey&typeName=confirmed

   
        
        url = "https://api.covid19api.com/country/{}/status/{}/live".format(country, "confirmed")

        payload = {}
        headers= {}

        response = requests.request("GET", url, headers=headers, data = payload)

        result = response.json()
        
        return result[len(result)-5:len(result)]


def getWorldStatistics():
    
    req_url = "https://api.covid19api.com/world/total"
    r = requests.get(req_url)
    j = json.loads(r.text)
    world_stats= []

    world_stats.append(
            { 'total_confirmed': j["TotalConfirmed"],
              'total_deaths':j["TotalDeaths"],
              'total_recovered': j["TotalRecovered"]
            }
        )

    json_return = {"world_stats":world_stats}
    return json_return

def CoronavirusByCountry(country):
    req_url = 'https://api.covid19api.com/country/' + country
    r = requests.get(req_url)
    if r.status_code != 200:
        json_return = {
            "country_results" : []
        }
        return json_return

    j = json.loads(r.text)

    # TODO: Check if request resulted in a success.
    
    country_data = []

    for index, day_info in enumerate(j):
        country_data.append({
            'date': day_info['Date'],
            'province': day_info['Province'],
            'confirmed': day_info['Confirmed'],
            'deaths': day_info['Deaths'],
            'recovered': day_info['Recovered'],
            'active': day_info['Active']
        })

    json_return = {
        "country_results": country_data
    }

    return json_return

def plotDataFetch(countryName):
    link="https://api.covid19api.com/total/country/"+countryName+"/status/confirmed"
    r=requests.get(link)
    if not 'json' in r.headers.get('Content-Type'):
        return False
    return json.loads(r.text)

#Returns plot from total case request
def create_figure(countryName):
    j=plotDataFetch(countryName)
    if j==False:
        return False
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    
    dayNo=len(j)
    dayByDayTotalNo=[0]*dayNo    
    for i in range(len(j)):
        dayByDayTotalNo[i]=j[i]["Cases"]    
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(dayByDayTotalNo)
    return fig
