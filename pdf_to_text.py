from tika import parser
import os

def main():
    filepaths = traverse_txt_files(os.path.dirname(os.path.realpath(__file__)))
    for path in filepaths:
        print(path)
        parse_paths(path)

def traverse_txt_files(directory):
    files = []
    for r, d, f in os.walk(directory):
        for file in f:
            if file.endswith(".pdf"):
                files.append(os.path.join(r,file))
    return files

def parse_paths(filepath):
    pdf_contents = parser.from_file(filepath)
    title = filepath.rsplit('\\',1)[-1]
    writePath = os.getcwd()+"\\txtfiles\\"+title+".txt"
    with open(writePath, 'w', encoding='utf-8') as txt_file:
        txt_file.write(pdf_contents['content'])


main()