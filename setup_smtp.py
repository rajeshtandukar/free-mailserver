#!/usr/bin/python

import sys
import paramiko
from CMD import *

class ErrorInCommand(Exception): pass

class MailuServerSetup:
    def __init__(self, hostname, ip, username, password):
        # Initialize with server credentials
        self.hostname = hostname.strip()
        self.ip = ip.strip()
        self.username = username.strip()
        self.password = password.strip()
        self.admin = f'admin@{self.hostname}'
        self.ssh_client = None

    def connect(self):
        # Establish SSH connection
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.load_system_host_keys()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.ip, username = self.username, password = self.password, allow_agent=False, look_for_keys=False, timeout=10)
        except paramiko.SSHException as e:
            print(f"Failed to connect via SSH: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
    
    def close(self):
        # Close SSH connection
        self.ssh_client.close()

    def execute_command(self, command):
        # Execute a command on the remote server
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        if stdout.channel.recv_exit_status() != 0:
                raise ErrorInCommand
        return stdout
        
    def run(self):
        # Main method to run the setup process
        self.connect()
        self.presetup()
        self.install_docker()
        self.install_docker_compose()
        self.install_mail_server()
        self.close()

    def presetup(self):
        # Pre-setup tasks
        self.execute_command(erase_prev_server_installations)
        self.execute_command(cmd_create_directory)
        # Use SFTP to upload necessary files
        sftp = self.ssh.open_sftp()
        sftp.put('docker-compose.yml', './mailu/docker-compose.yml')
        sftp.put('mailu.env', './mailu/mailu.env')
        self.execute_command(cmd_install_sed)
        self.execute_command(yml_file_sed_cmd(self.ip))
        self.execute_command(env_file_sed_cmd(self.hostname))
        self.execute_command(cmd_install_lsof_and_unzip)
        self.execute_command(cmd_kill_ports)
        

        print("Presetup executed successfully")

    def install_docker(self):
        # Install Docker if not already installed
        response = self.execute_command(cmd_check_install_or_update_docker)
        if (response.read().decode() == 'Install docker'):
            print("Installing Docker...")
            self.execute_command(cmd_install_yum_utils)
            self.execute_command(cmd_add_yum_repo)
            self.execute_command(cmd_install_docker)
            print("Docker installed successfully")

    def install_docker_compose(self):
        # Install Docker Compose if not already installed
        response = self.execute_command(cmd_check_docker_compose)
        if (response.read().decode() == 'yes'):
            print ('Docker compose already installed')
        else:
            print ('Installing docker compose...')
            self.execute_command(cmd_download_docker_compose)
            self.execute_command(cmd_permissions_docker_compose)
            self.execute_command(cmd_docker_compose_version) 
            print ('Docker compose installed successfully')

    def install_mail_server(self):
         # Install and configure Mailu mail server
        self.execute_command(cmd_create_directory)      
        self.execute_command(cmd_copy_contents)    
        self.execute_command(cmd_start_docker_engine)
        self.execute_command(f'{cmd_change_mail_ectory} {cmd_stop_docker_compose}')
        self.execute_command(f'{cmd_change_mail_ectory} {cmd_start_docker_compose}')
        self.execute_command(f'{cmd_change_mail_ectory} {cmd_start_docker_engine}')
        self.execute_command(f'{cmd_change_mail_ectory} {cmd_start_docker_compose_mail_server}')
        self.execute_command('sleep 15')
        self.execute_command(cmd_create_mail_admin_user(self.admin, self.hostname, password))        
        print('Mail server installed successfully')


def init():
    if len(sys.argv) != 5:
        print("Usage: script.py <hostname> <ip> <username> <password>")
        sys.exit(1)
    mailu_setup = MailuServerSetup(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    mailu_setup.run()

if __name__ == '__main__':
    init()