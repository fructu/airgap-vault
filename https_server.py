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
# backups are done like this:
#    tar -czvf vault/chromium_bk_0.tar.gz vault/chromium_bk/
# to restore:
#
#   restore from Persistent:
#
#       rm -rf ~/.cache/chromium
#       rm -rf ~/.config/chromium
#       rm -rf ~/.config/dconfig
#       rm -rf vault/cache
#       rm -rf vault/config
#       tar -xf vault/cache_chromium_bk_0.tar.gz
#       tar -xf vault/config_chromium_bk_0.tar.gz
#       tar -xf vault/config_dfconf_bk_0.tar.gz
# 
#   Note: bigger number in bk_#n.tar.gz does not imply newer
#     to check last one see dates with this command
#        ls -lhd vault/*
#
import http.server
import ssl
from multiprocessing import Process
import subprocess
from time import sleep
from lib.backup import Backup

IP = "127.0.0.1"
PORT = 5000
DIRECTORY = "www"

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

def isYes(question):
    response = input(question)
    if not response:
        return False

    if response[0].lower() == "y":
        return True

    return False

def chromium_open():
    bk = Backup()
    bk.pre_chromium()
    sleep(1)
    print('chromium "https://'+IP+':'+str(PORT)+'/"')
    code = subprocess.call(["chromium", "https://"+IP+":"+str(PORT)+"/"])
    print("-------------------------------------------------------")
    print("if created a new wallet or do you want to save cookies")
    if isYes("  backup y/n? "):
        bk.run()
        bk.post_chromium()

def main():
    print("megatron.thx airgap-vault v1.4")

    server = Process(target=https_server_run)
    server.start()
    chromium_open()
    server.terminate()
    input("press any key to close window ...")

main()
