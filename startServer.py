import time
import requests
from python_aternos import Client
import argparse

class AternosWithCloudflare(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    def _request(self, method, url, *args, **kwargs):
        kwargs["timeout"] = 10
        response = self.session.request(method, url, *args, **kwargs)
        if response.status_code == 503 and "Cloudflare-Abusing" in response.text:
            print("Cloudflare protection detected. Waiting for 30 seconds...")
            time.sleep(30)
            response = self.session.request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response

def findServer(name):
    servs = atclient.account.list_servers()
    for serv in servs:
        serv.fetch()
        if serv.domain == f'{name}.aternos.me':
            return serv

    return None

def start_server(atclient, name):
    
    myserv = findServer(name)
    if myserv:
        myserv.start()
    else:
        print(f"ghir katkhra ya kho mkynch hada")

def stop_server(atclient, server_index):
    servs = atclient.account.list_servers()
    if server_index < 0 or server_index >= len(servs):
        print(f"Invalid server index: {server_index}")
        return
    myserv = servs[server_index]
    myserv.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aternos Minecraft Server Control")
    parser.add_argument("action", choices=["start", "stop"], help="Action to perform (start or stop)")
    parser.add_argument("index", type=str, help="Index of the server to control")
    args = parser.parse_args()
    with open ("token.txt" ,"r") as file:
        token = file.readline().replace("\n", '')
    atclient = AternosWithCloudflare()
    atclient.login_with_session(f"{token}")

    if args.action == "start":
        start_server(atclient, args.index)
    elif args.action == "stop":
        stop_server(atclient, args.index)
