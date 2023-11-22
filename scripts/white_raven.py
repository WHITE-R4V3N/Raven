import sys
import argparse

from ravens_core import *

logo_text = '''
██╗    ██╗██╗  ██╗██╗████████╗███████╗    
██║    ██║██║  ██║██║╚══██╔══╝██╔════╝    
██║ █╗ ██║███████║██║   ██║   █████╗     
██║███╗██║██╔══██║██║   ██║   ██╔══╝    
╚███╔███╔╝██║  ██║██║   ██║   ███████╗    
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝       
                                            
██████╗  █████╗ ██╗   ██╗███████╗███╗   ██╗ 
██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║ 
██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║ 
██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║ 
██║  ██║██║  ██║ ╚████╔╝ ███████╗██║ ╚████║ 
╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝ 
            Created by: R4V3N
'''

if __name__ == '__main__':
    print(f'{logo_text}')

    print(f'  HELP\t\t TOOLS \t\tPOLICY\n')

    while True:
        try:
            usr_cmd_str = input(CMD_Prompt.prompt).strip()

            if usr_cmd_str == '':
                continue

            # Handle single and double quoted command arguements
            single_quoted = re.findall("'{1}[\s\S]*'{1}", usr_cmd_str)
            double_quoted = re.findall('"{1}[\s\S]*"{1}', usr_cmd_str)
            quoted_args = single_quoted + double_quoted

            if len(quoted_args):
                for arg in quoted_args:
                    space_escaped = arg.replace(' ', CMD_Prompt.SPACE)

                    if (space_escaped[0] == "'" and space_escaped[-1] == "'") or (space_escaped[0] == '"' and space_escaped[-1] == '"'):
                        space_escaped = space_escaped[1:-1]
                    
                    usr_cmd_str = usr_cmd_str.replace(arg, space_escaped)

            # Create cmd-line args list
            usr_cmd_str = usr_cmd_str.split(' ')
            command_list = [w.replace(CMD_Prompt.SPACE, ' ') for w in usr_cmd_str if w]
            command_list_len = len(command_list)
            command = command_list[0].lower() if command_list else ''

            if command == 'help':
                if command_list_len == 1:
                    HELP_Prompt.basic_help()
                if command_list_len == 2:
                    HELP_Prompt.detailed_help(command_list[1])

            elif command == 'tools':
                try:
                    if command_list[1] == 'map':
                        try:
                            target_ip = command_list[2]
                            scan_results = RAVEN_Map.scan(target_ip)

                            RAVEN_Map.print_result(scan_results)
                            print()
                        except:
                            print(f'Please use help command to see proper use of map tool.')
                    
                    elif command_list[1] == 'fortel':
                        try:
                            RAVEN_Fortel.target_ip = command_list[2]
                            RAVEN_Fortel.num_threads = command_list[3]

                            start_port, end_port = command_list[4].split('-')
                            start_port, end_port = int(start_port), int(end_port)

                            ports = [p for p in range(start_port, end_port)]

                            RAVEN_Fortel.scanable_ports = ports

                            RAVEN_Fortel.run_scanner()
                        except:
                            print('Please use help command to see proper use of frotel tool.')

                    elif command_list[1] == 'decoy':
                        try:
                            RAVEN_Decoy.start_server(command_list[2], command_list[3])
                        except:
                            print('Please use help command to see proper use of decoy tool.')

                    elif command_list[1] == 'audit':
                        try:
                            suspicious_patterns = []

                            for pattern in command_list[3:]:
                                suspicious_patterns.append(pattern)
                            print()
                            RAVEN_Audit.audit_logs(command_list[2], suspicious_patterns)
                            print()
                        except:
                            print('Please use help command to see proper use of audit tool.')
                except:
                    print(f'\n Please view | help tools | for proper usage of tools command.\n')

        except KeyboardInterrupt:
            print(f'\n\nWhite Raven is now closing. Good-bye!\n')
            sys.exit(0)