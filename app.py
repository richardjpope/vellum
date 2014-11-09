from flask import Flask, request, redirect, render_template
from flaskext.markdown import Markdown
import jinja2
import os
from legislation import parse_query

app = Flask(__name__)
app.debug = True
Markdown(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/result", methods=['GET', 'POST'])
def result():

    result = None
    query = request.form.get('q')

    if query:
        result = parse_query(query)

    return render_template('legislation.html', result=result, query=query)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
