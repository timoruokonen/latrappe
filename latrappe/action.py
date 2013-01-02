from resourcefactory import ResourceFactory


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
        if (self.is_done()):
            self._end_action()

        if (self.time_left < 0):
            #action was completed and some time was left
            return -self.time_left
        return 0

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

class StockAction(object):
    def __init__(self, name, resources_to_sell, resources_to_buy, duration, buyer_seller, stock):
        Action.__init__(self, name, duration)
        self.resources_to_sell = resources_to_sell
        self.resources_to_buy = resources_to_buy
        self.buyer_seller = buyer_seller

        self.stock = stock

    def _start_action(self):
        #TODO: think how to best implement this. Now stuff is just moved/sold already in start of the action...
        for resource in self.resources_to_sell:
            self.stock.sell_resource(resource, self.buyer_seller)

    def _end_action(self):
        pass


