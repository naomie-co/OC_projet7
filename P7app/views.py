"""Views of Pybot app"""

from flask import Flask, render_template, request, jsonify
from P7app.api.api_classes import WikiApi
from P7app.api.api_classes import GoogleMapsApi
from P7app.parser.parser_class import Parser_search

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/test_ajax/', methods=['POST'])
def bot_answer():
    """Data are collected from the ajax request and sent to an API"""

    #the question is parsed
    the_question = request.form['question']
    search_0 = Parser_search(the_question)
    search = search_0.focus_search()

    #get the GPS coordinates and the address from GoolgeMapsApi class
    g_search = GoogleMapsApi(search)
    g_answer = g_search.request()

    #get the wikipedia's data
    w_request = WikiApi(g_answer[1], g_answer[2], search)
    get_wiki_coordinates = w_request.wiki_coordinates()
    if get_wiki_coordinates:
        w_request.compare_coordinates()
        final_answer = w_request.wiki_geo_request()
    else:
        final_answer = w_request.wiki_summary_request()

    #data are send back to the js file
    return jsonify(final_answer=final_answer[0], link=final_answer[1], \
        address=g_answer[0], lat=g_answer[1], long=g_answer[2])
