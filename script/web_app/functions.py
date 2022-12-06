import paramiko;
import sys
import configparser

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

class WebPage():
    def __init__(self, Name, Number):
        self.name = Name
        self.numberOfSearchs = Number
    name=""
    numberOfSearchs=0

def get_memory(client):
  _, stdout, stderr = client.exec_command("free | grep -n Mem -")
  output = stdout.read().decode("utf-8")
  memorylist = output.splitlines()[0].split()
  del memorylist[0]
  for i in range(len(memorylist)):
    memorylist[i] = int(memorylist[i])
  return memorylist

def getAccessLogs(client):
	consultatedWebPages = []
	_, stdout, stderr = client.exec_command('cat /var/log/apache2/other_vhosts_access.log | grep "GET /?"')
	output = stdout.read().decode("utf-8")
	for line in output.splitlines():
		trouve = 0
		for wp in consultatedWebPages:
			if wp.name == line.split()[7]:
				wp.numberOfSearchs += 1
				trouve =1
		if trouve == 0:
			newWp = WebPage(line.split()[7],1)
			consultatedWebPages.append(newWp)
	return consultatedWebPages

def getProcessInfos(client):
	list_process = []
	_, stdout, stderr = client.exec_command("ps -aux | sort -k 3 -r | grep -wv USER | head -n 10")
	output = stdout.read().decode("utf-8")
	for line in output.splitlines():
		line = line.split()
		process = Process(line[0],line[1],line[2],line[3],line[8] +"-"+ line[9], (" ").join(line[10:len(line)]))
		list_process.append(process)
	return list_process