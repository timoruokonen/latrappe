
'''
Schedule for one day for a NPC. The schedule contains actions and must be advanced when the NPC is advanced.

Scheduled tasks are for now always in a queue. First items are done first. If the day is finished and some
tasks are still unfinished, these should be moved to the next day.
'''
class Schedule(object):
    #Lame, just use minutes now
    MaxTime = 24 * 60

    def __init__(self):
        self.actions = []
        self.totalRemainingTime = Schedule.MaxTime

    def GetTotalRemainingTime(self):
        return self.totalRemainingTime

    def AddAction(self, action):
        self.actions.append(action)

    def Advance(self, time):
        timeToSpend = min(time, self.totalRemainingTime)
        timeLeft = time - timeToSpend
        self.totalRemainingTime -= timeToSpend

        #advance through actions and remove if completed
        while (timeToSpend > 0):
            action = self.GetCurrentAction()
            if (action != None):
                #print "Advancing action " + action.name + ". Time left of day: " + str(self.totalRemainingTime)       
                timeToSpend = action.Advance(timeToSpend)
                if (action.IsDone()):
                    self._RemoveAction(action)
            else:
                #print "Doing nothing..." + ". Time left of day: " + str(self.totalRemainingTime)
                break;
        return timeLeft

    def GetCurrentAction(self):
        if (len(self.actions) > 0):
            return self.actions[0]
        return None

    def GetCurrentActionName(self):
        if (len(self.actions) > 0):
            return self.actions[0].name
        return "Lazing around"

    def IsDone(self):
        return self.totalRemainingTime <= 0

    def GetListOfNotFinishedActions(self):
        return self.actions

    def _RemoveAction(self, action):
        self.actions.remove(action)

