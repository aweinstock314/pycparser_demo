import re
import pycparser
import sys

from helper_functions_by_pycparser import *


#function to print well a dictionary. Thanks https://stackoverflow.com/a/21049038
def wellprint_dict(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print( '%s{' % ((nested_level) * spacing),file=output)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print( '%s%s:' % ((nested_level + 1) * spacing, k),file=output)
                wellprint_dict(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v),file=output)
        print('%s}' % (nested_level * spacing),file=output)
    elif type(obj) == list:
        print( '%s[' % ((nested_level) * spacing),file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                wellprint_dict(v, nested_level + 1, output)
            else:
                print( '%s%s' % ((nested_level + 1) * spacing, v),file=output)
        print( '%s]' % ((nested_level) * spacing),file=output)
    else:
        print( '%s%s' % (nested_level * spacing, obj),file=output)


def get_name_of_a_node(node):
    if isinstance(node, (pycparser.c_ast.Decl,pycparser.c_ast.Typename,pycparser.c_ast.Struct)):
        return node.name
    elif isinstance(node,pycparser.c_ast.TypeDecl):
        return node.declname
    elif isinstance(node, (pycparser.c_ast.ArrayDecl,pycparser.c_ast.PtrDecl)):
        return "" #sometimes the parent does not have a name . Eg pointer to pointer to pointer ...
    else:
        print("ERROR IN NAME")
        if node==None:
            print("node is None!")
        else:
            wellprint_dict(to_dict(node))
        sys.exit(-1)
