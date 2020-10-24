import requests
import sys
import getopt

#TO ADD:
#add functionality for extra params?
#pattern matching on payload?
#add optional flag to display response - use argparse?
#specific arg for api key
#param for some pattern to match in response - e.g. searching for response that indicates correct pass

#USAGE:
#python3 repeater.py -u url -p list of payloads to be modified in payload options
#url -u takes a fully qualified domain name as the target - payloads are marked by $x where x is any alphanumeric character - escape a dollar with a '\'
#program will pick up on dollars and prompt you to specify payload options for each of these - options you provide will use regex replace to encode attack payloads into these positions
#alternatively, you can provide a list of payload positions with -p - these are defined by [a, b, c] where a, b and c are unique strings in the URL - the first occurrence of these will be treated as the payload, so make sure they only appear once!

class Repeater:
    target = None
    positions = []
    payloads = {}

    def __init__(self, target, positions):
        """constructor for repeater"""
        self.target = target
        self.positions = positions

    #get methods

    def get_target(self):
        return self.target

    def get_positions(self):
        return self.positions

    def get_payloads(self):
        return self.payloads
        
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

def split_positions(pos_string):
    positions = pos_string.split(',')
    return positions

def main(argv):

    url = None
    positions = None

    try:
        opts, args = getopt.getopt(argv,"hu:p:",["url=","positions="])
    except getopt.GetoptError:
        print("USAGE: python3 repeater.py -u <URL> | url=<URL> [-p <positions> | positions=<positions>]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("USAGE: python3 repeater.py -u <URL> [-p <params>]")
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-p", "--positions"):
            pos_string = arg
    if url is None:
        print("USAGE: python3 repeater.py -u <URL> [-p <params>]")
        sys.exit()

    positions = split_positions(pos_string)

    print("URL: " + str(url))
    print("Positions: " + ",".join([str(p) for p in positions]))

    #instantiate repeater
    repeater = Repeater(url, positions)

    print(repeater.get_target())

    pos_copy = repeater.get_positions()
    for pos in pos_copy:
        print(str(pos))

if __name__ == "__main__":
    main(sys.argv[1:])