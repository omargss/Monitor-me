"""Allows to manage a client"""
import paramiko

class Client:
    """Definition of a client"""
    def __init__(self,host,port,user,pwd):
        self.hostname=host
        self.port=port
        self.username=user
        self.password=pwd

    def connection(self):
        """Allows to connect to the client"""
        self.client_ssh.load_system_host_keys()
        self.client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client_ssh.connect(hostname=self.hostname,
            port=self.port,username=self.username, password=self.password)

    def exec_command(self,string):
        """Execute the command pass in parameter"""
        return self.client_ssh.exec_command(string)

    hostname=""
    port=""
    username=""
    password=""
    client_ssh=paramiko.SSHClient()
