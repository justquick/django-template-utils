"""
Tags for performing basic value comparisons in templates.
"""
from django import template


from template_utils import blocks

class BlockNode(template.Node):
    def __init__(self, name, nodelist, varname, *vars):
        self.name = name
        self.vars = map(template.Variable, vars)
        self.nodelist = nodelist
        self.varname = varname
    
    def render(self, context):
        result = blocks[self.name](context, self.nodelist, *self.vars)
        if self.varname:
            context[self.varname] = result
            return ''
        return result

def do_block(parser, token):
    bits = token.contents.split()
    nodelist = parser.parse(('end%s' % bits[0],))
    parser.delete_first_token()
    varname = None
    if len(bits) > 2 and bits[-2] == 'as':
        varname = bits[-1]
        bits = bits[:-2]
    return BlockNode(bits[0], nodelist, varname, *bits[1:])

register = template.Library()
for tag_name in blocks:
    register.tag(tag_name, do_block)
