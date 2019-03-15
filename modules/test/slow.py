import sys
import time
from threading import Thread

sys.path.append('..')
import emailer
    

class MyThread(Thread):
    def __init__(self,user,z):
        Thread.__init__(self)
        self.z = z
        self.user = user

    def run(self):
        time.sleep(int(self.z))
        emailer.send(self.user, "Slow", "Retraso de: " + str(self.z))