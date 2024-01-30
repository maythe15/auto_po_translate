import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('input', help='PO file to translate')
parser.add_argument('output', help='Where to store new PO file')
parser.add_argument('dictionary', help='Translation dictionary to use')
args=parser.parse_args()

with open(args.input) as pfile:
    file=pfile.readlines()

replacements={}
replacable=[]
with open(args.dictionary) as dfile:
    repl_dict=json.load(dfile)
    for i in repl_dict.keys():
        replacements.update({i:repl_dict[i]})
        replacable.append(i)

for ind, i in enumerate(file):
    if i.startswith('msgstr'):
        message=i.split('"')[1]
        message_parts=message.split(' ')
        for mp, j in enumerate(message_parts):
            if j:
                isCapital=j[0]==j[0].upper()
                if j.lower() in replacable:
                    message_parts[mp]=replacements[j.lower()]
                    if isCapital:
                        message_parts[mp]=message_parts[mp].capitalize()

        file[ind]=f'''msgstr "{' '.join(message_parts)}"
'''

with open(args.output,'w') as f:
    f.write("".join(file))