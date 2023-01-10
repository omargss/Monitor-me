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
        client_ssh = paramiko.SSHClient()
        client_ssh.load_system_host_keys()
        client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client_ssh.connect(hostname=self.hostname,
            port=self.port,username=self.username, password=self.password)
        return client_ssh

    def change_client(self,host,port,user,pwd):
        """Change the client attributes (doesn't reload the connection"""
        self.hostname=host
        self.port=port
        self.username=user
        self.password=pwd

    hostname=""
    port=""
    username=""
    password=""
