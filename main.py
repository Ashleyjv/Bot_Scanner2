import zipfile
import os

# bots_filenames = "/Users/ashleyjvarghese/Desktop/bots_filenames.txt"
# fileptr = open(bots_filenames, 'r')
# base_path = "/Users/ashleyjvarghese/Desktop/bots_zip/"


def convert(bots_filenames, base_path, extraction_directory):
    fileptr = open(bots_filenames, 'r')
    paths_to_zip_files = []
    lines = fileptr.readlines()
    for line in lines:
        paths_to_zip_files.append(base_path + line[:-1])

    #creating extraction directory
    # directory = "bots_unzipp"
    # parent_dir = os.getcwd()
    # mode = 0o666
    # path2 = os.path.join(parent_dir, directory)
    # os.mkdir(path2)
    # extraction_directory = path2
    # path_to_unzipped_bots = path2

    # directory_to_extract_to = "/Users/ashleyjvarghese/Desktop/bots_unzup"

    for path in paths_to_zip_files:
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(extraction_directory)
        except:
            continue

    fileptr.close()


direct = "bots_unzipp"
parent_dir = os.getcwd()
path2 = os.path.join(parent_dir, direct)
os.mkdir(path2)

bots_filenames = input("enter full path to text file containing bot filenames")
base_path = input("enter full path to directory containing zipped bot directories")
path_to_unzipped_bots = path2
convert(bots_filenames, base_path, extraction_directory=path_to_unzipped_bots)

# convert(fileptr, base_path)
#
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


# print (r)



for i in r:
    fileptr2.write(i + str(set(r[i])))
    fileptr2.write('\n')
fileptr2.close()

r2 = dict(sorted(r2.items(), key=lambda item: item[1], reverse=True))
print (r2)







