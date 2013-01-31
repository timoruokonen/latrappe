from resourcefactory import ResourceFactory
from resource import *
from schedule import *

class Action(object):
    def __init__(self, npc, name, duration):
        self.npc = npc
        self.name = name
        self.time_left = duration
        self.started = False
        self.aborted = False

    def is_done(self):
        return self.time_left <= 0

    def advance(self, time):
        if not self.started:
            print self.npc.name + " starting action " + self.name
            self.started = True            
            self._start_action()

        self.time_left -= time
        self._advance(time)

        if self.is_done() and not self.aborted:
            self._end_action()

        if (self.time_left < 0):
            #action was completed and some time was left
            return -self.time_left
        return 0

    def abort(self):
        print "Action aborted: " + self.name
        self.aborted = True
        self.time_left = 0
    

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
    def __init__(self, npc, name, inputs, outputs, duration, possession):
        Action.__init__(self, npc, name, duration)
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
        Action.__init__(self, buyer_seller, name, StockAction.DURATION)
        self.resources_to_sell = resources_to_sell
        self.resources_to_buy = resources_to_buy
        self.buyer_seller = buyer_seller

        self.stock = stock

    def _start_action(self):
        #TODO: think how to best implement this. Now stuff is just moved/sold already in start of the action...
        for resource in self.resources_to_sell:
            if self.stock.sell_resource(resource, self.buyer_seller.possession):
                print self.buyer_seller.name, " sold ", resource.__name__
            else:
                print self.buyer_seller.name, " failed to sell ", resource.__name__

        for resource in self.resources_to_buy:
            if self.stock.buy_resource(resource, self.buyer_seller.possession):
                print self.buyer_seller.name, " bought ", resource.__name__
            else:
                print self.buyer_seller.name, " failed to buy ", resource.__name__
                
    def _end_action(self):
        pass

class MoveAction(Action):
    DURATION = 60
    SPEED = 5

    def __init__(self, name, npc, x, y):
        Action.__init__(self, npc, name, MoveAction.DURATION)
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
 

class ProductUnitAction(Action):
    def __init__(self, npc, unit):
        target_status = unit.next_status()
        Action.__init__(self, npc, unit.name(target_status), unit.duration(target_status))
        self.unit = unit
        self.target_status = target_status

    def _advance(self, time):
        pass

    def _start_action(self):
        inputs = self.unit.inputs(self.target_status)
        if not self.npc.possession.has_resources(inputs):
            print "Not enough resources to start " + self.name + "! Go home..."
            self.abort()
            return
        #destroy input resources immediately
        for resource in inputs:
            self.npc.possession.destroy_resource(resource)
        
        if self.unit.needs_presence(self.target_status):
            self.unit.in_progress = True
        else:
            self.unit.in_progress = False
    
    def _end_action(self):
        print "Finished produce unit action: ", self.unit.name(self.target_status)
        self.unit.status = self.target_status
        self.unit.in_progress = False

        #if next status is "automatic" add a shceduled action to finnish it
        if not self.unit.needs_presence(self.unit.next_status()):
            Scheduler.instance().add_action(ProductUnitAction(self.npc, self.unit))
        
        outputs = self.unit.outputs(self.target_status)
        for output in outputs:
            self.npc.possession.add_resource(ResourceFactory.create_resource_from_nothing(output))
 
