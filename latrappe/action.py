from resourcefactory import ResourceFactory


class Action(object):
    def __init__(self, name, duration):
        self.name = name
        self.timeLeft = duration
        self.started = False

    def is_done(self):
        return self.timeLeft <= 0

    def advance(self, time):
        if not self.started:
            print "Starting action " + self.name               
            self.started = True            
            self._start_action()

        self.timeLeft -= time
        if (self.is_done()):
            self._end_action()

        if (self.timeLeft < 0):
            #action was completed and some time was left
            return -self.timeLeft
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
        self.createdOutputs = []

    def _start_action(self):
        #Check that all reuired resources are available
        if not self.possession.HasResources(self.inputs):
            print "Not enough resources to start " + self.name + "! Go home..."
            self.timeLeft = 0
            return

        #create the output stuff right away also, so that resources are "reserved"
        #Don't give the results to the caller until duraton is passed
        for outputResource in self.outputs:
            createdOutput = ResourceFactory.CreateResource(outputResource, self.possession)
            self.createdOutputs.append(createdOutput)

    def _end_action(self):
        #Transfer produced output resources to the caller
        for output in self.createdOutputs:
            self.possession.AddResource(output)

    #@staticmethod
    #def CreateSellAction(resourcesToBeSold, possession):
    #    return Action("Selling goods", [],  

class StockAction(object):
    def __init__(self, name, resourcesToBeSold, resourcesToBeBought, duration, buyerSeller, stock):
        Action.__init__(self, name, duration)
        self.resourcesToBeSold = resourcesToBeSold
        self.resourcesToBeBought = resourcesToBeBought
        self.buyerSeller = buyerSeller
        self.stock = stock

    def _start_action(self):
        #Check that stock has resources to be bought
        if not self.stock.possession.HasResources(self.resourcesToBeBought):
            print "Not enough resources to start " + self.name + "! Go home..."
            self.timeLeft = 0
            return
        pass

    def _end_action(self):
        pass

