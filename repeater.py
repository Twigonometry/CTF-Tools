import requests

#TO ADD:
#add functionality for extra params?
#pattern matching on payload?
#add optional flag to display response - use argparse?
#specific arg for api key
#param for some pattern to match in response - e.g. searching for response that indicates correct pass

#get details of target url, type of request, name of incremental param, range of repeats, step
def setRequest():
    target = input("Enter target URL:\n")
    reqType = input("Enter request type (\"get\"/\"set\"):\n")
    paramName = input("Enter name of param to repeat over:\n")
    start = input("Enter starting number:\n")
    end = input("Enter last number:\n")
    step = input("Enter step:\n")

    if reqType == "postRequest":
        for i in range(start, end, step):
            postRequest(target, {paramName:i})
    elif reqType == "postRequest":
        for i in range(start, end, step):
            postRequest(target, {paramName:i})

def postRequest(target, params):
    request = requests.post(url = target, data = params)
    print(request.text)

def getRequest(target, params):
    request = requests.get(url = target, data = params)
    #print(request.text)