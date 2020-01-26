import requests

#TO ADD:
#add functionality for extra params?
#pattern matching on payload?
#add optional flag to display response - use argparse?
#specific arg for api key
#param for some pattern to match in response - e.g. searching for response that indicates correct pass
class Repeater:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def repType1(self, target, reqType):
        #print("Hello")
        request = requests.get(url = target)
        print(request.text)

    def repType2(self, target, reqType):
        paramName = input("Enter name of param to repeat over:\n")
        start = int(input("Enter starting number:\n"))
        end = int(input("Enter last number:\n"))
        step = int(input("Enter step:\n"))

        if reqType == "get":
            for i in range(start, end, step):
                self.getRequest(target, {paramName:i})
        elif reqType == "post":
            for i in range(start, end, step):
                self.postRequest(target, {paramName:i})

    #get details of target url, type of request, name of incremental param, range of repeats, step
    def setRequest(self):
        repType = int(input("""Select Repeater type:\n
        1. Single request\n2. Param with numeric range"""))

        target = input("Enter target URL:\n")
        reqType = input("Enter request type (\"get\"/\"post\"):\n")

        if repType == 1:
            repType1(target, reqType)
        elif repType == 2:
            print("2")
            self.repType2(target, reqType)

    def postRequest(self, target, params):
        request = requests.post(url = target, data = params)
        print(request.text)

    def getRequest(self, target, _params):
        request = requests.get(url = target, params = _params)
        #print(request.text)
        print(request.url)
        print(request.status_code)
        print(request.headers)

if __name__ == "__main__":
    repeater = Repeater()
    #repeater.repType1("https://www.google.com", "")
    repeater.setRequest()
    #repeater.postRequest("http://www.google.com")