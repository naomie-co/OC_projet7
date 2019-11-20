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


class MockResponse:

	# mock json() method always returns a specific testing dictionary
	@staticmethod
	def json():
		return {
			"formatted_adress": "Paris, France",
			"location": {"lat": 48.856614, "lng": 2.3522219},
			"status": "OK"
			}

def testGoogleMapsApi(monkeypatch):
	search = "Paris"
	results = ["Paris, France", 48.856614, 2.3522219, "OK"]


	def mock_get(*args, **kwargs):
		return MockResponse()

	# apply the monkeypatch for requests.get to mock_get
	monkeypatch.setattr(api_classes.requests, "get", mock_get)
	
	sample = GoogleMapsApi(search)
	assert sample.request() == results


def testWikiApi(monkeypatch):
	search = "Lyon"
	result = """Lyon (prononcé /lj?~/ ou /li?~/ ) est une commune française située dans le quart sud-est de la France au confluent du Rhône et de la Saône. Siège du conseil de la métropole de Lyon, elle est le chef-lieu de l'arrondissement de Lyon, de la circonscription départementale du Rhône et de la région Auvergne-Rhône-Alpes. Le gentilé est Lyonnais.
Lyon a une situation de carrefour géographique du pays, au nord du couloir naturel de la vallée du Rhône (qui s'étend de Lyon à Marseille). Située entre le Massif central à l'ouest et le massif alpin à l'est, la ville de Lyon occupe une position stratégique dans la circulation nord-sud en Europe."""	

	def mock_summary(wikipedia):

		return """Lyon (prononcé /lj?~/ ou /li?~/ ) est une commune française située dans le quart sud-est de la France au confluent du Rhône et de la Saône. Siège du conseil de la métropole de Lyon, elle est le chef-lieu de l'arrondissement de Lyon, de la circonscription départementale du Rhône et de la région Auvergne-Rhône-Alpes. Le gentilé est Lyonnais.
Lyon a une situation de carrefour géographique du pays, au nord du couloir naturel de la vallée du Rhône (qui s'étend de Lyon à Marseille). Située entre le Massif central à l'ouest et le massif alpin à l'est, la ville de Lyon occupe une position stratégique dans la circulation nord-sud en Europe."""

	monkeypatch.setattr(api_classes.WikiGlobal, "wiki_summary", mock_summary)
	sample = WikiApi(45.764942, 4.898393, search)
	assert sample.wiki_request() == result




