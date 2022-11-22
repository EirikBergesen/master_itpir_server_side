from socket import create_server, SOL_SOCKET, SO_REUSEADDR
from datetime import datetime
import threading
from os import getcwd
from pytz import timezone as pytimezone


class respondingServer:
    '''Server class
    Runs 'forever/until broken', and responds to requests by sending a file.
    '''
    def __init__(self, host_ip, tcp_port, send_filename) -> None:
        '''Takes params: (host ip, tcp port, filename to send from same directory)
        '''
        # Connection variables
        self.host_ip = host_ip
        self.tcp_port = tcp_port
        self.tcp_addr = (host_ip, tcp_port)

        # Naming variables
        self.application_name = '[Sending Server]'
        self.send_file_name = send_filename
        self.transfer_end_note = "FIN END"

        # Timezone variable
        self.timezone = 'Europe/Oslo'

        print(f"{self.application_name} starts on host: {self.host_ip}, tcp port {self.tcp_port}. {self._get_time_from_timezone()}")
        threading.Thread(target=self._tcp_request_handler).start()

    
    def _tcp_request_handler(self):
        '''Accept TCP connection and send data.
        Opens a socket create_server.
        Tries to find and read file from/in same directory as this script.
        Packages file with acknowledgement message and an endnote.
        Sends all.
        '''
        tcp_socket = create_server(self.tcp_addr)
        tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcp_socket.listen()
        
        while True:
            conn, addr = tcp_socket.accept()


            # Start first timer
            first_time = self._get_time_from_timezone()


            #print(f"{self.application_name} Sending: \nAcknowledgement message to address: {addr}. {self._get_time_from_timezone()}")


            # Try to find and read file
            try:
                path = getcwd()
                with open(f"{path}/{self.send_file_name}", 'rb') as data_file:
                    data = data_file.read()
                    #print(f"{self.application_name} Sending:\n {self.send_file_name} \nto:  {addr}. {self._get_time_from_timezone()}")
            except:
                print(f"{self.application_name} The file does not exist. {self._get_time_from_timezone()}")
            

            # Timer after reading
            after_reading_time = self._get_time_from_timezone()


            # Data management




            
            after_data_operations_time = self._get_time_from_timezone()
            


            # Package timestamps
            timestamps = dict()
            timestamps['request_received'] = datetime.strftime(first_time, '%Y-%m-%d %H:%M:%S.%f%z')
            timestamps['after_reading_data'] = datetime.strftime(after_reading_time, '%Y-%m-%d %H:%M:%S.%f%z')
            timestamps['after_data_operations'] = datetime.strftime(after_data_operations_time, '%Y-%m-%d %H:%M:%S.%f%z')


            # Packaging and sending with end note
            packet = str([data, str(timestamps)])
            msg = packet + self.transfer_end_note
            conn.send(msg.encode())


    def _get_time_from_timezone(self):
        '''Returns time.now() from spesific timezone (self.timezone).
        self.timezone was set to europe/oslo
        '''
        time = datetime.now(pytimezone(self.timezone))
        return time



tcp_port = 5500
host_ip = '13.51.175.214'
send_file_name = 'tree-picture.jpg'
server = respondingServer(host_ip, tcp_port, send_file_name)
