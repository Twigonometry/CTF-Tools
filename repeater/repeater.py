import requests
import sys
import getopt

#TO ADD:
#add functionality for extra params?
#pattern matching on payload?
#add optional flag to display response - use argparse?
#specific arg for api key
#param for some pattern to match in response - e.g. searching for response that indicates correct pass
#make use of requests params feature if users only submitting params (i.e at the end of the URL, ?param=val)

#USAGE:
#python3 repeater.py -u url -p list of payloads to be modified in payload options
#url -u takes a fully qualified domain name as the target - payloads are marked by $x$ where x is any alphanumeric character - escape a dollar with a '\'
#program will pick up on dollars and prompt you to specify payload options for each of these - options you provide will use regex replace to encode attack payloads into these positions
#alternatively, you can provide a list of payload positions with -p - these are defined by [a, b, c] where a, b and c are unique strings in the URL - the first occurrence of these will be treated as the payload, so make sure they only appear once!

HTTP_VERBS = ["GET", "POST"]

class Repeater:
    target = None
    positions = []
    payloads = {}

    def __init__(self, target, positions):
        """constructor for repeater"""
        self.target = target
        self.positions = positions

        #confirm positions are correct
        print("Target: " + self.target)
        print("Positions:")
        for pos in self.positions:
            print(str(pos))
        print("If these positions are incorrect, make sure you have specified a unique string for each, or try wrapping each position in $ signs")

        cont = input("Press q to quit and resubmit your parameters, or any other key to continue\n").upper()
        if cont == "Q" or cont == "QUIT":
            sys.exit()

        for pos in positions:
            self.payloads[pos] = define_payload(self.target, pos)

        print(self.payloads)

    #get methods

    def get_target(self):
        return self.target

    def get_positions(self):
        return self.positions

    def get_payloads(self):
        return self.payloads

    def exec_payload(self, pos, payload):
        start = self.target.find(pos)
        fin = start + len(pos)
        pos_highlight = self.target[:start] + "(" + pos + ")" + self.target[fin:]
        print("Executing payload for position: " + pos_highlight)

        i = payload['fst']
        step = payload['step']
        lst = payload['lst']

        while i <= lst:
            url = self.target[:start] + str(i) + self.target[fin:]
            print("Sending request to " + url)

            #set data
            if not "data" in payload:
                data = None
            else:
                data = payload['data']

            #set headers
            if not "headers" in payload:
                headers = None
            else:
                headers = payload['headers']

            #send request based on verb type
            if payload['verb'] == "GET":
                r = self.getRequest(url, data, headers)
            elif payload['verb'] == "POST":
                r = self.postRequest(url, data, headers)

            i += step

    def postRequest(self, target, data, headers):
        request = requests.post(url = target, data = data, headers = headers)
        print("Request URL:\n" + request.url)
        print("Response text:\n" + request.text)
        print("Response status code:\n" + str(request.status_code))
        print("Response headers:\n" + str(request.headers))

    def getRequest(self, target, data, headers):
        request = requests.get(url = target, data = data, headers = headers)
        print("Request URL:\n" + request.url)
        print("Response text:\n" + request.text)
        print("Response status code:\n" + str(request.status_code))
        print("Response headers:\n" + str(request.headers))

def split_positions(pos_string):
    positions = pos_string.split(',')
    return positions

def define_payload(target, pos):
    start = target.find(pos)
    fin = start + len(pos)
    pos_highlight = target[:start] + "(" + pos + ")" + target[fin:]
    print("Define payload for position: " + pos_highlight)
    
    #choice of sequence of integers, items from wordlist etc
    #for now, just integers

    payload = {}

    fst = None
    while fst is None:
        try:
            fst = int(input("What number to start payload at?\n"))
        except:
            print("Please enter an integer")

    payload['fst'] = fst

    lst = None
    while lst is None:
        try:
            lst = int(input("What number to finish payload at?\n"))
        except:
            print("Please enter an integer")

    payload['lst'] = lst

    step = None
    while step is None:
        try:
            step = int(input("What step to use?\n"))
        except:
            print("Please enter an integer")

    payload['step'] = step

    print("First: " + str(fst) + "\nLast: " + str(lst) + "\nStep: " + str(step))

    #get choice of HTTP verb
    verb_choice = ""

    while verb_choice not in HTTP_VERBS:
        verb_choice = input("Define HTTP verb to use. Must be one of " + ",".join(HTTP_VERBS) + "\n").upper()

    payload['verb'] = verb_choice

    #get data to submit
    data_choice = input("Type 'data' to define data to be submitted with this payload, or any other key to continue\n").upper()
    if data_choice == "DATA":
        cont = ""
        data = {}

        #get key-value pairs
        while not (cont == "Q" or cont == "QUIT"):
            data_key = input("Enter key for data\n")
            data_val = input("Enter value for data\n")
            data[data_key] = data_val
            cont = input("Type 'q' to finish defining data, or any other key to add more key-value pairs\n").upper()

        payload['data'] = data

    #get data to submit
    headers_choice = input("Type 'headers' to define headers to be submitted with this payload, or any other key to continue\n").upper()
    if headers_choice == "HEADERS":
        cont = ""
        headers = {}

        #get key-value pairs
        while not (cont == "Q" or cont == "QUIT"):
            header_key = input("Enter key for header\n")
            header_val = input("Enter value for header\n")
            headers[header_key] = header_val
            cont = input("Type 'q' to finish defining headers, or any other key to add more key-value pairs\n").upper()

        payload['headers'] = headers

    return payload

def main(argv):

    print("NOTE: currently $ signs not supported when defining positions")

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

    #instantiate repeater
    repeater = Repeater(url, positions)

    for pos, payload in repeater.get_payloads().items():
        repeater.exec_payload(pos, payload)

if __name__ == "__main__":
    main(sys.argv[1:])