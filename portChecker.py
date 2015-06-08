from socket import *
import threading
setdefaulttimeout(0.2)


class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)


class portChecker:
    def __init__(self, host, initPort=1, endPort=65535, threads=20):
        self.pool = ActivePool()
        self.semaphore = threading.Semaphore(threads)
        self.host = host
        self.initPort = initPort
        self.endPort = endPort
        self.totalPorts = 0
        self.openedPorts = []

    def checkPort(self, port, s, pool):
        with s:
            try:
                name = threading.currentThread().getName()
                pool.makeActive(name)
                connection = socket(AF_INET, SOCK_STREAM)
                connection.connect((self.host, port))
                connection.sendall('Hello World!')
                result = connection.recv(512)
                if result == "":
                    result = 'No info about this port'
                connection.close()
                print 'Port ' + str(port) + '\n' + str(result) + '\n'
                self.totalPorts += 1
                self.openedPorts.append(port)
                pool.makeInactive(name)
            except:
                pass

    def checkOpenPorts(self):
        for port in range(self.initPort, self.endPort):
            try:
                t = threading.Thread(target=self.checkPort, args=(port, self.semaphore, self.pool,))
                t.start()
            except:
                pass