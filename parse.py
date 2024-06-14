#!/usr/bin/python3


import sys
import json
import re


data = ""
file2parse = "trace.log"
output = "t.log"
if len(sys.argv) > 1:
    file2parse = sys.argv[1]


with open(file2parse, "r") as file:
    for line in file.readlines():
        if not "send" in line:
            continue

        i = 0
        j = len(line) - 1
    
        while i < len(line) and line[i] != '(':
            i += 1    
        
        while j > 0 and line[j] != ')':
            j -= 1

        if i == len(line) or j == 0:
            continue

        parse = line[i+1:j]
        parse = processed = re.sub(r'(?<![\\\w])([a-zA-Z_\d]+[\(\<\]*\d*\)?[\|a-zA-Z_]*)', r'"\1"', parse.replace('\n', '')).replace('\\', '\\\\').replace('=', ':').replace('"true"', 'true').replace('"false"', 'false')
        parse = "[" + parse + "]"
        data = json.loads(parse)
        print(data)


with open(output, "w+") as file:
    json.dump(data, file, indent=True)



            


