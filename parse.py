#!/usr/bin/python3


import sys
import json
import re


data = []
debug = False
file2parse = "trace.log"
output = "t.json"

if '-d' in sys.argv:
    debug = True

with open(file2parse, "r") as file:
    for line in file.readlines():
        if not "send" in line and not "recv" in line:
            continue

        send_check = "send" in line
        msg = "send" if send_check else "recv"

        i = 0
        j = len(line) - 1
    
        while i < len(line) and line[i] != '(':
            i += 1    
        
        while j > 0 and line[j] != ')':
            j -= 1

        if i == len(line) or j == 0:
            continue

        parse = line[i+1:j]
        parse = processed = re.sub(r'(?<![\\\w])([a-zA-Z_\d-]+[\(\<\]*\d*\)?[\|a-zA-Z_]*)', r'"\1"',
                                   parse.replace('\n', '')).replace('\\', '\\\\').replace('=', ':').replace('"true"', 'true').replace('"false"', 'false').replace('...', '')
        parse = "[" + parse + "]"

        if debug:
            print(parse)

        data.append("{\"" + msg + "\":" + parse + "}")

data = ",".join(data)
data = "[" + data + "]"
data = json.loads(data)

with open(output, "w+") as file:
    json.dump(data, file, indent=True)
