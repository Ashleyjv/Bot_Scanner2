import zipfile
import os
from os import listdir
from os.path import isfile, join, isdir
from glob import glob
import ast
from collections import namedtuple
import csv
import shutil

Import = namedtuple("Import", ["module", "name", "alias"])
DATA_OUTPUT = "bots_unzipp"
DATA_INPUT="/Users/arjunarunasalam/Desktop/GithubCrawler/data2"
PARENT_DIR = os.getcwd()
UNZIP_DIRECTORY = os.path.join(PARENT_DIR, DATA_OUTPUT)


try:
    os.mkdir(path_to_unzipped_bots)
    print("Making bots_unzipp directory")
except:
    print("Bots_unzipp already exists exists")

#deletes all subdirs within a directory (arg 1)
def cleanup(directory):
    onlyfolders= ["{}/{}".format(directory,f) for f in listdir(directory) if isdir(join(directory, f))]
    for dir_to_delete in onlyfolders:
        shutil.rmtree(dir_to_delete)

# Accepts a path as an argument and returns the import statements within said part 
def get_imports(path):
    with open(path) as fh:        
       root = ast.parse(fh.read(), path)
    #print(path)
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):  
            if not node.module:
                module = "."
                continue
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)

# Accepts a path as an argument and returns all python files within that path's directoroy
def return_all_python_files(directory):
    result = [y for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.py'))]
    return result

#Accepts a list of python file paths and returns a set of all imported libraries/modules
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

#Accepts a src (argument 1) of zipped files to produce unzipped folders within dst (argument 2)
def unzip_all( base_path, extraction_directory):
    # extract all zipped file names
    onlyfiles = ["{}/{}".format(base_path,f) for f in listdir(base_path) if isfile(join(base_path, f))]
    
    #unzip
    for path in onlyfiles:
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(extraction_directory)
            print("Unzipping", path)
        except:
            print("Error unzipping", path)
 
#
def generate_import_report(directory):
    global_map = {}
    for path in os.listdir(directory):
        full_path = os.path.join(directory,path)
        if not os.path.isdir(full_path):
            continue

        print("Extracting imports from:",full_path)

        pythonFiles = return_all_python_files(full_path)
        if not pythonFiles:
            continue
        #print(pythonFiles)
        try:
            imports = extract_all_imports(pythonFiles)
        except:
            print("Error extracting modules from", path)
            continue

        for module in imports: 
            if module in global_map:
                global_map[module] +=1
            else:
                global_map[module] = 1 

    return global_map

#accepts a sorted dictionary to a csv
def write_module_csv(filename,sorted_dict):
    with open(filename, 'w') as f:  # You will need 'wb' mode in Python 2.x
        w = csv.DictWriter(f, ['module_name','repo count'])
        w.writeheader()
        for key in sorted_dict:
            w.writerow({'module_name':key,'repo count':sorted_dict[key]})
    
#accepts a dictionary of modules/submodules and returns sorted count with respect to modules only 
#ex, selenium.x and selenium y are all under selenium
def remove_sub_modules(sorted_dictionary):
    new_dictionary = {}
    for key in sorted_dictionary:

        modified_key = key.split(".")[0]

        if modified_key not in new_dictionary:
            new_dictionary[modified_key] = 1
        else: 
            new_dictionary[modified_key] += 1 

    dict(sorted(new_dictionary.items(), key=lambda item: item[1], reverse=True))

    return new_dictionary


def main():

    unzip_all(DATA_INPUT, extraction_directory=UNZIP_DIRECTORY)

    global_map = generate_import_report(UNZIP_DIRECTORY)

    sorted_global_map = dict(sorted(global_map.items(), key=lambda item: item[1], reverse=True))

    write_module_csv('module_sorted_by_count.csv', sorted_global_map)

    global_map_submodule_removed  = remove_sub_modules(sorted_global_map)

    write_module_csv('modules_only(nosubmodules)_sorted_by_count.csv', global_map_submodule_removed)

    cleanup(UNZIP_DIRECTORY)


main()







