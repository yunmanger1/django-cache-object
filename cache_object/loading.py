from django.utils.datastructures import SortedDict
from django.db.models import loading
import threading
from django.conf import settings
from django.utils.importlib import import_module
from common import logwrapper
log = logwrapper.defaultLogger(__file__)

class CacheContainer(object):

    global_store = {}

def get_state(key):
    try:
        return CacheContainer.global_store[key]
    except KeyError:
        state = dict(
            # Keys of app_store are the model modules for each application.
            object_store = SortedDict(),

            # -- Everything below here is only used when populating the cache --
            loaded = False,
            write_lock = threading.RLock(),
        )
        CacheContainer.global_store[key] = state
        return state


class Cache(object):
    """
    A cache that stores installed applications and their models. Used to
    provide reverse-relations and for app introspection (e.g. admin).
    """

    def __init__(self, key, module_name = None, app_list = settings.INSTALLED_APPS):
        self.__dict__ = get_state(key)
        self.module_name = module_name
        self.app_list = app_list

    def __contains__(self, key):
        self._populate()
        return key in self.object_store

    def _populate(self):
        """
        Fill in all the cache information. This method is threadsafe, in the
        sense that every caller will see the same state upon return, and if the
        cache is already initialised, it does no work.
        """
        if self.loaded or self.module_name is None:
            return
        self.write_lock.acquire()
        try:
            if self.loaded:
                return
            loading.cache._populate()
            for app_label in self.app_list:
                try:
                    import_module('.{0}'.format(self.module_name), app_label)
                except ImportError:
                    pass
            self.loaded = True
        finally:
            self.write_lock.release()

    def add_object(self, object, name):
        self.object_store[name] = object

    def get_object(self, name):
        self._populate()
        return self.object_store[name]
