import httplib
import urllib
def encodeCredentials(**credentials):
    param = urllib.urlencode(credentials)
    return param

def request(request_type, request_route, request_param, header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"},  address = "localhost", port = 8000):
    response = ""
    try:
        connection = httplib.HTTPConnection("localhost", 8000)
        connection.request(request_type, request_route + request_param, "", header)
        data = connection.getresponse()
        response = data.read()
    except:
        return "not_connected", response
    return "connected", response
def uploadFile(request_type, request_route, file_content, user_key, address = "localhost", port = 8000):
    request_param = encodeCredentials(profile_picture = file_content, key = user_key)
    try:
        connection = httplib.HTTPConnection(address, port)
        connection.request(request_type, request_route, request_param)
        data = connection.getresponse()
        response = data.read()
    except:
        return "not_connected", response
    return "connected", response
