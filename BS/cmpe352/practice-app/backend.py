
from flask import Flask, render_template, jsonify, request

import requests
import json
import scholar_util
import coronavirus_api
import bitcoin_api

#For plot	

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas	
from matplotlib.figure import Figure	
import io	
from flask import Response	
import numpy as np	



app = Flask(__name__)
#Template for flask backend

@app.route('/')
def form_post():
    return render_template('home.html')

@app.route('/api-list')
def api_list():
    return render_template('api_list.html')


@app.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':

        json = scholar_util.getAuthors(request.form["search_param"])
        context = {
            "results": json["author_search_result"],
            "param":   request.form["search_param"],
        }

    else:
        context = {}

    return render_template('search.html', context=context)


@app.route('/api/search', methods=['POST'])
def api_search():

    req_data = request.get_json()
    name = req_data['name']
    json  = scholar_util.getAuthors(name)
    return jsonify(json)


@app.route('/api/authorpublications', methods=['GET'])
def api_authorpublications():
    name = request.args.get("name")
    _range = request.args.get("range")
    json = scholar_util.getAuthorsPublications(name, _range)
    return jsonify(json)


@app.route('/api/publicationsearch', methods=['GET'])
def api_publicationsearch():

    name = request.args.get("name")
    json = scholar_util.searchPublication(name)
    return jsonify(json)


@app.route('/api/authorstats', methods=['GET'])
def api_authorstats():

    name = request.args.get("name")
    json = scholar_util.getAuthorCitationStats(name)
    return jsonify(json)


@app.route('/profile/<name>', methods=['GET'])
def profile(name):
    url = request.url_root+'api/profiledata?name=' + name
    results = requests.get(url)
    results = json.loads(results.text)

    context = results

    return render_template("profile.html", context=context)


@app.route('/api/profiledata', methods=['GET'])
def api_profile_data():

    name = request.args.get("name")
    json = scholar_util.getUserProfileData(name)
    return jsonify(json)


@app.route('/api/bitcoinprice', methods=['GET'])
def api_bitcoin_price():

    json = bitcoin_api.getBitcoinPrice()
    return jsonify(json)

@app.route('/bitcoinprice', methods=['GET'])
def bitcoin_price():

    context = bitcoin_api.getBitcoinPrice()

    return render_template('bitcoin.html', context=context)


@app.route('/api/coinranks', methods=['GET'])
def api_coin_ranks():

    json = bitcoin_api.getCoinRanks()
    return jsonify(json)

@app.route('/coinranks', methods=['GET'])
def coin_ranks():

    context = bitcoin_api.getCoinRanks()

    return render_template('rankcoin.html', context=context)


@app.route('/coronavirus', methods=['GET'])
def coronavirus():

    countryData = coronavirus_api.coronavirus_summary_search()
    if countryData == False:
        return "Server is overloaded, please wait for a couple of seconds and try again!"
    else:
        return render_template('coronavirus.html', context=countryData)


@app.route('/api/coronavirus', methods=['GET'])
def api_coronavirus():

    countryData = coronavirus_api.coronavirus_summary_search()
    return jsonify(countryData)

@app.route('/coronavirusCountryLive', methods=['POST', 'GET'])
def coronavirusCountryLive():

   if request.method == 'POST':
        results = coronavirus_api.coronavirusCountryLive(request.form["search_param"])
        print(results)
        context = {
            "results": results,
            "param":   request.form["search_param"],
        }
        #print(context)
   else:
        context = {}

   return render_template('searchCountryName.html', context=context)


@app.route('/api/coronavirusCountryLive',  methods=['POST', 'GET'])
def api_coronavirusCountryLive():

        context = {}
        req_data = request.get_json()
        country = req_data['country']
        results=coronavirus_api.coronavirusCountryLive(country)
        context = {
            "results": results,
            "param":   country,
        }


        return context


@app.route('/api/worldStats', methods=['GET'] )
def api_world_stats():
    world_data = coronavirus_api.getWorldStatistics()
    return world_data

@app.route('/worldStats', methods=['GET'])
def world_stats():
    world_data = coronavirus_api.getWorldStatistics()
    return render_template('worldstats.html', context = world_data)

@app.route('/coronavirusByCountry', methods=['POST', 'GET'])
def coronavirusByCountry():
    if request.method == 'POST':
        country_data = coronavirus_api.CoronavirusByCountry(request.form["search_param"])
        context = {
            "results": country_data["country_results"],
            "param": request.form["search_param"]
        }
    else:
        context = {}

    return render_template('coronavirusByCountry.html', context=context)

#
# MIGHT BE WRONG. WILL BE FIXED IF SO.
#
@app.route('/api/coronavirusByCountry', methods=['POST'])
def api_coronavirusByCountry():
    if request.method == 'POST':
        req_data = request.get_json()
        country = req_data['country']
        country_data = coronavirus_api.CoronavirusByCountry(country)
        context = {
            "results": country_data["country_results"],
            "param": country
        }
    else:
        context = {}

    return context


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Unfortunately this endpoint was not integrated into frontend.However you can call it like this:
# http://localhost/plotCountry?country=sweden
# http://localhost/plotCountry?country=turkey
# http://localhost/plotCountry?country=iran
# http://localhost/plotCountry?country=russia
# http://localhost/plotCountry?country=us
#Plots a plot of total cases, needs to parametrized by country name
@app.route('/plotCountry', methods=['GET','POST'])
def plot_png():   
    country = request.args.get('country')
    fig = coronavirus_api.create_figure(country)
    if fig==False:
        return "Error 404: No country as such, or service is busy"
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

#API version support for plotData receive
@app.route('/api/plot.png', methods=['POST'])
def api_plot_png():
   
    req_data = request.get_json()
    name = req_data['name']
    json  = coronavirus_api.plotDataFetch(name)
    if json==False:
        return "Error 404: No country as such, or service is busy"
    return jsonify(json)

if __name__ == '__main__':

    app.run(host="0.0.0.0",port = 80)
