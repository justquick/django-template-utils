import re
from django.conf import settings
from django.template import add_to_builtins
try:
    set
except:
    from sets import Set as set

more_builtins = getattr(settings, 'DEFAULT_BUILTIN_TAGS', ())
if more_builtins:
    map(add_to_builtins, more_builtins)

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
        
comparisons, functions = TemplateRegistry(), TemplateRegistry()

# Standard builtins for compat
comparisons.register('less', lambda x,y: x < y)
comparisons.register('less_or_equal', lambda x,y: x <= y)
comparisons.register('greater_or_equal', lambda x,y: x >= y)
comparisons.register('greater', lambda x,y: x > y)
    
# Some extras that are kinda handy
comparisons.register('startswith', lambda x,y: x.startswith(y))
comparisons.register('endswith', lambda x,y: x.endswith(y))
comparisons.register('contains', lambda x,y: x.find(y) > -1)
comparisons.register('matches', lambda x,y: re.compile(y).match(x))
comparisons.register('subset', lambda x,y: set(x) <= set(y))
comparisons.register('superset', lambda x,y: set(x) >= set(y))
comparisons.register('divisible_by', lambda x,y: float(x) % float(y) == 0)
comparisons.register('setting', lambda x: hasattr(settings, x) and getattr(settings, x))

def do_set(context, **kwargs):
    """
    Updates the context with the keyword arguments
    """
    context.update(kwargs)
    return ''
do_set.takes_context = True

def do_del(context, *args):
    """
    Deletes template variables from the context
    """
    for name in args:
        del context[name]
    return ''
do_del.takes_context = True
do_del.do_not_resolve = True

functions.register('set', do_set)
functions.register('del', do_del)
functions.register('serialize','django.core.serializers.serialize')