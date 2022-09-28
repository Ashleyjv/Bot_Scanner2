import zipfile
import os
from os import listdir
from os.path import isfile, join

DATA_OUTPUT = "bots_unzipp"
DATA_INPUT = "data"
PARENT_DIR = os.getcwd()
UNZIP_DIRECTORY = os.path.join(PARENT_DIR, DATA_OUTPUT)


try:
    os.mkdir(path_to_unzipped_bots)
    print("Making bots_unzipp directory")
except:
    print("Bots_unzipp exists")


def unzip_all( base_path, extraction_directory):
    # extract all zipped file names
    onlyfiles = ["{}/{}".format(base_path,f) for f in listdir(base_path) if isfile(join(base_path, f))]
    
    #unzip
    for path in onlyfiles:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(extraction_directory)
 


unzip_all(data_input, extraction_directory=UNZIP_DIRECTORY)



def read_py(directory):
    r = []
    # for i in os.walk(directory):
    #     print (i)
    # op = open('repoImports', 'w')
    import_Map = {}
    map = {}
    for i in os.listdir(directory):
        map[directory + '/' + i] = []
    # print (map)
    map2 = {}
    for root, dirs, files in os.walk(directory):
        last_occu = root.rfind('/')
        root_valu = -1
        root_Orig = root
        if (root[last_occu - 11: last_occu] != 'bots_unzipp'):
            test1index = root.find('bots_unzipp')
            end_Index = root[test1index + 12:].find('/')
            root_valu = root[:end_Index + test1index + 12]
            if root_valu not in map:
                map[root_valu] = []
                map2[root_valu] = []
        else:
            map[root] = []
            map2[root] = []
        flag = False
        for name in files:
            if name[-3:] == '.py':
                flag = True
                fileptr = open(root_Orig + '/' + name, 'r')
                lines = fileptr.readlines()
                final_imports = []
                for line in lines:
                    if line[:4] == 'from' or line[:6] == 'import':
                        # # processing
                        arra = line.split()
                        for i in arra:
                            if i != 'as' and i != 'from' and i != 'import':
                                temp = i
                                if i[-1] == ',':
                                    temp = i[:-1]
                                    final_imports.append(temp)
                                else:
                                    final_imports.append(temp)
                                if temp not in import_Map:
                                    import_Map[temp] = 1
                                else:
                                    import_Map[temp] = import_Map[temp] + 1




                # print (final_imports)
                if root_valu != -1:
                    map2[root_valu] += (final_imports)
                else:
                    map2[root] += (final_imports)
                        # if line[:-1] not in import_Map:
                        #     import_Map[line[:-1]] = 1
                        # else:
                        #     import_Map[line[:-1]] = import_Map[line[:-1]] + 1
                if root_valu != -1:
                    map[root_valu] += (name)

                else:
                    map[root] += (name)
        if flag == False:
            continue
            # print ('flaq')
            # print (root, root_valu)
            # r.append(os.path.join(root, name))

    fileptr.close()
    return map2, import_Map
    # return r

directory = path_to_unzipped_bots
# print (directory)
r = read_py(directory)
fileptr2 = open('imports.txt', 'w')
r, r2 = r[0], r[1]


#CLEANUP
onlyfiles = ["{}/{}".format(path2,f) for f in listdir(path2) if isfile(join(path2, f))]
for directory in onlyfiles:
    print(directory)
    os.rmdir(directory)

# print (r)



for i in r:
    fileptr2.write(i + str(set(r[i])))
    fileptr2.write('\n')
fileptr2.close()

r2 = dict(sorted(r2.items(), key=lambda item: item[1], reverse=True))
print(r2)







