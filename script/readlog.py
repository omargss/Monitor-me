"""Module qui permet de récupérer des logs sur la machine"""
from connection import client

class WebPage():
    """Classe qui permet de modéliser le nombre de fois où une page a été consultée."""
    def __init__(self, name, number):
        self.name = name
        self.researches_number = number
    name=""
    numberOfSearchs=0

def get_access_logs():
    """Retourne les pages consulté sur le serveur apache"""
    cmd = 'cat /var/log/apache2/other_vhosts_access.log | grep "GET /?"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    consultated_web_pages = []
    for line in output.splitlines():
        trouve = 0
        for web_page in consultated_web_pages:
            if web_page.name == line.split()[7]:
                web_page.numberOfSearchs += 1
                trouve =1
        if trouve == 0:
            new_web_page = WebPage(line.split()[7],1)
            consultated_web_pages.append(new_web_page)
    return consultated_web_pages

consultatedPages = get_access_logs()

for wp in consultatedPages:
    print(wp.name + " "+str(wp.numberOfSearchs))
