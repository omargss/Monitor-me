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

def get_error_logs():
    """Retourne les logs d'erreur"""
    cmd = 'cat /var/log/apache2/error.log | grep "warn"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    warn_list = []
    for line in output.splitlines():
        warn_list.append(line)
    
    cmd = 'cat /var/log/apache2/error.log | grep "emerg"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    emerg_list = []
    for line in output.splitlines():
        emerg_list.append(line)

    cmd = 'cat /var/log/apache2/error.log | grep "alert"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    alert_list = []
    for line in output.splitlines():
        alert_list.append(line)

    cmd = 'cat /var/log/apache2/error.log | grep "crit"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    crit_list = []
    for line in output.splitlines():
        crit_list.append(line)

    cmd = 'cat /var/log/apache2/error.log | grep "error"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    error_list = []
    for line in output.splitlines():
        error_list.append(line)

    cmd = 'cat /var/log/apache2/error.log | grep "notice"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    notice_list = []
    for line in output.splitlines():
        notice_list.append(line)

    cmd = 'cat /var/log/apache2/error.log | grep "debug"'
    _, stdout, _ = client.exec_command(cmd)
    output = stdout.read().decode("utf-8")
    debug_list = []
    for line in output.splitlines():
        debug_list.append(line)

    return warn_list, emerg_list,alert_list, crit_list, error_list, notice_list,debug_list

warnlist = get_error_logs()
print(len(warnlist))