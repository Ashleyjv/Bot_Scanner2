import os
from glob import glob
import ast
from collections import namedtuple

Import = namedtuple("Import", ["module", "name", "alias"])

def get_imports(path):
    with open(path) as fh:        
       root = ast.parse(fh.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
            #print(node.module)
        elif isinstance(node, ast.ImportFrom):  
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)

def return_all_python_files(directory):
	result = [y for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.py'))]
	return result


def extract_all_imports(pythonFileList):	
	importSet = set()
	for file in pythonFileList:
		imports = get_imports(file)
		for val in imports:
			if val.module:
				importSet.add(".".join(val.module))
			else:
				importSet.add(".".join(val.name))
	return importSet


def main():
	pythonFiles = return_all_python_files('test-dir')
	imports = extract_all_imports(pythonFiles)
	print(imports)

main()
