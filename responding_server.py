from socket import create_server, SOL_SOCKET, SO_REUSEADDR
from datetime import datetime
import threading
from os import getcwd
from pytz import timezone as pytimezone
from picture_math_module_folder.picture_math_module import *


class respondingServer:
    '''Server class
    Runs 'forever/until broken', and responds to requests by sending a file.
    '''
    def __init__(self, host_ip, list_of_file_names, tcp_port = 5500, modes = 0) -> None:
        '''Takes params: (host ip, tcp port, filename to send from same directory)
        '''
        # Connection variables
        self.host_ip = host_ip
        self.tcp_port = tcp_port
        self.tcp_addr = (host_ip, tcp_port)
        self._BUFFER_SIZE = 1024
        self.tcp_transfer_endnote = 'FIN'

        # Naming variables
        self.application_name = f"[Server On Host: {self.host_ip}, OnPort: {tcp_port}]"
        self.list_of_file_names = list_of_file_names

        # Timezone variable
        self.timezone = 'Europe/Oslo'

        print(f"{self.application_name} starts on host: {self.host_ip}, tcp port {self.tcp_port}. {self._get_time_from_timezone()}")
        
        if modes == '1':
            print('Starting Chors')
            threading.Thread(target=self._tcp_request_handler_chors).start()
        else:
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
            print(f"Connection accepted from: {addr}")
            data = self._recvall(conn)
            # Start first timer
            first_time = self._get_time_from_timezone()

            if type(data) == str and not data in self.list_of_file_names:
                try:
                    evaluated_data = eval(data)
                except:
                    print('The data received could not be interpreted')
                    return 
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
                msg = packet + self.tcp_transfer_endnote
                conn.send(msg.encode())
            else:
                print('Could not build packet based on: ', str(data))


    def _tcp_request_handler_chors(self):
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
            print(f"Connection accepted from: {addr}")
            data = self._recvall(conn)
            # Start first timer
            first_time = self._get_time_from_timezone()
            data = eval(data)
            print('Data request received: ', data)
            if type(data) == list and type(data[0]) == int:
                wanting_list = []
                for iter, obj in enumerate(data):
                    if obj:
                        wanting_list.append(list_of_picture_names[iter])
                print('Wanted list: ', wanting_list)
                packet = self._make_data_package_chors(wanting_list, first_time=first_time)
                                    
            else:
                print(data, 'Can not be used. Something is wrong, not a list of ints')
            
            if packet:
                msg = packet + self.tcp_transfer_endnote
                conn.send(msg.encode())
            else:
                print('Could not build packet based on: ', str(data))


    def _make_data_package_chors(self, sending_filenames, first_time):
        # Timer after reading
        after_reading_time = self._get_time_from_timezone()
        
        # Try to find and read file
        if type(sending_filenames) == str: 
            sending_filenames = [sending_filenames]

        paths_for_pictures = []
        for iter, sending_filename in enumerate(sending_filenames):
            try:
                path = getcwd()
                full_path = f"{path}/{sending_filename}"
                paths_for_pictures.append(full_path)
            except:
                print(f"{self.application_name} The file does not exist. {self._get_time_from_timezone()}")
                return
        
        

        # Data management
        
        images_from_path = load_several_images_from_path(paths_for_pictures)
        merged_picture = add_several_images(images_from_path)
        returned_image_name = f"compounded_image{self.tcp_port}.png"
        save_image_as(merged_picture, returned_image_name)
        
        after_data_operations_time = self._get_time_from_timezone()
        
        data = []
        path = getcwd()
        full_path = f"{path}/{returned_image_name}"
        with open(full_path, 'rb') as data_file:
            data.append(data_file.read())

        # Package timestamps
        metadata = dict()
        metadata['name_of_server'] = self.application_name
        metadata['request_received'] = datetime.strftime(first_time, '%Y-%m-%d %H:%M:%S.%f%z')
        metadata['after_reading_data'] = datetime.strftime(after_reading_time, '%Y-%m-%d %H:%M:%S.%f%z')
        metadata['after_data_operations'] = datetime.strftime(after_data_operations_time, '%Y-%m-%d %H:%M:%S.%f%z')

        # Packaging
        packet = str([data, str(metadata)])
        return packet


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
        metadata = dict()
        metadata['name_of_server'] = self.application_name
        metadata['request_received'] = datetime.strftime(first_time, '%Y-%m-%d %H:%M:%S.%f%z')
        metadata['after_reading_data'] = datetime.strftime(after_reading_time, '%Y-%m-%d %H:%M:%S.%f%z')
        metadata['after_data_operations'] = datetime.strftime(after_data_operations_time, '%Y-%m-%d %H:%M:%S.%f%z')

        # Packaging
        packet = str([data, str(metadata)])
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
            if str(msg_array.decode()[-len(self.tcp_transfer_endnote):]).endswith(self.tcp_transfer_endnote):
                break
        
        # Remove endnote
        msg = msg_array.decode()[:-len(self.tcp_transfer_endnote)]
        return msg



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
default_tcp_port = '5500'
default_host_ip = ''
default_modes = '1'

print('Default port: 5500, No modes and HostIp is empty.')
tcp_port = input('What port should this server get: ')
modes = input("What mode should be used: default is chors")



if tcp_port:
    default_tcp_port = tcp_port
if modes:
    default_modes = modes

server = respondingServer(default_host_ip, list_of_picture_names, int(default_tcp_port), default_modes)