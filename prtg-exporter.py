import http.server
import time
import requests
import json
from urllib.parse import urlencode

ENDPOINT = "https://{PRTG MONITOR URL HERE}/api/" #You may need to change the api 
API_KEY = ''


class MyHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

    def _set_headers_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
    def do_GET(self):

        if "metrics" not in self.path and "/organizations" not in self.path:
            self._set_headers_404()
            return()

        self._set_headers()
 

        if "/metrics" in self.path:
            start_time = time.monotonic()
            displayedText = "# TYPE prtg_modem_status gauge\n"
            exportString = ""
            print("Starting to collect data...")
            print("Collecting Device List...")

            r = requests.get(ENDPOINT+"table.json?apitoken={}".format(API_KEY))
            print(r.text)
            if(r.status_code == 200):
                print("Collected Device List Successfully")
            else:
                print("Failed to collect device list")
            jsonObject = json.loads(r.text)
            print("Organizing Individual Device Data")



            for count,prtgModem in enumerate(jsonObject[""]):
                if(count>5 and prtgModem["sensor"] != ""): #remove duplicate entries and skip first 5 empty items in jsonObject

                    if("Up" == prtgModem["status"]):
                        onlineStatus = "1"
                    elif("Pause" in prtgModem["status"]):
                        onlineStatus = "2"
                    else:
                        onlineStatus = "0"

                    exportString = ('prtg_modem_status{name="'+prtgModem['device']+'",IsOnline="'+str(onlineStatus)+'"} ' + onlineStatus+"\n")
                    #print(exportString)
                    displayedText+=exportString



            displayedText += "# TYPE request_processing_seconds summary\n" 
            displayedText = displayedText + 'request_processing_seconds ' + str(time.monotonic() - start_time) + '\n'
            #print(displayedText)
            print(("Collected {} values").format(len(jsonObject[""])))
            
            self.wfile.write(displayedText.encode('utf-8'))
            self.wfile.write("\n".encode('utf-8'))
            return


HTTP_BIND_IP = "localhost"
HTTP_PORT_NUMBER = 3310

server_class = MyHandler
httpd = http.server.ThreadingHTTPServer((HTTP_BIND_IP, HTTP_PORT_NUMBER), server_class)
print(time.asctime(), "Server Starts - %s:%s" % ("*" if HTTP_BIND_IP == '' else HTTP_BIND_IP, HTTP_PORT_NUMBER))
httpd.serve_forever()
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print(time.asctime(), "Server Stops - %s:%s" % ("localhost", HTTP_PORT_NUMBER))
