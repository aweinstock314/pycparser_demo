#!/usr/bin/env python2
import pycparser.c_ast
import pycparser.c_parser
import copy
import sys

sys.dont_write_bytecode = True #we don't want these .pyc files!

from helper_functions_by_pycparser import *
from our_helper_functions import *

give_small_output=True
ast = pycparser.c_parser.CParser().parse(open("foo.c.preprocessed").read())

#ast.show()

dictify = lambda n: {k:v for k,v in n.children()}
listify = lambda n: [v for _,v in n.children()] if n else []

def access(node, *path):
    tmp = node
    for label in path:
        try:
            tmp = dictify(tmp)[label]
        except KeyError:
            return None
    return tmp

def typetorepr(node, word_size=8,**kwargs):
    ast_of_last_decl=kwargs.get("ast_of_last_decl",None) #get the ast of the last Decl/TypeDecl/Typename
    parent_node=kwargs.get("parent_node",None) #grab a pointer to our parent node
    kwargs["parent_node"]=node #and set ourselves as the parent node

    if isinstance(node, pycparser.c_ast.ArrayDecl):
        ty, sz = typetorepr(node.type, word_size,**kwargs)
        n = int(node.dim.value, 10)
        if (give_small_output):
            return (['array', (ty, sz), n], n*sz)
        else:
            return (['array',
                    {"type":"array", "name":get_name_of_a_node(parent_node) , "type_of_array_element":(ty, sz), "num_of_array_elements:":n, "size":n*sz , "pycparser_ast":copy.deepcopy(node)}],
                    n*sz)
    
    if isinstance(node, pycparser.c_ast.Struct):
        types = []
        size = 0
        for decl in node.decls:
            ty, sz = typetorepr(decl,**kwargs)
            types.append((ty, sz))
            size += sz
        if (give_small_output):
            return (['struct', node.name, types], size)
        else:
            return (['struct',
                    {"type":"struct", "name":node.name,  "size":size,  "struct_elements":types ,"pycparser_ast":copy.deepcopy(node)}], 
                    size)

    if isinstance(node, pycparser.c_ast.PtrDecl):
        if (give_small_output):
            return (['pointer', typetorepr(node.type,**kwargs)], word_size)
        else:
            return (['pointer',
                    {"type":"pointer", "name":get_name_of_a_node(parent_node) , "type_of_pointed_element":typetorepr(node.type,**kwargs), "size":word_size , "pycparser_ast":copy.deepcopy(node)}],
                    word_size)

    if isinstance(node, pycparser.c_ast.IdentifierType):
        assert len(node.names) == 1
        name = node.names[0]
        size = {
            'void': 0,
            'float': 4,
            'double': 8, 
            'int': 4,
            'char': 1,
            }[name]
        return (name, size)

    if isinstance(node, pycparser.c_ast.FuncDecl):
        ty = node.type
        return (['function', [typetorepr(arg,**kwargs) for arg in listify(node.args)], typetorepr(node.type, word_size,**kwargs)], None)
    
    if isinstance(node, (pycparser.c_ast.Decl, pycparser.c_ast.TypeDecl, pycparser.c_ast.Typename)):
        kwargs["ast_of_last_decl"]=node
        return typetorepr(node.type,**kwargs)
    node.show()
    assert False, 'Unhandled type %r %r %r' % (type(node), dictify(node), dir(node))

function_types = dict()

for node in listify(ast):
    if isinstance(node, pycparser.c_ast.Decl):
        function_types[node.name] = typetorepr(node)
        print node.name
        print '\t', typetorepr(node)
    if isinstance(node, pycparser.c_ast.FuncDef):
        function_types[node.decl.name] = typetorepr(node.decl.type)
        print node.decl.name
        print '\t', typetorepr(node.decl.type)

print function_types
