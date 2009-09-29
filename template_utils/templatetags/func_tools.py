import re
from shlex import split
from django.utils.importlib import import_module
from django import template
from django.conf import settings
from django.template.loader import get_template
from django.template.context import Context
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
        self.args = args
        self.kwargs = kwargs
        self.varname = varname
    
    def render(self, context):
        def lookup(var, resolve=True):
            if resolve:
                var = template.Variable(var)
                try:
                    return var.resolve(context)
                except template.VariableDoesNotExist:
                    return unicode(var)
            return unicode(var)
       
        func = functions[self.func]
        resolve = not (hasattr(func, 'do_not_resolve') and getattr(func, 'do_not_resolve'))
        args = [lookup(var, resolve) for var in self.args]
        kwargs = dict([(k, lookup(var, resolve)) for k,var in self.kwargs.items()])
        if isinstance(func, basestring):
            func = import_function(func)
        if hasattr(func,'takes_context') and getattr(func, 'takes_context'):
            args = [context] + args
        if hasattr(func, 'is_inclusion') and getattr(func, 'is_inclusion'):
            template_name,ctx = func(*args, **kwargs)
            if not isinstance(ctx, Context):
                ctx = Context(ctx)
            result = get_template(template_name).render(ctx)
        else:
            result = func(*args, **kwargs)
        if self.varname:
            context[self.varname] = result
            return ''
        return result
    
        
def do_function(parser, token):
    """
    Performs a defined function an either outputs results, or stores results in template variable
    
    Syntax::
    
        {% [function] [var args...] [name=value kwargs...] [as varname] %}

    Examples::
    
        {% listdir '.' colors=True %}	    

    """
    varname = None
    bits = [filter(lambda x: x != '\x00', token) for token in split(' '.join(token.contents.split()))]
    if len(bits) > 2 and bits[-2] == 'as':
        varname = bits[-1]
        bits = bits[:-2]
    kwarg_re = re.compile(r'(^[A-z]+)\=(.+)')
    args, kwargs = (),{}
    for bit in bits[1:]:
        match = kwarg_re.match(bit)
        if match:
            kwargs[match.group(1)] = match.group(2)
        else:
            args += (bit,)
    return FunctionalNode(bits[0], varname, *args, **kwargs)


register = template.Library()
for tag_name in functions:
    register.tag(tag_name, do_function)