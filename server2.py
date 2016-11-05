import sys
import SocketServer
import pickle
from mysql.connector import MySQLConnection, Error

data2 = [0,0,0,0]

def insert_data(data):
    query = "INSERT INTO Weather(Humidity,Temperature,Pressure,DTime) " \
            "VALUES(%s,%s,%s,%s)"
    args = (data[0], data[1],data[2],data[3])

    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='weather',
                                       user='root',
                                       password='test')
        cursor = conn.cursor()
        cursor.execute(query, args)
        print "db test"
        
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def request_handler(request_socket):
    try:
        print "test"
        request_msg = request_socket.recv(1024)
        data2 = pickle.load(request_msg)
        insert_data(data2)
        request_socket.send('HTTP/1.0 200 Ok')

    except Exception, ex:
        print 'e', ex,

def simple_tcp_server():
    tcp_server = SocketServer.TCPServer(("localhost", 443),
                                        RequestHandlerClass=None,
                                        bind_and_activate=True)

    while True:
        request_socket, address_port_tuple = tcp_server.get_request()
        print "Connection from: %s" % str(address_port_tuple)

        # nothing going to request handler
        request_handler(request_socket)
        # shutdown request socket and close it
        #tcp_server.shutdown_request(request_socket)

if __name__ == "__main__":
    simple_tcp_server()
