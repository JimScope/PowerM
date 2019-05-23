import sys
from threading import Thread

sys.path.append('..')
import emailer

class MyThread(Thread):
    def __init__(self,user,z):
        Thread.__init__(self)
        self.z = int(z)
        self.user = user
        self.tab_list = []

    def run(self):
        for i in range(1,11):
            self.tab_list.append((self.z,"x",i,"=",self.z*int(i)))
        x = self.tab_list

        emailer.send(self.user,
            "Tabla del " + str(self.z),
            str(x))


__version__ = '0.1'




