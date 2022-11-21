# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
# add the listener socket to the set
    s = socket.socket()
    s.bind(("", port))
    s.listen()
    ready_set = [s]

    # main loop:
    while True: 
        # call select() and get the sockets that are ready to read
        ready_to_read, _, _ = select.select(ready_set, {}, {})

        # for all sockets that are ready to read:
        for ready_socket in ready_to_read:
            
            # if the ready_socket is the listener ready_socket:
            if ready_socket is s:
                
                # accept() a new connection
                client_connection, client_address = s.accept()
                print(f"{client_address}: connected")
               
                # add the new socket to our set!
                ready_set.append(client_connection)
                
            #  else the socket is a regular socket:
            else:
                
                # recv() the data from the socket
                data = ready_socket.recv(4096)
               
                # if you receive zero bytes
                if not data:
                   
                    # the client hung up
                    print(f"{ready_socket.getpeername()}: disconnected")

                    # remove the socket from tbe set!
                    ready_set.remove(ready_socket)
                else: 
                    print(f"{ready_socket.getpeername()} {len(data)} bytes: {data}")

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
