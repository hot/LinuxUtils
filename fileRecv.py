import socket

bind_ip = "0.0.0.0"
bing_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.bind((bind_ip, bing_port))

f = open("downloadFile", 'wb')

server.listen(5)

print "[*] Listen on %s:%d" % (bind_ip, bing_port)

while True:
    c, addr = server.accept()
    print 'Got connect from', addr
    data = c.recv(1024)
    while data:
        print "Recving..."
        f.write(data)
        data = c.recv(1024)

    f.close()

    print 'Recv Over!!'
    c.send('Server RECV over ACK!')
    c.close()
    break

