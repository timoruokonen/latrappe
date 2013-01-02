
'''
Resource factory. All resources should be created through this factory class! Has a static method for
creating resources. When a resource is created, all the possible input resources are reduced from the
possession instance of the entity that is creating a new resource.
'''
class ResourceFactory(object):
    resource_created_subscribers = []
    resource_destroyed_subscribers = []

    def __init__(self):
        pass

    @staticmethod
    def create_resource(target, possession):
        copy_possession = possession
        for resource in target.materials:
            found = False
            for pos_resource in possession.resources:
                if (isinstance(resource, type(pos_resource))):
                    possession.destroy_resource(pos_resource)
                    found = True
                    break;
            if not found:
                raise Exception("Could not create " + str(target) + ", not enough resources!!")
        print "New " + str(target) + " was created!"
        created_resource = target()
        ResourceFactory.on_resource_created(created_resource)
        return created_resource

    @staticmethod
    def destroy_resource(resource):
        ResourceFactory.on_resource_destroyed(resource)

    @staticmethod
    def on_resource_created(resource):
        for subscriber in ResourceFactory.resource_created_subscribers:
            subscriber.on_resource_created(resource)
    
    @staticmethod
    def on_resource_destroyed(resource):
        for subscriber in ResourceFactory.resource_destroyed_subscribers:
            subscriber.on_resource_destroyed(resource)

