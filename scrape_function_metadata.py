#!/usr/bin/env python3
import pycparser.c_ast
import pycparser.c_parser
import copy
import sys

sys.dont_write_bytecode = True #we don't want these .pyc files!

from helper_functions_by_pycparser import *
from our_helper_functions import *

give_small_output=True

if len(sys.argv)!=2:
    print("Usage: "+sys.argv[0]+" <c_program_to_parse>")
    sys.exit(-1)

ast = pycparser.c_parser.CParser().parse(open(sys.argv[1]).read())

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
    ast_of_last_decl_init=kwargs.get("ast_of_last_decl_init",None) #get the ast of the last Decl init block
    parent_node=kwargs.get("parent_node",None) #grab a pointer to our parent node

    kwargs["parent_node"]=node #set ourselves as the parent node
    
    if (isinstance(node,pycparser.c_ast.TypeDecl) #NOT A GOOD WAY to check, we need to do something better than this
        and isinstance(node.type,pycparser.c_ast.IdentifierType)):
        #the idea here is that we need to transfer the init block from the last Decl. We should cancel what we got for our children, EXCEPT if we are a TypeDecl (and followed by an Identifier)
        pass    
    else:
        kwargs["ast_of_last_decl_init"]=None # cancel the last decl init

    if isinstance(node, pycparser.c_ast.ArrayDecl):
        ty, sz = typetorepr(node.type, word_size,**kwargs)
        n = int(node.dim.value, 10)
        if (give_small_output):
            return (['array', (ty, sz), n], n*sz)
        else:
            return (['array',
                    {"type":"array", "name":get_name_of_a_node(parent_node) , "type_of_array_element":(ty, sz), "num_of_array_elements:":n, "size":n*sz , "init":ast_of_last_decl_init,"pycparser_ast":copy.deepcopy(node)}],
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
                    {"type":"pointer", "name":get_name_of_a_node(parent_node) , "type_of_pointed_element":typetorepr(node.type,**kwargs), "size":word_size , "init":ast_of_last_decl_init, "pycparser_ast":copy.deepcopy(node)}],
                    word_size)

    if isinstance(node, pycparser.c_ast.IdentifierType):
        assert len(node.names) == 1
        name = node.names[0]
        size = {
            'void': 0,
            'float': 4,
            'double': 8,
            'long':8, 
            'int': 4,
            'char': 1,
            }[name]
        if (give_small_output):
            return (name, size)
        else:
            return ([name,
                    {"type":name, "size":size , "init":ast_of_last_decl_init, "pycparser_ast":copy.deepcopy(node)}],
                    size)

    if isinstance(node, pycparser.c_ast.FuncDecl):
        ty = node.type
        return_value_parse=typetorepr(node.type, word_size,**kwargs)
        list_with_arguments_parse=[typetorepr(arg,**kwargs) for arg in listify(node.args)]
        if (give_small_output):
            return (['function',list_with_arguments_parse , return_value_parse], None)
        else:
            return (['function decl',
                    {"type":"function decl", "name":get_name_of_a_node(parent_node) , "list_of_arguments":list_with_arguments_parse, "return_value":return_value_parse , "pycparser_ast":copy.deepcopy(node)}],
                    None)
        
    if isinstance(node, (pycparser.c_ast.Decl, pycparser.c_ast.TypeDecl, pycparser.c_ast.Typename)):
        kwargs["ast_of_last_decl"]=node
        if isinstance(node, (pycparser.c_ast.Decl)):
            kwargs["ast_of_last_decl_init"]=copy.deepcopy(node.init)
        retval=typetorepr(node.type,**kwargs)
        if isinstance(node, (pycparser.c_ast.Decl)):
            decls_to_gather.append(retval)
        return retval
    
    node.show()
    assert False, 'Unhandled type %r %r %r' % (type(node), dictify(node), dir(node))

function_types = dict()
global_decls=[]
kwargs=dict()
decls_to_gather=[]

for node in listify(ast):
    kwargs["parent_node"]=node
    if isinstance(node, pycparser.c_ast.Decl):
        global_decls.append(typetorepr(node,**kwargs))
        print (node.name)
        print ('\t', typetorepr(node,**kwargs))
    if isinstance(node, pycparser.c_ast.FuncDef):
        name_of_fun=node.decl.name
        decls_to_gather=[]
        local_vars=[typetorepr(local,**kwargs) for local in node.body.block_items if isinstance(local, (pycparser.c_ast.Decl))]
        function_types[name_of_fun] = {"fun_decl":typetorepr(node.decl,**kwargs), "fun_locals":local_vars }
        print(name_of_fun)
        print ('\t', function_types[name_of_fun])

print("FUNCTIONS:")
print(function_types)
print("GLOBAL DECLS:")
print(global_decls)
