from connection import client    
# First, we get the memory informations and stock it in an array with, in order: Total, used, free, shared, buff/cache, available
_, stdout, stderr = client.exec_command('cat /var/log/apache2/other_vhosts_access.log | grep "GET /?"')
output = stdout.read().decode("utf-8")

class WebPage():
    name=""
    numberOfSearchs=0
    
consultatedPages = []

line1 = output.splitlines()[0].split()

for line in output.splitlines():
    if not(line.split()[7] in consultatedPages):
        consultatedPages.append(line.split()[7])

print(consultatedPages)
