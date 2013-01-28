
'''
Schedule for one day for a NPC. The schedule contains actions and must be advanced when the NPC is advanced.

Scheduled tasks are for now always in a queue. First items are done first. If the day is finished and some
tasks are still unfinished, these should be moved to the next day.
'''
class Schedule(object):
    #Lame, just use minutes now
    MAX_TIME = 24 * 60

    def __init__(self):
        self.actions = []
        self.total_remaining_time = Schedule.MAX_TIME

    def get_total_remaining_time(self):
        return self.total_remaining_time

    def add_action(self, action):
        self.actions.append(action)

    def advance(self, time):
        time_to_spend = min(time, self.total_remaining_time)
        timeLeft = time - time_to_spend
        self.total_remaining_time -= time_to_spend

        #advance through actions and remove if completed
        while (time_to_spend > 0):
            action = self.get_current_action()
            if (action != None):
                #print "Advancing action " + action.name + ". Time left of day: " + str(self.total_remaining_time)       
                time_to_spend = action.advance(time_to_spend)
                if (action.is_done()):
                    self._remove_action(action)
            else:
                #print "Doing nothing..." + ". Time left of day: " + str(self.total_remaining_time)
                break;
        return timeLeft

    def get_current_action(self):
        if (len(self.actions) > 0):
            return self.actions[0]
        return None

    def get_current_action_name(self):
        if (len(self.actions) > 0):
            return self.actions[0].name
        return "Lazing around"

    def is_done(self):
        return self.total_remaining_time <= 0

    def get_ist_of_not_finished_actions(self):
        return self.actions

    def _remove_action(self, action):
        self.actions.remove(action)

class Scheduler(object):
    _instance = None

    def __init__(self):
        self._actions = []

    @staticmethod
    def instance():
        if Scheduler._instance == None:
            Scheduler._instance = Scheduler()
        return Scheduler._instance

    def add_action(self, action):
        self._actions.append(action)

    def advance(self, time):
        for action in self._actions:
            #print "advancing action: ", action
            action.advance(time)
            if (action.is_done()):
                self._actions.remove(action)



        



