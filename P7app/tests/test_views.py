import pytest
import requests
from P7app import app
from P7app.parser.parser_class import Parser_search
from P7app.api.api_classes import GoogleMapsApi
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
	sample = Parser_search("Bonjour, parle-moi de Paris!")
	sample.filter_parser()
	assert sample.filter_parser() == ["bonjour,", "parle-moi", "paris!"]


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
	results = {
			"formatted_adress": "Paris, France",
			"location": {"lat": 48.856614, "lng": 2.3522219},
			"status": "OK"
			}


	def mock_get(*args, **kwargs):
		return MockResponse()

	# apply the monkeypatch for requests.get to mock_get
	monkeypatch.setattr(api_classes.requests, "get", mock_get)
	
	sample = GoogleMapsApi(search)
	assert sample.request() == results


def testWikiApi(monkeypatch):
	pass