import socket

target_host = "httpbin.org"

target_port = 80  # create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data
request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
client.send(request.encode())

# receive some data
response = client.recv(4096)
http_response = repr(response)
http_response_len = len(http_response)


print(http_response)