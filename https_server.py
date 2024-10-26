#!/usr/bin/env python3
#
# https://stackoverflow.com/questions/77510803/how-to-make-a-simple-https-server-in-python-3x
#  The cert.pem and key.pem are created using this command:
#    openssl req -x509 -nodes -days 36500 -newkey rsa:2048 -keyout key.pem -out cert.pem
#
#   https://127.0.0.1:5000/
# 

import http.server
import ssl

#ip = "127.0.0.1"
#PORT = 5000
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


server_address = ("127.0.0.1", 5000)
httpd = http.server.HTTPServer(server_address, MyHandler)

context = get_ssl_context("cert.pem", "key.pem")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("megatron.thx https server https://127.0.0.1:5000/ v1.0")
httpd.serve_forever()