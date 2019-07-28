from flask import Flask, render_template, jsonify
import BigSearch
import jsonpickle

app = Flask(__name__)


@app.route('/search/<name>')
def search(name):
    list = BigSearch.BigSearch(name)
    return render_template('search.html', list=list)
    # response = app.response_class(
    #     response = jsonpickle.encode(list),
    #     status = 200,
    #     mimetype= 'application/json'
    # )
    # return render_template('search.html',response=response)



if __name__ == '__main__':
    app.run(debug=False)
