from connection import client    
_, stdout, stderr = client.exec_command('cat /var/log/apache2/other_vhosts_access.log | grep "GET /?"')
output = stdout.read().decode("utf-8")

class WebPage():
    def __init__(self, Name, Number):
        self.name = Name
        self.numberOfSearchs = Number
    name=""
    numberOfSearchs=0

def getAccessLogs():
    consultatedWebPages = []
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



consultatedPages = getAccessLogs()

for wp in consultatedPages:
    print(wp.name + " "+str(wp.numberOfSearchs))