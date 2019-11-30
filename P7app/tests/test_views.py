import pytest
import requests
from P7app import app
from P7app.parser.parser_class import Parser_search
from P7app.api.api_classes import GoogleMapsApi, WikiApi, WikiGlobal
from P7app.api import api_classes

def test_url():
    client = app.test_client()
    result = client.get("/")
    assert result.status_code == 200

def test_recherche():
    client = app.test_client()
    result = client.get("/")
    html = result.data
    #b is used to convert result in byte type
    assert b"GrandPy Bot" in html
    assert b"<input" in html

    
def test_off_punctuation():
    sample = Parser_search("Bonjour, parle-moi de Paris!")
    sample.off_punctuation()
    assert sample.off_punctuation() == "bonjour  parle moi de paris "

def test_parser_search():
    sample = Parser_search("Parle moi de Meaux")
    sample.filter_parser()
    assert sample.filter_parser() == "meaux"

def request_test(monkeypatch):
    search = "Paris"
    results = ["Paris, France", 48.856614, 2.3522219, "OK"]
    def json():
        return {
            "formatted_adress": "Paris, France",
            "location": {"lat": 48.856614, "lng": 2.3522219},
            "status": "OK"
            }

    def mock_json(*args, **kwargs):
        return json()

    monkeypatch.setattr(GoogleMapsApi, "json", mock_json_)
    
    sample = GoogleMapsApi(search)
    assert sample.request() == results

def test_wiki_summary(monkeypatch):
    search = "Lyon"
    result = ["Lyon (prononcé /lj?~/ ou /li?~/ ) est une commune française située dans le quart sud-est de la France au confluent du Rhône et de la Saône. Siège du conseil de la métropole de Lyon, elle est le chef-lieu de l'arrondissement de Lyon, de la circonscription départementale du Rhône et de la région Auvergne-Rhône-Alpes. Le gentilé est Lyonnais.\nLyon a une situation de carrefour géographique du pays, au nord du couloir naturel de la vallée du Rhône (qui s'étend de Lyon à Marseille). Située entre le Massif central à l'ouest et le massif alpin à l'est,.",'https://fr.wikipedia.org/wiki?curid=802627']
    
    def w_request():
        return {'batchcomplete': '', 'warnings': {'extracts': {'*': '"exlimit" was too large for a whole article extracts request, lowered to 1.'}}, 'query':{'pages': {'802627': {'pageid': 802627, 'ns': 0, 'title': 'Lyon', 'extract': "Lyon (prononcé /lj?~/ ou /li?~/ ) est une commune française située dans le quart sud-est de la France au confluent du Rhône et de la Saône. Siège du conseil de la métropole de Lyon, elle est le chef-lieu de l'arrondissement de Lyon, de la circonscription départementale du Rhône et de la région Auvergne-Rhône-Alpes. Le gentilé est Lyonnais.\nLyon a une situation de carrefour géographique du pays, au nord du couloir naturel de la vallée du Rhône (qui s'étend de Lyon à Marseille). Située entre le Massif central à l'ouest et le massif alpin à l'est,."}}}}

    def mock_w_request(*args, **kwargs):
        return w_request()

    monkeypatch.setattr(api_classes.WikiGlobal, "w_request", mock_w_request)
    sample = WikiGlobal()
    assert sample.wiki_summary(search) == result
        
def test_w_geosearch(monkeypatch):
    result = ["Lyon"]
    def w_request():
        return {'batchcomplete': '', 'query': {'normalized': [{'from': 'lyon', 'to': 'Lyon'}], 'pages': {'802627': {'pageid': 802627, 'ns': 0, 'title': 'Lyon'}}, 
        'geosearch': [{'pageid': 9261440, 'ns': 0, 'title': 'Sommet mondial climat et territoires', 'lat': 45.759723, 'lon': 4.842223, 'dist': 0, 'primary': ''}]}}
    
    def mock_w_request(*args, **kwargs):
        return w_request()
    monkeypatch.setattr(api_classes.WikiGlobal, "w_request", mock_w_request)
    sample = WikiGlobal()
    assert sample.w_geosearch(45.764942, 4.898393, "Lyon") == result

def test_get_coordinate(monkeypatch):
    result = (45.759723, 4.842223)
    def w_request():
        return {'batchcomplete': '', 'query': {'normalized': [{'from': 'lyon', \
        'to': 'Lyon'}], 'pages': {'802627': {'pageid': 802627, 'ns': 0, \
        'title': 'Lyon', 'coordinates': [{'lat': 45.759723, 'lon': 4.842223, \
        'primary': '', 'globe': 'earth'}]}}}}

    def mock_w_request(*args, **kwargs):
        return w_request()
    monkeypatch.setattr(api_classes.WikiGlobal, "w_request", mock_w_request)
    sample = WikiGlobal()
    assert sample.get_coordinate("Lyon") == result

def test_compare_coordinates(): 

    sample = WikiApi(48.856614, 2.3522219, "Paris")
    sample.w_latitude = 40.759723
    sample.w_longitude = 5.842223
    assert sample.compare_coordinates() == False
