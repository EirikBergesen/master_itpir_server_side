from socket import create_server, SOL_SOCKET, SO_REUSEADDR
from datetime import datetime
import threading
from os import getcwd
from pytz import timezone as pytimezone


class respondingServer:
    '''Server class
    Runs 'forever/until broken', and responds to requests by sending a file.
    '''
    def __init__(self, host_ip, tcp_port, list_of_file_names) -> None:
        '''Takes params: (host ip, tcp port, filename to send from same directory)
        '''
        # Connection variables
        self.host_ip = host_ip
        self.tcp_port = tcp_port
        self.tcp_addr = (host_ip, tcp_port)
        self._BUFFER_SIZE = 1024
        self.tcp_transfer_endnote = 'FIN END'

        # Naming variables
        self.application_name = '[Sending Server]'
        self.list_of_file_names = list_of_file_names
        self.transfer_end_note = "FIN END"

        # Timezone variable
        self.timezone = 'Europe/Oslo'

        print(f"{self.application_name} starts on host: {self.host_ip}, tcp port {self.tcp_port}. {self._get_time_from_timezone()}")
        threading.Thread(target=self._tcp_request_handler).start()

    
    def _tcp_request_handler(self):
        '''Accept TCP connection and send data.
        Opens a socket create_server.
        Tries to find and read file from/in same directory as this script.
        Packages file, message and an endnote.
        Sends all.
        '''
        tcp_socket = create_server(self.tcp_addr)
        tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcp_socket.listen()
        
        while True:
            conn, addr = tcp_socket.accept()
            data = self._recvall(conn)
            # Start first timer
            first_time = self._get_time_from_timezone()

            if type(data) == str and not data in self.list_of_file_names:
                try:
                    evaluated_data = eval(data)
                except:
                    print('The data received could not be interpreted')
                if type(evaluated_data) == list:
                    for entry in evaluated_data:
                        if not entry in self.list_of_file_names:
                            print('The sent list contains items that is not contained in the server repertoare.')
                            return
                    packet = self._make_data_package(eval(data), first_time=first_time)
                    

            elif data in self.list_of_file_names:
                packet = self._make_data_package(data, first_time=first_time)
                
            else:
                print(data, 'is not in ', self.list_of_file_names)
            
            if packet:
                msg = packet + self.transfer_end_note
                conn.send(msg.encode())
            else:
                print('Could not build packet based on: ', str(data))


    def _make_data_package(self, sending_filenames, first_time):
        # Try to find and read file
        if type(sending_filenames) == str: 
            sending_filenames = [sending_filenames]

        data = []
        for iter, sending_filename in enumerate(sending_filenames):
            try:
                path = getcwd()
                full_path = f"{path}/{sending_filename}"
                with open(full_path, 'rb') as data_file:
                    data.append(data_file.read())
            except:
                print(f"{self.application_name} The file does not exist. {self._get_time_from_timezone()}")
                return
            
        # Timer after reading
        after_reading_time = self._get_time_from_timezone()

        # Data management
        after_data_operations_time = self._get_time_from_timezone()

        # Package timestamps
        timestamps = dict()
        timestamps['request_received'] = datetime.strftime(first_time, '%Y-%m-%d %H:%M:%S.%f%z')
        timestamps['after_reading_data'] = datetime.strftime(after_reading_time, '%Y-%m-%d %H:%M:%S.%f%z')
        timestamps['after_data_operations'] = datetime.strftime(after_data_operations_time, '%Y-%m-%d %H:%M:%S.%f%z')

        # Packaging
        packet = str([data, str(timestamps)])
        return packet


    def _get_time_from_timezone(self):
        '''Returns time.now() from spesific timezone (self.timezone).
        self.timezone was set to europe/oslo
        '''
        return datetime.now(pytimezone(self.timezone))

    
    def _recvall(self, socket_connection):
        '''Returns decoded message
        Builds a byte array from several messages sendt, with size buffersize
        '''
        # Building byte array
        msg_array = bytearray()
        while True:
            msg_part = socket_connection.recv(self._BUFFER_SIZE)
            msg_array.extend(msg_part)

            # Breaking at endnote
            # TODO: Somewaht unsure if this is secure, or maybe slow
            if str(msg_array.decode()).endswith(self.tcp_transfer_endnote):
                break
        
        # Remove endnote
        msg = msg_array.decode()[:-len(self.tcp_transfer_endnote)]
        return msg


tcp_port = 5500
host_ip = ''

list_of_picture_names = [
    'tree-picture_320240_00.png',
    'tree-picture_320240_01.png',
    'tree-picture_320240_02.png',
    'tree-picture_320240_03.png',
    'tree-picture_320240_04.png',
    'tree-picture_320240_05.png',
    'tree-picture_320240_06.png',
    'tree-picture_320240_07.png',
    'tree-picture_320240_08.png',
    'tree-picture_320240_09.png'
]


server = respondingServer(host_ip, tcp_port, list_of_picture_names)
