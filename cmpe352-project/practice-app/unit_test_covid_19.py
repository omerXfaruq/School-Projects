import unittest
import json
import coronavirus_api

def isCoronavirusByCountryCorrect():
    response = coronavirus_api.CoronavirusByCountry("turkey")
    if not response:
        return False
    if not response['country_results'] :
        return False
    else:
        country_data = response['country_results'][0]
        if type(country_data['deaths']) == int:
            return True
        else:
            return False
        
def isWorldStatsCorrect():
    json = coronavirus_api.getWorldStatistics()
    if not json:
        return False
    if not json['world_stats'] :
        return False
    else:
        stats_dict = json['world_stats'][0]
        if type(stats_dict["total_confirmed"]) == int:
            return True
        else:
            return False

def isPlotDataFetchCorrect():
    json=coronavirus_api.plotDataFetch("turkey")
    if json==False:
        return False
    if not len(json)>0:
        return False
    if not type(json[0]["Cases"])==int:
        return False
    return True


def isCoronavirusJson():
    
    list = coronavirus_api.coronavirus_summary_search()     
    
    if list == False:
        return True
    elif 'Country' not in list[0]:
        return False
    elif 'CountryCode' not in list[0]:
        return False
    elif 'Date' not in list[0]:
        return False
    elif 'NewConfirmed' not in list[0]:
        return False
    elif 'NewDeaths' not in list[0]:
        return False
    elif 'NewRecovered' not in list[0]:
        return False
    elif 'Slug' not in list[0]:
        return False
    elif 'TotalConfirmed' not in list[0]:
        return False
    elif 'TotalDeaths' not in list[0]:
        return False
    elif 'TotalRecovered' not in list[0]:
        return False
    else:
        return True


def isJson():
    
    list = coronavirus_api.coronavirusCountryLive("France")     
    if 'Cases' not in list[0]:
        return False
    else:
        if type(list[0]["Cases"]) == int and list[0]["Status"] == 'confirmed':
            return True
        else:
            return False


class SimpleTest(unittest.TestCase):

    def test_cv_by_country(self):
        self.assertTrue(isCoronavirusByCountryCorrect() == True)
    def test_plot(self):
        self.assertTrue(isPlotDataFetchCorrect() == True)
    def test_world(self):
        self.assertTrue(isWorldStatsCorrect() == True)
    def test_cov_json(self):
        self.assertTrue(isCoronavirusJson() == True)
    def test_json(self):
        self.assertTrue(isJson() == True) 

if __name__ == '__main__':
    unittest.main()
