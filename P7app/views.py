from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def recherche():
	if request.method == 'POST': 
		search=request.form['recherche']
		if search is not "":
			return render_template('result.html', question=search)
	return index()

#if __name__ == "__main__":
#    app.run()