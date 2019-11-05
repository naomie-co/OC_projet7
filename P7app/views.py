from flask import Flask, render_template, request
from P7app.api import api_classes
from P7app.api.api_classes import WikiApi

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/test_ajax/', methods=['GET'])
def test():
	# -----------------------STEP 4-------------------------
	# Data are collected from the request and sent to an API
	# ------------------------------------------------------
	search=request.form['recherche']
	test = GoogleMapsApi(search)
	r_google = test.request() 
	w_request = WikiApi((r_google[1], r_google[2]), search)
	r = w_request.wiki_request()
	return render_template('index.html', r=r, question=search)
"""
@app.route('/', methods=['POST'])
def recherche():
	if request.method == 'POST': 
		search=request.form['recherche']
		if search is not "":
			return render_template('result.html', question=search)
	return index()

#if __name__ == "__main__":
#    app.run()
"""