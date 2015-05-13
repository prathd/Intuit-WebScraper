import requests
import time
import json

_key = None
_secret = None
_endpoint = None

_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

_expire = 5
_cache = { }

# Hybrids
def key(value=None) :
    global _key
    if value != None :
        _key = value
    return _key

def secret(value=None) :
    global _secret
    if value != None :
        _secret = value
    return _secret

def endpoint(value=None) :
    global _endpoint
    if value != None :
        _endpoint = value
    return _endpoint

def headers(value=None) :
    global _headers
    if value != None :
        _headers = value
    return _headers

def RelateIQ(_key,_secret,_endpoint=None) :
    if _endpoint == None :
        _endpoint = 'https://api.relateiq.com/v2/'
    key(_key)
    secret(_secret)
    endpoint(_endpoint)

# Helper Functions
def cache(endpoint,value=None) :
    if(value != None) :
        _cache[endpoint] = value
    return _cache.get(endpoint,{})

def process_response(response) :
    if response.status_code == 503 :
        raise NotImplementedError("This function is not currently supported by RelateIQ")
    elif response.status_code == 404 :
        raise requests.exceptions.HTTPError("Object Not Found", response=response)
    elif response.status_code >= 400 :
        # Record Response Data
        message = "\n[" + str(response.status_code) + "] "
        message += response.reason + " : "
        if response.text == None :
            message += "<no message>"
        elif response.apparent_encoding == "json" :
            message += "\n" + response.json().get("errorMessage","<no message>")
        else :
            message += "\n" + response.text

        # Record Request Data
        request = response.request
        if request != None :
            message += "\n    Request: " 
            message += request.method + " " + request.url 
            if request.body != None :
                message += "\n" + request.body
        raise requests.exceptions.HTTPError(message, response=response)
    # 404 Object not found
    #    if List, have them check if it is shared
    # 500
    # 422
    # 400 Bad Request - pass on internal message
    # 502 Bad Gateway - Reattempt
    response.raise_for_status()
    return response.json()

def send_request(request) :
    session = requests.Session()
    prepared_request = session.prepare_request(request)
    response = session.send(prepared_request)
    result = process_response(response)
    return result

# HTTP Functions
def get(_endpoint,options={}) :
    request = requests.Request(
        method = 'GET',
        url = endpoint() + _endpoint,
        params=options,
        auth=(key(),secret()),
        headers=headers()
    )
    result = send_request(request)
    return result

def post(_endpoint,data,options={}) :
    request = requests.Request(
        method = 'POST',
        url = endpoint() + _endpoint,
        params=options,
        data=json.dumps(data),
        auth=(key(),secret()),
        headers=headers()
    )
    result = send_request(request)
    return result

def put(_endpoint,data,options={}) :
    request = requests.Request(
        method = 'PUT',
        url = endpoint() + _endpoint,
        params=options,
        data=json.dumps(data),
        auth=(key(),secret()),
        headers=headers()
    )
    result = send_request(request)
    return result

def delete(_endpoint,options={}) :
    request = requests.Request(
        method = 'DELETE',
        url = endpoint() + _endpoint,
        params=options,
        auth=(key(),secret()),
        headers=headers()
    )
    result = send_request(request)
    return result

def fetch(endpoint,options={}) :
    try:
        return get(endpoint)
    except requests.exceptions.HTTPError as e :
        if e.response.status_code == 404 :
            return {}
        raise e

# Configuration Methods
def fetchConfig() :
    return get('configs')
