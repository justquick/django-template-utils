from django.conf import settings
from django.template import add_to_builtins
from django.utils.importlib import import_module

    
class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class TemplateRegistry(dict):
    """
    A simple dictionary with register and unregister functions
    """
    def register(self, name_or_func, func=None):
        """
        Add a function to the registry by name
        """
        if func is None and hasattr(name_or_func, '__name__'):
            name = name_or_func.__name__
            func = name_or_func
        elif func:
            name = name_or_func

        if name in self:
            raise AlreadyRegistered('This function %s is already registered' % name)
            
        self[name] = func
        
    def unregister(self, name):
        """
        Remove the function from the registry by name
        """
        if not name in self:
            raise NotRegistered('This function %s is not registered' % name)
        del self[name]
        
comparisons, functions, filters, blocks = TemplateRegistry(), TemplateRegistry(), TemplateRegistry(), TemplateRegistry()

more_builtins = getattr(settings, 'DEFAULT_BUILTIN_TAGS', ())
if more_builtins:
    map(add_to_builtins, more_builtins)

for app_name in settings.INSTALLED_APPS:
    try:
        mod = import_module('.template', app_name)
    except ImportError:
        continue
    for name in dir(mod):
        obj = getattr(mod, name)
        if callable(obj):
            if hasattr(obj, 'block'):
                if hasattr(obj, 'name'):
                    blocks.register(getattr(obj, 'name'), obj)
                else:
                    blocks.register(obj)
            if hasattr(obj, 'function'):
                if hasattr(obj, 'name'):
                    functions.register(getattr(obj, 'name'), obj)
                else:
                    functions.register(obj)
            if hasattr(obj, 'comparison'):
                if hasattr(obj, 'name'):
                    comparisons.register(getattr(obj, 'name'), obj)
                else:
                    comparisons.register(obj)
            if hasattr(obj, 'filter'):
                if hasattr(obj, 'name'):
                    filters.register(getattr(obj, 'name'), obj)
                else:
                    filters.register(obj)
