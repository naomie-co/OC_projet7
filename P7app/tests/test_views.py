import pytest
from P7app import app

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


	
	