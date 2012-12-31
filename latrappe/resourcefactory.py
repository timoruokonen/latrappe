
'''
Resource factory. All resources should be created through this factory class! Has a static method for
creating resources. When a resource is created, all the possible input resources are reduced from the
possession instance of the entity that is creating a new resource.
'''
class ResourceFactory(object):
    resourceCreatedSubscribers = []
    resourceDestroyedSubscribers = []

    def __init__(self):
        pass

    @staticmethod
    def CreateResource(target, possession):
        copyPossession = possession
        for resource in target.materials:
            found = False
            for posResource in possession.resources:
                if (isinstance(resource, type(posResource))):
                    possession.DestroyResource(posResource)
                    found = True
                    break;
            if not found:
                raise Exception("Could not create " + str(target) + ", not enough resources!!")
        print "New " + str(target) + " was created!"
        createdResource = target()
        ResourceFactory.OnResourceCreated(createdResource)
        return createdResource

    @staticmethod
    def DestroyResource(resource):
        ResourceFactory.OnResourceDestroyed(resource)

    @staticmethod
    def OnResourceCreated(resource):
        for subscriber in ResourceFactory.resourceCreatedSubscribers:
            subscriber.OnResourceCreated(resource)
    
    @staticmethod
    def OnResourceDestroyed(resource):
        for subscriber in ResourceFactory.resourceDestroyedSubscribers:
            subscriber.OnResourceDestroyed(resource)

