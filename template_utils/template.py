import re
try:
    set
except:
    from sets import Set as set
from django.conf import settings


# Standard builtins for compat
def less(x,y):
    'True if x is less than y'
    return x < y
less.comparison = 1

def less_or_equal(x,y):
    'True if x is less than or equal to y'
    return x <= y
less_or_equal.comparison = 1

def greater_or_equal(x,y):
    'True if x is greater than or equal to y'
    return x >= y
greater_or_equal.comparison = 1

def greater(x,y):
    'True if x is greater than y'
    return x > y
greater.comparison = 1
    
    
# Some extras that are kinda handy
def startswith(x,y):
    'String comparison. True if x startswith y'
    return x.startswith(y)
startswith.comparison = 1

def endswith(x,y):
    'String comparison. True if x endswith y'
    return x.endswith(y)
endswith.comparison = 1

def contains(x,y):
    'String comparison. True if x contains y anywhere'
    return x.find(y) > -1
contains.comparison = 1

def matches(x,y):
    'String comparison. True if string x matches regex y'
    return re.compile(y).match(x)
matches.comparison = 1

def subset(x,y):
    'Set comparison. True if x is a subset of y'
    return set(x) <= set(y)
subset.comparison = 1

def superset(x,y):
    'Set comparison. True if x is a superset of y'
    return set(x) >= set(y)
superset.comparison = 1

def divisible_by(x,y):
    'Numeric comparison. True if x is divisible by y'
    return float(x) % float(y) == 0
divisible_by.comparison = 1

def setting(x):
    'True if setting x is defined in your settings'
    return hasattr(settings, x)
setting.comparison = 1


# Any templatetag can be named
def do_set(context, **kwargs):
    'Updates the context with the keyword arguments'
    context.update(kwargs)
    return ''
do_set.function = 1
do_set.takes_context = 1
do_set.name = 'set'

def do_del(context, *args):
    'Deletes template variables from the context'
    for name in args:
        del context[name]
    return ''
do_del.function = 1
do_del.takes_context = 1
do_del.do_not_resolve = 1
do_del.name = 'del'

# Functions can be imported from elsewhere
from django.core.serializers import serialize
serialize.function = 1

# Functions can be filters too
def md5(value):
    'Returns MD5 hexadecimal hash of value'
    from django.utils.hashcompat import md5_constructor
    return md5_constructor(value).hexdigest()
md5.filter = 1
md5.function = 1

def sha1(value):
    'Returns SHA1 hexadecimal hash of value'
    from django.utils.hashcompat import sha_constructor
    return sha_constructor(value).hexdigest()
sha1.filter = 1
sha1.function = 1