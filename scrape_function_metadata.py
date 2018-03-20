#!/usr/bin/env python2
import pycparser.c_ast
import pycparser.c_parser
import copy

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

def typetorepr(node, word_size=8):
    if isinstance(node, pycparser.c_ast.ArrayDecl):
        ty, sz = typetorepr(node.type, word_size)
        n = int(node.dim.value, 10)
        if (give_small_output):
            return (['array', (ty, sz), n], n*sz)
        else:
            return (['array',
                    {"type":"array", "name":node.type.declname , "type_of_array_element":(ty, sz), "num_of_array_elements:":n, "size":n*sz , "pycparser_ast":copy.deepcopy(node)}],
                    n*sz)
    if isinstance(node, pycparser.c_ast.Struct):
        types = []
        size = 0
        for decl in node.decls:
            ty, sz = typetorepr(decl)
            types.append((ty, sz))
            size += sz
        if (give_small_output):
            return (['struct', node.name, types], size)
        else:
            return (['struct',
                    {"type":"struct", "name":node.name,  "size":size,  "struct_elements":types ,"pycparser_ast":copy.deepcopy(node)}], 
                    size)
    if isinstance(node, pycparser.c_ast.PtrDecl):
        return (['pointer', typetorepr(node.type)], word_size)
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
        return (['function', [typetorepr(arg) for arg in listify(node.args)], typetorepr(node.type, word_size)], None)
    if isinstance(node, (pycparser.c_ast.Decl, pycparser.c_ast.TypeDecl, pycparser.c_ast.Typename)):
        return typetorepr(node.type)
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
