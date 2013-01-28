from resourcefactory import ResourceFactory
from resource import *
from schedule import *

class Action(object):
    def __init__(self, name, duration):
        self.name = name
        self.time_left = duration
        self.started = False

    def is_done(self):
        return self.time_left <= 0

    def advance(self, time):
        if not self.started:
            print "Starting action " + self.name               
            self.started = True            
            self._start_action()

        self.time_left -= time
        self._advance(time)

        if (self.is_done()):
            self._end_action()

        if (self.time_left < 0):
            #action was completed and some time was left
            return -self.time_left
        return 0

    def _start_action(self):
        pass

    def _end_action(self):
        pass

    def _advance(self, time):
        pass

'''
General action that requires input resources and produces output resources in given time. 
When the action is started, input resources are removed from the given possession instance.
When the action is finished, created output resources are added to the given possession instance.
'''
class ProduceAction(Action):
    def __init__(self, name, inputs, outputs, duration, possession):
        Action.__init__(self, name, duration)
        self.inputs = inputs
        self.outputs = outputs
        self.possession = possession
        self.created_outputs = []

    def _start_action(self):
        #Check that all reuired resources are available
        if not self.possession.has_resources(self.inputs):
            print "Not enough resources to start " + self.name + "! Go home..."
            self.time_left = 0
            return

        #create the output stuff right away also, so that resources are "reserved"
        #Don't give the results to the caller until duraton is passed
        for output_resource in self.outputs:
            created_output = ResourceFactory.create_resource(output_resource, self.possession)
            self.created_outputs.append(created_output)

    def _end_action(self):
        #Transfer produced output resources to the caller
        for output in self.created_outputs:
            self.possession.add_resource(output)

    #@staticmethod
    #def CreateSellAction(resourcesToBeSold, possession):
    #    return Action("Selling goods", [],  

class StockAction(Action):
    DURATION = 60

    def __init__(self, name, resources_to_buy, resources_to_sell, buyer_seller, stock):
        Action.__init__(self, name, StockAction.DURATION)
        self.resources_to_sell = resources_to_sell
        self.resources_to_buy = resources_to_buy
        self.buyer_seller = buyer_seller

        self.stock = stock

    def _start_action(self):
        #TODO: think how to best implement this. Now stuff is just moved/sold already in start of the action...
        for resource in self.resources_to_sell:
            if self.stock.sell_resource(resource, self.buyer_seller):
                print str(self.buyer_seller), " sold ", str(resource)
            else:
                print str(self.buyer_seller), " failed to sell ", str(resource)

        for resource in self.resources_to_buy:
            if self.stock.buy_resource(resource, self.buyer_seller):
                print str(self.buyer_seller), " bought ", str(resource)
            else:
                print str(self.buyer_seller), " failed to buy ", str(resource)
                
    def _end_action(self):
        pass

class MoveAction(Action):
    DURATION = 60
    SPEED = 5

    def __init__(self, name, npc, x, y):
        Action.__init__(self, name, MoveAction.DURATION)
        self.npc = npc
        self.x = x
        self.y = y

    def _advance(self, time):
        #start moving towards the destination
        new_x = self.npc.x
        new_y = self.npc.y

        #finish the action if npc arrives to destination
        if new_x == self.x and new_y == self.y:
            #print(str(self.npc), " reached destination (", self.x, ", ", self.y, ")!")
            self.time_left = 0
        else:
            self.time_left = MoveAction.DURATION


        if (new_x < self.x):
            new_x += min(self.x - new_x, time * MoveAction.SPEED)
        elif (new_x > self.x):
            new_x -= min(new_x - self.x, time * MoveAction.SPEED)
        if (new_y < self.y):
            new_y += min(self.y - new_y, time * MoveAction.SPEED)
        elif (new_y > self.y):
            new_y -= min(new_y - self.y, time * MoveAction.SPEED)

        self.npc.x = new_x
        self.npc.y = new_y

class FieldAction(Action):
    def __init__(self, name, npc, field, target_status):
        Action.__init__(self, name, field.get_action_duration(target_status))
        self.npc = npc
        self.field = field
        self.target_status = target_status

    def _advance(self, time):
        pass

    def _start_action(self):
        #print self.npc.possession.get_all()
        if self.target_status == FieldSquare.STATUS_SOWED:
            if not self.npc.possession.has_resources(FieldSquare.SOWING_INPUTS):
                print "Not enough resources to start sowing " + self.name + "! Go home..."
                self.time_left = 0
                return
            #destroy input resources immediately
            for resource in FieldSquare.SOWING_INPUTS:
                self.npc.possession.destroy_resource(resource)
    

    def _end_action(self):
        print "Finished field action: ", self.target_status
        self.field.status = self.target_status
        if self.target_status == FieldSquare.STATUS_SOWED:
            #add scheduler task to "automatically" grow the weed
            Scheduler.instance().add_action(FieldAction("Growing...", self.npc, self.field, FieldSquare.STATUS_READY_TO_BE_HARVESTED))
        elif self.target_status == FieldSquare.STATUS_HARVESTED:
            for output in FieldSquare.HARVEST_OUTPUTS:
                self.npc.possession.add_resource(ResourceFactory.create_resource_from_nothing(output))
            

 
