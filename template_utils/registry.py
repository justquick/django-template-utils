import re
from django.conf import settings
from django.template import add_to_builtins
try:
    set
except:
    from sets import Set as set

map(add_to_builtins, getattr(settings, 'DEFAULT_BUILTIN_TAGS', ()))

class TemplateRegistry(dict):
    
    def register(self, name, func):
        self[name] = func
        
    def unregister(self, name):
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



def do_set(context,**kwargs):
    """
    Updates the context with the keyword arguments
    """
    context.update(kwargs)
    return ''
do_set.takes_context = True

def do_del(context,*args):
    """
    Deletes template variables from the context
    """
    for name in args:
        del context[name]
    return ''
do_del.takes_context = True

functions.register('set', do_set)
functions.register('del', do_del)
functions.register('serialize','django.core.serializers.serialize')