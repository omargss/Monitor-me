import paramiko;
import sys
from six.moves import configparser 

config = configparser.RawConfigParser()   
config.read("config.txt")
hostname = config['settings']['hostname']
port = config['settings']['port']
username = config['settings']['username']
password = config['settings']['password']

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

client.connect(hostname = hostname, port=port, username=username, password=password)

# First, we get the memory informations and stock it in an array with, in order: Total, used, free, shared, buff/cache, available
_, stdout, stderr = client.exec_command("free | grep -n Mem -")
output = stdout.read().decode("utf-8")
memorylist = output.splitlines()[0].split()
del memorylist[0]


