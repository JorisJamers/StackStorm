import sys
from st2common.runners.base_action import Action
import datetime
from os.path import expanduser
import os



class WorkFlowAction(Action):

    fileName="StackStormCounter.cnf"
    fileLocation=expanduser("~/")
    path = fileLocation + fileName

    def __init__(self):

        # Check if file exists
        if os.path.isfile(self.path):

            # read data from filecnf
            line = self.ReadFile()

            # process file
            result = self.ProcessFile(line)

        else:
            self.WriteCounter(1, datetime.datetime.now())

        return


    def ProcessFile(self, line):

        count = int(self.GetCounter(line))
        time = self.GetTime(line)
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f ")

        # avoid wrong data
        if count > 3 or count < 0:
            count = 0

        if self.IsTimeWithinRange(time):
            # counter +1 , tijd hetzelfde houden
            print("time is within range")
            count = self.IncreaseCounter(count)

            if count >= 3:
                self.ResetFile()
                count = self.IncreaseCounter(count)
                self.WriteCounter(count, datetime.datetime.now())
                return "error"
            else:
                return "succes"


            #self.WriteCounter(count, time)
        else:
            #tijd resetten en counter op 1 zetten
            print("tijd niet in range -> reset")
            self.ResetFile()
            count = self.IncreaseCounter(count)
            self.WriteCounter(count, datetime.datetime.now())
            return "succes"


    def GetTimePlusRange(self, time):
        # geeft de tijd  + 10 minuten terug
        newTime = time + datetime.timedelta(10,0)
        return newTime

    def IsTimeWithinRange(self, time):
        timePlusTen = time + datetime.timedelta(minutes=10)
        if datetime.datetime.now() < timePlusTen:
            return True
        else:
            return False

    def WriteCounter(self, count, time):
        file = open(self.path, "w")
        file.write(str(time) + " >> " + str(count))
        file.close()

    def ResetFile(self):
        count = 0
        self.WriteCounter(count, str(datetime.datetime.now()))

    def ReadFile(self):
        file = open(self.path)
        line = file.readline()
        file.close()
        return line

    def GetCounter(self, line):
        value=line.split(" ")
        return value[3]

    def GetTime(self, line):
        time=line.split(">>")
        return time[0]

    def IncreaseCounter(self, count):
        return count + 1
