import sys
from threading import Thread
import os

sys.path.append('..')
import emailer
import config
from utilities import compress

class MyThread(Thread):
    def __init__(self,user):
        Thread.__init__(self)
        self.user = user
        self.name = "logs"
        self.attach = "./data/"+ self.name + ".tar.bz2"
        self.attachname = self.name[:10] + ".tar.bz2"

    def run(self):
        if compress(self.name) == 0:
            emailer.send(self.user,
                "PowerM Logs",
                "", self.attach,
                self.attachname)
            os.remove(self.attach)

__version__ = '0.1'