
class TemplateRegistry(dict):
    
    def register(self, name, func):
        self[name] = func
        
    def unregister(self, name):
        del self[name]
        
comparisons = TemplateRegistry()
functions = TemplateRegistry()


comparisons.register('less', lambda x,y: x < y)
comparisons.register('less_or_equal', lambda x,y: x <= y)
comparisons.register('greater_or_equal', lambda x,y: x >= y)
comparisons.register('greater', lambda x,y: x > y)
    

comparisons.register('startswith', lambda x,y: x.startswith(y))
comparisons.register('endswith', lambda x,y: x.endswith(y))
comparisons.register('contains', lambda x,y: x.find(y) >- 1)
comparisons.register('matches', lambda x,y: re.compile(y).match(x))
comparisons.register('divisible_by', lambda x,y: x % y == 0)
comparisons.register('subset', lambda x,y: set(x) <= set(y))
comparisons.register('superset', lambda x,y: set(x) >= set(y))



def pygmentize(code,lexer='python'):
    from pygments import highlight
    from pygments import lexers
    from pygments.formatters import HtmlFormatter
    format = HtmlFormatter()
    return '<style>%s</style>%s' % (format.get_style_defs('.highlight') ,
        highlight(code, getattr(lexers, '%sLexer' % lexer.title())(), format))

def arg_test(*args,**kwargs):
    return '<pre>\nA: %s\nKW: %s</pre>' %(args,kwargs)

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

functions.register('pygmentize', pygmentize)
functions.register('args', arg_test)
functions.register('set', do_set)
functions.register('del', do_del)
functions.register('capfirst','django.utils.text.capfirst')
functions.register('dump','django.core.serializers.serialize')