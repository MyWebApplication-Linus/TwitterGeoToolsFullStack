from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from tools import get_politics, get_food, get_pop_culture, get_technology, get_latest
import json
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

latitude = 0
longitude = 0
location_selected = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    var = request.form["searchbarr"]
    print(var)
    return render_template("index.html")



@app.route("/location/coordinates", methods=['POST'])
@cross_origin()
def storeCoordinates():
    global latitude
    global longitude
    global location_selected
    if request.method == 'POST':
        # request must be a json with format:
        # { "latitude" : [value], "longitude" : [value] }
        coordinates = request.json
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        location_selected = '{},{},100mi'.format(latitude, longitude)
        return 'OK', 200
    else:
        return 'NOT IMPLEMENTED', 501


@app.route("/topic", methods=['GET'])
@cross_origin()
def getTweets():
    global latitude
    global longitude
    global location_selected
    if request.method == 'GET':
        if location_selected == "":
            return 'NO LOCATION SELECTED', 400
        # request must include a query parameter with a value of "politics", "food", "pop culture", "technology", or "latest"
        topic = request.args.get('topic')
        # map topic request params to function in tools.py
        options = {
            "politics" : get_politics,
            "food" : get_food,
            "pop culture" : get_pop_culture,
            "technology" : get_technology,
            "latest" : get_latest
        }
        # call the function in tools.py associated with the request param and return its contents
        return json.dumps(options[topic](location_selected))
    else:
        return 'NOT IMPLEMENTED', 501
