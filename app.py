from flask import Flask, render_template, request, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, send
from itertools import groupby
from types import SimpleNamespace
from spch_module import *
from time import sleep
from calc_module import HEADERS_LIST

app = Flask(__name__, template_folder='../dist', static_folder='../dist/js')
app.config["Access-Control-Allow-Origin"] = "*"


DEBUG = True

CORS(app, resources={r'/*':{'origins':'*'}})

socketio = SocketIO(app, cors_allowed_origins='http://localhost:8080')




@app.route('/')
def index():
    return 'sadasdsad'


@app.route('/headers', methods=['GET'])
def url_header():
    return jsonify({
        'headers':HEADERS_LIST        
    })

@app.route('/default_limits', methods=['GET'])
def default_limits():
    return jsonify({
        'default_limits': DEFAULT_LIMITS        
    })

@app.route('/gdh_<spch_name>')
def get_gdh(spch_name):
    spch = next(filter(lambda x: x.name == spch_name, ALL_SPCH_LIST))
    return jsonify(get_gdh_curvs(spch))

@app.route('/base', methods=['GET'])
def base():
    return jsonify({
        'base':[{
            'pressure':item[0],
            'show':False,                    
            'list':[{
                'name':s.name,
                'title':s.title,
                'short_name':s.title[6:],
                'fnom':s.fnom
            } for s in item[1]]                    
        }for item in GROUPED_SPCH_LIST
    ]})

@socketio.on('one_calc')
def handle_from_python(data):
    for _ in data['modes']:
        sleep(0.2)
        emit('push_sol',{
            'id':data['id'],
            'compName':data['compName'],
            'sol':[data['compName']] * len(LENGTH)
        })        
if __name__ == '__main__':
    socketio.run(app)
