from flask import Flask, render_template, request, jsonify
from P7app.api import api_classes
from P7app.api.api_classes import WikiApi
from P7app.api.api_classes import GoogleMapsApi
from P7app.parser import parser_class
from P7app.parser.parser_class import Parser_search

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/test_ajax/', methods=['POST'])
def bot_answer():
	# -----------------------STEP 4-------------------------
	# Data are collected from the request and sent to an API
	# ------------------------------------------------------
	the_question = request.form['question']
	print("la question :", the_question)#test
	search_0 = Parser_search(the_question)
	search = search_0.focus_search()
	print("le search :", search)#test
	g_search = GoogleMapsApi(search)
	g_answer = g_search.request()
	w_request = WikiApi(g_answer[1], g_answer[2], search)
	get_wiki_coordinates = w_request.wiki_coordinates()
	compare = w_request.compare_coordinates(g_answer[1], g_answer[2], get_wiki_coordinates[0], get_wiki_coordinates[1])
	final_answer = w_request.wiki_request()
	return jsonify(final_answer=final_answer[0], link=final_answer[1], address=g_answer[0], lat=g_answer[1], long=g_answer[2])


#if __name__ == "__main__":
#	app.run()
