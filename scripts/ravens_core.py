import sys, string, os, re
import socket
import time

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
            \r Tools: Ravens Map, Ravens Fortel, Ravens Decoy, Ravens Sense

            \r Ravens Map:
            \r   Will map a network and all connected IP adresses.
            \r   Command Usage:
            \r   tool map

            \r Ravens Fortel:
            \r   Takes an IP address and finds open ports and checks for vulnerabilities.
            \r   Command Usage:
            \r   tool fortel <IP address> <number of threads> <highest port to scan>

            \r Ravens Sense:
            \r   Will monitor the network for ping sweeps and intrusions.
            \r   Command Usage:
            \r   tool sense

            \r Ravens Decoy:
            \r   Will turn the session into a decoy or create a decoy script for a device.
            \r   The script can then be installed and run on a device.
            \r   It will ban any IP address that pings the device that the decoy is running on.
            \r   Command Usage:
            \r   tool decoy
            \r   or
            \r   tool decoy download
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
    init()

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

        for t in range(1, int(RAVEN_Fortel.num_threads)):
            thread = Thread(target=RAVEN_Fortel.worker)
            thread_list.append(thread)
            
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        print(f'{RAVEN_Fortel.banner_dict}')

    def print_changes():
        print(RAVEN_Fortel.target_ip)
        print(RAVEN_Fortel.num_threads)
        print(f'{RAVEN_Fortel.start_port}-{RAVEN_Fortel.end_port}')



