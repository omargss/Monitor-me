""" Module functions"""
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# Class Process used to store processes
class Process:
    """ Process class"""
    def __init__(self, u, p, c, m, s, co): # pylint: disable=too-many-arguments
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


# Class WebPage used to store web pages
class WebPage:
    """ Class WebPage """
    def __init__(self, name, number):
        self.name = name
        self.numberOfSearchs = number

    name = ""
    numberOfSearchs = 0
    def __eq__(self, other):
        return self.name == other.name and self.numberOfSearchs == other.numberOfSearchs

def get_memory(client):
    """ get memory function """
    _, stdout, _ = client.exec_command("free | grep -n Mem -")
    output = stdout.read().decode("utf-8")
    memorylist = output.splitlines()[0].split()
    del memorylist[0]
    for i in range(len(memorylist)): # pylint: disable=consider-using-enumerate
        memorylist[i] = int(memorylist[i])
    return memorylist

def AnalyzeLogs(file):
    """ Analyse logs function """
    consultatedWebPages = []
    for line in file.splitlines():
        trouve = 0
        for wp in consultatedWebPages:
            if wp.name == line.split()[7]:
                wp.numberOfSearchs += 1
            trouve = 1
        if trouve == 0:
            newWp = WebPage(line.split()[7], 1)
            consultatedWebPages.append(newWp)
    return consultatedWebPages


def get_access_logs(client):
    """ get access function """
    _, stdout, _ = client.exec_command(
        'cat /var/log/apache2/other_vhosts_access.log | grep "GET /?"'
    )
    output = stdout.read().decode("utf-8")
    ConsultatedWebPages = AnalyzeLogs(output)
    return ConsultatedWebPages

def get_error_logs(client):
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


def get_process_infos(client):
    """ get process infos function """
    list_process = []
    _, stdout, _ = client.exec_command(
        "ps -aux | sort -k 3 -r | grep -wv USER | head -n 10"
    )
    output = stdout.read().decode("utf-8")
    for line in output.splitlines():
        line = line.split()
        process = Process(
            line[0],
            line[1],
            line[2],
            line[3],
            line[8] + "-" + line[9],
            (" ").join(line[10 : len(line)]),
        )
        list_process.append(process)
    return list_process


def get_biggest_files(client):
    """ get biggest files function """
    list_files = []
    list_size = []
    _, stdout, _ = client.exec_command(
        "du -ah 2>/dev/null | sort -n -r | head -n 25 | sort -n"
    )
    output = stdout.read().decode("utf-8")
    for line in output.splitlines():
        line = line.split()
        list_files.append(line[0])
        list_size.append(line[1])
    return list_files, list_size
