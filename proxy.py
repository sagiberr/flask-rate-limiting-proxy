from flask import Flask, request
import time



class Proxy:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.requests_log = {}


    def setup_routes(self):
        @self.app.route('/') # 
        def index():
            ip = request.remote_addr
            if not self.is_allowed(ip):
               return "Too Many Requests", 429
            return f"Hello from {ip}"

        
    def run(self):
        self.setup_routes()
        self.app.run(host=self.host, port=self.port)



    def is_allowed(self, ip: str) -> bool:
        now = time.time()
        window_seconds = 10
        max_requests = 5

        #list of times
        timestamps = self.requests_log.get(ip, [])

        # save only the requests from the last 10 sec
        recent = [t for t in timestamps if t > now - window_seconds]

        # update the log of the user
        recent.append(now)
        self.requests_log[ip] = recent

        #if there are too much requests- block
        if len(recent) > max_requests:
            return False
        return True

if __name__ == "__main__":
    proxy = Proxy("127.0.0.1", 5000)
    proxy.run()
