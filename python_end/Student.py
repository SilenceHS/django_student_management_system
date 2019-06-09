class Student:
    def __init__(self,ID,name,pcount,qcount,qscore):
        self.ID=ID
        self.name=name
        self.pcount=pcount
        self.qcount=qcount
        self.qscore=qscore
        if(qscore is None):
            self.qscore=0