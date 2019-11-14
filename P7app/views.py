from flask import Flask, render_template, request, jsonify
from P7app.api import api_classes
from P7app.api.api_classes import WikiApi
from P7app.api.api_classes import GoogleMapsApi

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/test_ajax/', methods=['POST'])
def bot_answer():
	# -----------------------STEP 4-------------------------
	# Data are collected from the request and sent to an API
	# ------------------------------------------------------
	search = request.form['question']
	g_search = GoogleMapsApi(search)
	g_answer = g_search.request()
	w_request = WikiApi(g_answer[1], g_answer[2], search)
	final_answer = w_request.wiki_request()
	return jsonify(final_answer=final_answer, search=search, lat=g_answer[1], long=g_answer[2])
""" 
@app.route('/', methods=['POST'])
def recherche():
	if request.method == 'POST': 
		search=request.form['recherche']
		if search is not "":
			return render_template('result.html', question=search)
	return index()
"""
#if __name__ == "__main__":
#	app.run()
