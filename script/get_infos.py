import paramiko;
import sys
import configparser 
# ---------------------------------------------------------
#Class process used to stock our processes from ps command
class Process():
    def __init__(self, u, p, c, m, s, co):
        self.user = u
        self.cpu = c
        self.pid = p
        self.memory = m
        self.start_time = s
        self.command = co
    user = ""
    cpu = 0
    pid = 0
    memory = 0
    start_time = ""
    command = ""
# ---------------------------------------------------------
# We use configparser to read data from config.txt file and paramiko to connect with ssh
config = configparser.RawConfigParser()   
config.read("./config.txt")
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(hostname = config['settings']['hostname'], port=config['settings']['port'], username=config['settings']['username'], password=config['settings']['password'])
# ---------------------------------------------------------
# First, we get the username with the whoami command
_, stdout, stderr = client.exec_command("whoami")
output = stdout.read().decode("utf-8")
whoami = output.splitlines(0)[0]
# ---------------------------------------------------------
# then, we get the memory informations and stock it in an array with, in order: Total, used, free, shared, buff/cache, available
_, stdout, stderr = client.exec_command("free | grep -n Mem -")
output = stdout.read().decode("utf-8")
memorylist = output.splitlines()[0].split()
del memorylist[0]
# ---------------------------------------------------------
#then, we get informations for processes with (USER/PID/MEM/START TIME/COMMAND)
list_process = []
_, stdout, stderr = client.exec_command("ps -aux | sort -k 3 -r | grep -wv USER")
output = stdout.read().decode("utf-8")
for line in output.splitlines():
    line = line.split()
    process = Process(line[0],line[1],line[2],line[3],line[8] +"-"+ line[9], (" ").join(line[10:len(line)]))
    list_process.append(process)
# ---------------------------------------------------------