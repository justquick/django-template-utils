import re
from shlex import split
from django.utils.importlib import import_module
from django import template
from django.conf import settings

from template_utils import functions

def import_function(s):
    """
    Import a function given the string formatted as
    `module_name.function_name`  (eg `django.utils.text.capfirst`)
    """
    a = s.split('.')
    j = lambda x: '.'.join(x)
    return getattr(import_module(j(a[:-1])), a[-1])

class FunctionalNode(template.Node):
    def __init__(self, func, varname=None, *args, **kwargs):
        self.func = func
        self.args = map(template.Variable, args)
        self.kwargs = dict([(k,template.Variable(v)) for k,v in kwargs.items()])
        self.varname = varname
    
    def render(self, context):
        def lookup(var):
            try:
                return var.resolve(context)
            except template.VariableDoesNotExist:
                return unicode(var)
       
        args = map(lookup, self.args)
        func = functions[self.func]
       
        if isinstance(func, basestring):
            func = import_function(func)
        if hasattr(func,'takes_context') and getattr(func,'takes_context'):
            args = [context] + args
            
        result = func( *args, **dict([(k, lookup(v)) \
            for k,v in self.kwargs.items()]))     
        if self.varname:
            context[self.varname] = result
            return ''
        return result
        
def do_function(parser, token):
    """
    Compares two values.
    
    Syntax::
    
        {% [function] [var args...] [name=value kwargs...] [as varname] %}

    Examples::
    
        {% listdir '.' colors=True %}	    

    """
    varname = None
    bits = split(' '.join(token.contents.split()))
    if len(bits)>2:
        if bits[-2] == 'as':
            varname = bits[-1]
            bits = bits[:-2]
    kwarg_re = re.compile('^[A-z]\w+\=')
    kwargs = {}
    for n,bit in enumerate(bits):
        if kwarg_re.match(bit):
            del bits[n]
            kwargs[bit.split('=')[0]] = bit[bit.index('=')+1:]
    return FunctionalNode(bits[0], varname, *bits[1:], **kwargs)
    
register = template.Library()
for tag_name in functions:
    register.tag(tag_name, do_function)