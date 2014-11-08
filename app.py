from flask import Flask, request, redirect, render_template
import jinja2
import os
from legislation import parse_legislation, parse_bill, parse_query

app = Flask(__name__)
app.debug = True

@app.route("/text", methods=['GET', 'POST'])
def text():
    result = None
    query = request.form.get('q')

    if query:
        result = parse_query(query)

    return render_template('legislation.html', result=result, query=query)

@app.route("/", methods=['GET', 'POST'])
def legislation():

    result = None
    query = request.args.get('q')

    if query:
        if query.find("legislation.gov.uk") >= 0:
            result = parse_legislation(query)

        if query.find("services.parliament.uk") >= 0:
            result = parse_bill(query)

    return render_template('legislation.html', result=result, query=query)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
