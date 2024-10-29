#!/usr/bin/env python3
#
# megatron.thx 2024 Margate
#
# https://stackoverflow.com/questions/77510803/how-to-make-a-simple-https-server-in-python-3x
#  The cert.pem and key.pem are created using this command:
#    openssl req -x509 -nodes -days 36500 -newkey rsa:2048 -keyout key.pem -out cert.pem
#    mv key.pm www/
#    mv cert.pm www/
#
#   https://127.0.0.1:5000/
#

import http.server
import ssl
from multiprocessing import Process
import subprocess
from time import sleep
import os

IP = "127.0.0.1"
PORT = 5000
DIRECTORY = "www"

# backups of previous directories
directories_previous_total = 10
directory_bk = "vault/chromium_bk/"
directories_bk = (
    ("~/.cache/", directory_bk+"cache/"),
    ("~/.config/", directory_bk+"config/")
)

def get_ssl_context(certfile, keyfile):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile, keyfile)
    context.set_ciphers("@SECLEVEL=1:ALL")
    return context

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        print(post_data.decode("utf-8"))

def https_server_run():
    server_address = (IP, PORT)
    httpd = http.server.HTTPServer(server_address, MyHandler)

    context = get_ssl_context("www/cert.pem", "www/key.pem")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("megatron.thx https server https://"+IP+":"+str(PORT)+"/")
    httpd.serve_forever()

def backup_previous():
    print("backup previous")
    #directory_bk
    for i in reversed(range(1, directories_previous_total)):
        if i <= 1:
            origin = directory_bk
        else:
            origin = directory_bk.replace("_bk/", "_bk_"+str(i-1)+"/")
        destiny = directory_bk.replace("_bk/", "_bk_"+str(i)+"/")

        command = "mkdir -p " + origin
        print(command)
        os.system(command)

        command = "mkdir -p " + destiny
        print(command)
        os.system(command)

        command = "cp -r -u " + origin + " " + destiny
        print(command)
        os.system(command)

def pre_chromium():
    print("restore from Persistent")
    for destiny, origin in directories_bk:
        command = "mkdir -p " + origin + "chromium "
        print(command)
        os.system(command)
        command = "cp -r -u " + origin + "chromium " + destiny
        print(command)
        os.system(command)

def post_chromium():
    print("saving to Persistent")
    for origin, destiny in directories_bk:
        command = "cp -r -u " + origin + "chromium " + destiny
        print(command)
        os.system(command)

def chromium_open():
    pre_chromium()
    sleep(1)
    print('chromium "https://'+IP+':'+str(PORT)+'/"')
    code = subprocess.call(["chromium", "https://"+IP+":"+str(PORT)+"/"])
    sleep(1)
    post_chromium()
    sleep(1)

def main():
    print("megatron.thx airgap-vault v1.0")
    backup_previous()
    server = Process(target=https_server_run)
    server.start()
    chromium_open()
    server.terminate()

main()
