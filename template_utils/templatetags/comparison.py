"""
Tags for performing basic value comparisons in templates.
"""
from django import template


from template_utils import comparisons

class ComparisonNode(template.Node):
    def __init__(self, comparison, nodelist_true, nodelist_false, negate, *vars):
        self.vars = map(template.Variable, vars)
        self.comparison = comparison
        self.negate = negate
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        resolve = lambda var: var.resolve(context)
        try:
            if comparisons[self.comparison](
              *[var.resolve(context) for var in self.vars]):
                if self.negate:
                    return self.nodelist_false.render(context)
                return self.nodelist_true.render(context)
        # If either variable fails to resolve, return nothing.
        except template.VariableDoesNotExist:
            return ''
        # If the types don't permit comparison, return nothing.
        except TypeError:
            return ''
        if self.negate:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_comparison(parser, token):
    """
    Compares two values.
    
    Syntax::
    
        {% if_[comparison] [var1] [var2] [var...] [negate] %}
        ...
        {% else %}
        ...
        {% endif_[comparison] %}

    
    Supported comparisons are ``match``, ``find``, ``startswith``, ``endswith``,
    ``less``, ``less_or_equal``, ``greater`` and ``greater_or_equal``.
    
    Examples::
    
        {% if_less some_object.id 3 %}
        <p>{{ some_object }} has an id less than 3.</p>
        {% endif_less %}
        
        {% if_match request.path '^/$' %}
        <p>Welcome home</p>
        {% endif_match %}	    

    """
    negate = False
    bits = token.contents.split()
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    if bits[-1] == 'negate':
        bits = bits[:-1]
        negate = True
    comparison = bits[0].split('if_')[1]
    return ComparisonNode(comparison, nodelist_true, nodelist_false, negate, *bits[1:])

register = template.Library()
for tag_name in comparisons:
    register.tag('if_%s' % tag_name, do_comparison)
