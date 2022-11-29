import paramiko;
import configparser 

config = configparser.RawConfigParser()   
config.read("./config.txt")
hostname = config['settings']['hostname']
port = config['settings']['port']
username = config['settings']['username']
password = config['settings']['password']

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(hostname = hostname, port=port, username=username, password=password)
