# [1] Getting the descriptions
# [2]Splitting it on \n
# [3] Extracting the first N lines [change with N]
# [4] remove stop words, stemming (common NLP methods)
# [5] add that to the csv
from nltk.stem import PorterStemmer
import csv



def extract(data, writerobj):
    lines = data.split('\n')
    numLines = len(lines)
    print ("there are " + str(numLines) + " lines how many do you want to analyze?")
    n = int(input())
    lines = lines[:n]
    ps = PorterStemmer()
    for line in lines:
        words = line.split()
        for i in range(len(words)):
            words[i] = ps.stem(words[i])
        stemmed_line = " ".join(words)
        writerobj.writerow(words)



def main():
    data = input("ENTER INPUT")
    with open("stemmed_data.csv", 'w') as csvfile:
        writerobj = csv.writer(csvfile)
        extract(data, writerobj)



if __name__ == "__main__":
    main()




