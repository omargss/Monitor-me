import paramiko;
import sys
import configparser 

def get_memory(client):
  _, stdout, stderr = client.exec_command("free | grep -n Mem -")
  output = stdout.read().decode("utf-8")
  memorylist = output.splitlines()[0].split()
  del memorylist[0]
  for i in range(len(memorylist)):
    memorylist[i] = int(memorylist[i])
  return memorylist