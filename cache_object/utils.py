from cache_object.loading import Cache

class CacheLibrary(object):

    def __init__(self, cache):
        assert issubclass(cache.__class__, Cache)
        self.cache = cache

    def validate(self, object):
        return True

    def register_function(self, func, name = None):
        if self.validate(func):
            if name is None:
                fname = func.__name__
            else:
                fname = name
            self.cache.add_object(func, fname)
        return func

    def register(self, name = None, filter_func = None):
        if name == None and filter_func == None:
            # @register()
            return self.register_function
        elif filter_func == None:
            if(callable(name)):
                # @register
                return self.register_function(name)
            else:
                # @register('somename') or @register(name='somename')
                def dec(func):
                    return self.register(name, func)
                return dec
        elif name != None and filter_func != None:
            # register('somename', somefunc)
            return self.register_function(filter_func, name)
        else:
            raise AttributeError('Invalid')
