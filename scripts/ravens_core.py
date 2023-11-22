import sys, string, os, re
import socket
import time
import json

import scapy.all as scapy

from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

class CMD_Prompt:
    original_prompt = prompt = f"White-Raven > "
    SPACE = '#>SPACE$<#'

class HELP_Prompt:
    commands = {

        'help' : {
            'details' : f'''
            \r Really ?
            \r Displays the basic help page information.

            \r Command Usage:

            \r help
            \r or
            \r help <command>
            '''
        },

        'tools' : {
            'details' : f'''
            \r Create a tool or use a tool in the current session.
            \r Tools: Ravens Map, Ravens Fortel, Ravens Decoy, Ravens Audit

            \r Ravens Map:
            \r   Will map a network and all connected IP adresses.
            \r   Command Usage:
            \r   tool map <ip range>

            \r Ravens Fortel:
            \r   Takes an IP address and finds open ports and checks for vulnerabilities.
            \r   Command Usage:
            \r   tool fortel <IP address> <number of threads> <port range>

            \r Ravens Decoy:
            \r   Will turn the session into a decoy displaying an IP address scanning the
            \r   selected port address. Opening the port and baiting in anyone doing a port
            \r   scan on the device.
            \r   Command Usage:
            \r   tool decoy <device ip> <port number>

            \r Ravens Audit:
            \r   Searches through chosen logs with selected key words to check for suspicious
            \r   activity. Alternate quotes for keywords that have more than one word in it.
            \r   ie. 'unauthorized access' or "failed login" 
            \r   Command Usage:
            \r   tool audit <path to log file> <keywords to check for>
            '''
        },

        'policy' : {
            'details' : f'''
            \r Lets the user see the policy statements for using this program.

            \r Command Usage:
            \r policy
            '''
        }
    }

    def basic_help():
        print(
            f'''
            \r   Command                 Description

            \r help     [+]     Prints this message or the help for specific command.
            \r tools    [+]     Creates a tool or uses the tool in the current session.
            \r policy           Allows the user to view the policy statement for use of program.

            \r Commands with [+] may take additional arguements.
            \r For details please use: help <command>
            '''
        )

    def detailed_help(cmd):
        print(HELP_Prompt.commands[cmd]['details']) if cmd in HELP_Prompt.commands.keys() else print(f'\nCould not find detailed help for {cmd}.\n')

class RAVEN_Fortel():
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RESET = Fore.RESET
    GRAY = Fore.LIGHTBLACK_EX

    # User adjustable variables
    num_threads = 1
    target_ip = '0.0.0.0'
    scanable_ports = []

    # Variables
    q = Queue()
    banner_dict = {}

    def port_scan(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((RAVEN_Fortel.target_ip, port))
            banner = s.recv(1024).decode()
            RAVEN_Fortel.banner_dict[port] = banner
            return True
        except:
            return False

    def get_ports():
        for port in RAVEN_Fortel.scanable_ports:
            RAVEN_Fortel.q.put(port)

    def worker():
        while not RAVEN_Fortel.q.empty():
            port = RAVEN_Fortel.q.get()

            if RAVEN_Fortel.port_scan(port):
                print(f'{RAVEN_Fortel.GREEN}[+] {port} is open!{RAVEN_Fortel.RESET}')
    
    def run_scanner():
        RAVEN_Fortel.get_ports()
        thread_list = []
        print()

        for t in range(1, int(RAVEN_Fortel.num_threads)):
            thread = Thread(target=RAVEN_Fortel.worker)
            thread_list.append(thread)
            
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        print(f'{RAVEN_Fortel.banner_dict}\n')

    def print_changes():
        print(RAVEN_Fortel.target_ip)
        print(RAVEN_Fortel.num_threads)
        print(f'{RAVEN_Fortel.start_port}-{RAVEN_Fortel.end_port}')

class RAVEN_Map():
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RESET = Fore.RESET
    GRAY = Fore.LIGHTBLACK_EX

    def get_device_name(ip):
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except socket.herror:
            return "N/A"

    def scan(ip):
        arp_request = scapy.ARP(pdst=ip)
        
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request

        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        
        clients_list = []
    
        for element in answered_list:
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, 'name': RAVEN_Map.get_device_name(element[1].psrc)}
            clients_list.append(client_dict)
        
        return clients_list

    def print_result(results_list):
        print("\nIP Address\t\tMAC Address\t\tDevice Name\n")
        for client in results_list:
            print(f'{RAVEN_Map.GREEN}{client["ip"]}{RAVEN_Map.RESET}\t\t{client["mac"]}\t{client["name"]}')

class RAVEN_Audit():
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RESET = Fore.RESET
    GRAY = Fore.LIGHTBLACK_EX

    def audit_logs(log_file_path, suspicious_patterns):
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()

            parsed_logs = [line for line in log_content.split('\n')]

        for log_entry in parsed_logs:
            for pattern in suspicious_patterns:
                if pattern in str(log_entry):
                    print(f'{RAVEN_Audit.YELLOW}[+] Suspicious Activity Found!:{RAVEN_Audit.RESET}\n\t{log_entry}')

class RAVEN_Decoy():
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RESET = Fore.RESET
    GRAY = Fore.LIGHTBLACK_EX

    def start_server(ip_address, port):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            server_socket.bind((ip_address, int(port)))

            server_socket.listen(5)
            print(f'\nPort {port} is now open on {ip_address}. Listening...\n')

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"{RAVEN_Decoy.YELLOW}[-] {client_address[0]}:{client_address[1]}{RAVEN_Decoy.RESET} connected to decoy!")

                client_socket.close()

        except KeyboardInterrupt:
            print('\nServer is shutting down...')
        except:
            print(f'Something went wrong! Make sure you are using your device IP address!\n')
        finally:
            server_socket.close()
            print("\tDecoy sever is now closed.\n")