from resourcefactory import ResourceFactory

'''
General action that requires input resources and produces output resources in given time. 
When the action is started, input resources are removed from the given possession instance.
When the action is finished, created output resources are added to the given possession instance.
'''
class Action(object):
    def __init__(self, name, inputs, outputs, duration, possession):
        self.started = False
        self.name = name
        self.timeLeft = duration
        self.inputs = inputs
        self.outputs = outputs
        self.possession = possession
        self.createdOutputs = []

    def _AddOutputs(self):
        for output in self.createdOutputs:
            self.possession.AddResource(output)

    def Advance(self, time):
        if not self.started:
            self._ReserveResourcesAndCreateOutputs()

        self.timeLeft -= time
        if (self.IsDone()):
            self._AddOutputs()

        if (self.timeLeft < 0):
            #action was completed and some time was left
            return -self.timeLeft
        return 0

    def IsDone(self):
        return self.timeLeft <= 0

    def _ReserveResourcesAndCreateOutputs(self):
        print "Starting action " + self.name       
        self.started = True

        if not self.possession.HasResources(self.inputs):
            print "Not enough resources to start " + self.name + "! Go home..."
            self.timeLeft = 0
            return

        #create the stuff right away, so that resources are "reserved"
        #Don't give the results to the caller until duraton is passed
        for outputResource in self.outputs:
            createdOutput = ResourceFactory.CreateResource(outputResource, self.possession)
            self.createdOutputs.append(createdOutput)

