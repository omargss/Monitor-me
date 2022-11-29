import paramiko;
import sys
import configparser 

class Process():
    def __init__(self, u, p, m, s, co):
        self.user = u
        self.pid = p
        self.memory = m
        self.start_time = s
        self.command = co

    user = ""
    pid = 0
    cpu = 0
    start_time = ""
    command = ""

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

#then, we get the username with the whoami command
_, stdout, stderr = client.exec_command("whoami")
output = stdout.read().decode("utf-8")
whoami = output.splitlines(0)[0]

list_process = []
#then, we get informations for processes with (USER/PID/CPU/MEM/VSZ/RSS/TTY/STAT/START TIME / COMMAND)
_, stdout, stderr = client.exec_command("ps -aux | sort -k 4 -r | grep -wv USER | head -10 ")
output = stdout.read().decode("utf-8")
for line in output.splitlines():
    line = line.split()
    print(line)
    process = Process(line[0],line[1],line[3],line[9], line[10])
    list_process.append(process)

for i in range(len(list_process)):
    print(list_process[i].user, " ", list_process[i].pid," ", list_process[i].memory," ", list_process[i].start_time," ", list_process[i].command) 