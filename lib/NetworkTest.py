import socket


class NetworkTest():

    def isHTTPOK(self, host, port=80):
        """/*
        Function: isHTTPOK

            Test HTTP server connection

        Parameters:

            host - server ip or server domain
            port - server port (default=80)

        Return:

            Boolean
        */"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send("GET / HTTP/1.0\r\n\r\n")
            s.recv(512)
        except:
            return False

        return True
