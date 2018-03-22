import re
import pycparser
import sys


def get_name_of_a_node(node):
    if isinstance(node, (pycparser.c_ast.Decl,pycparser.c_ast.Typename,pycparser.c_ast.Struct)):
        return node.name
    elif isinstance(node,pycparser.c_ast.TypeDecl):
        return node.declname
    elif isinstance(node, (pycparser.c_ast.ArrayDecl,pycparser.c_ast.PtrDecl)):
        return "" #sometimes the parent does not have a name . Eg pointer to pointer to pointer ...
    else:
        print("ERROR IN NAME")
        print(to_dict(node))
        sys.exit(-1)
