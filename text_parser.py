from collections import Counter
from tempfile import NamedTemporaryFile
import shutil
import csv 
import os

character_count = 0


def main():
    #creating file incase it doesn't exist
    with open("output.csv","w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["pair","count"])
        f.close()
    filepaths = traverse_txt_files(os.path.dirname(os.path.realpath(__file__)))
    for path in filepaths:
        parse_file(path)
    print(str(character_count)+" characters parsed")

def traverse_txt_files(directory):
    files = []
    for r, d, f in os.walk(directory):
        for file in f:
            if file.endswith(".txt"):
                files.append(os.path.join(r,file))
    return files

def parse_file(filepath):
    global character_count
    file = open(filepath,"r", encoding='utf-8')
    text = file.read()
    text = text.lower() #all text lowercase
    text = "".join(text.splitlines()) #remove new line characters
    text = "".join(e for e in text if e.isalnum()) #remove all punctuation ex: !@#$%^&**(){}[] etc.
    text = "".join(e for e in text if not e.isdigit()) #remove all numerals
    text = "".join(i for i in text if ord(i)<128) #removing unkown characters, non english chars
    character_count = character_count+len(text)
    out = get_pairs(list(text))
    print(filepath)
    write_to_data(out)

def get_pairs(txt):
    pairs = []
    i=0
    while i < len(txt):
        p = i+1
        if(i == len(txt)-1):
            return dict(Counter(pairs))
        else:
            pairs.append(txt[i]+txt[p])
            i+=1


def write_to_data(data):
    filename = "output.csv"
    fields = ("pair","count")
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')
    d = data
    if not d:
        print("We hit a blank file")
        return
    with open(filename, 'r', newline='') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['pair'] in d.keys():
                #print("pair is in set, updating",row['pair'])
                row['count'] = int(row['count'])+d.get(row['pair'])
                del d[row['pair']]
            writer.writerow(row)
        for pair, count in d.items():
            #print("pair is not in set, updating",row['pair'])
            row = {}
            row['pair'] = pair
            row['count'] = count
            writer.writerow(row)

    shutil.move(tempfile.name, filename)
    
main()