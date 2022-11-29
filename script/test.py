import paramiko;

# aelis / 118-TgBT-1407 / 22118

hostname = "gauvain.telecomste.net"
port = 22117
username = "grudu"
password = "117-TgBT-0216"


client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

client.connect(hostname = hostname, port=port, username=username, password=password)

# First, we get the memory informations and stock it in an array with, in order: Total, used, free, shared, buff/cache, available
_, stdout, stderr = client.exec_command("free | grep -n Mem -")
output = stdout.read().decode("utf-8")
memorylist = output.splitlines()[0].split()
del memorylist[0]
print(memorylist)

# First, we get the memory informations and stock it in an array with, in order: Total, used, free, shared, buff/cache, available
_, stdout, stderr = client.exec_command("free | grep -n Mem -")
output = stdout.read().decode("utf-8")
memorylist = output.splitlines()[0].split()
del memorylist[0]
print(memorylist)

