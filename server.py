from flask import Flask, request
import sys
import requests

if len(sys.argv) < 2:
    print("Error: port not specified")
    sys.exit(1)
    
port = sys.argv[1]

app = Flask(__name__)



db= [0]

@app.route("/get", methods=['get'])
def get():
    return ''.join(str(a)+", " for a in db)


@app.route("/set", methods=['post'])
def set():
    if len(request.form) == 0:
        return "400: Bad Request"
    item = request.form["item"]
    db.append(int(item))
    return "200: OK"

@app.route("/store", methods=['post'])
def store():
    ''' receive db contents from another node '''
    if len(request.form) == 0:
        return "400: Bad Request"
    items = request.form["items"]
    global db   
    items = items[:-2]
    #return items
    db = [int(a.strip()) for a in items.split(',')]
    
    return ''.join(str(a)+", " for a in db)

@app.route("/replicate", methods=['post'])
def replicate():
    ''' send contents to another node '''
    
    if len(request.form) == 0:
        return "400: Bad Request"
    port = request.form["port"]
    url="http://127.0.0.1:"+port+"/store"
    
    data = {'items': ''.join(str(a)+", " for a in db)}

    x = requests.post(url, data=data)
    
    return x.text

app.run(debug=True, host='0.0.0.0', port=port)
