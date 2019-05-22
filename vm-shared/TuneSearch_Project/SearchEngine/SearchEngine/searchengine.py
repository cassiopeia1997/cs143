#!/usr/bin/python3

from flask import Flask, render_template, request

import search

application = app = Flask(__name__)
app.debug = True

@app.route('/search', methods=["GET"])
def dosearch():
    query = request.args.get('query',None)
    qtype = request.args.get('query_type',None)

    page_num = int(request.args.get('page_num',1))
    page_button = request.args.get('page_button','init')
    if page_button == 'Previous':
        page_num -= 1
    elif page_button == 'Next':
        page_num += 1
    else:
        page_num=1
   


    

    """
    TODO:
    Use request.args to extract other information
    you may need for pagination.
    """

    search_results = search.search(query, qtype,page_num,page_button)

    

    return render_template('results.html',
            query=query,
            results=len(search_results),
            search_results=search_results,
            page_num=page_num
            )

@app.route("/", methods=["GET"])

def index():
    if request.method == "GET":
        pass
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
