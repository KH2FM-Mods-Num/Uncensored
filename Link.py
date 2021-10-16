import struct
import json

flags = open('flag.json')
flags = json.load(flags)

def clean(num,char=2):
    if num >= 0:
        num = hex(num)[2:]
    elif num < 0:
        num = '-'+hex(num)[3:]
    return num.upper().zfill(char)

def count(address):
    return struct.unpack('h',f[address:address+2])[0]

def flagparse(flagid):
    try:
        return flagid+' '+flags[flagid]
    except:
        return flagid

f = open('00progress.bin/link.bin','rb').read()
g = open('00progress.bin/result/link.txt','w')
amt = struct.unpack('I',f[4:8])[0]

for i in range(amt):
    offset = 8 + 0x3C*i
    data = f[offset:offset+0x3C]
    req  = struct.unpack('I',data[0x38:0x3C])[0]
    for j in range(14):
        flagtype = data[j*4]
        flagnum  = clean(count(offset+4*j+2),4)
        if flagtype == 0:
            continue
        elif flagtype == 1:
            flagnum = flagparse(flagnum)
        else:
            flagnum = 'Type '+str(flagtype)+' '+flagnum
        if j == 0:
            g.write(flagnum+': ('+str(req)+')\n')
        else:
            g.write('\t'+flagnum+'\n')
    g.write('\n')
g.close()
        
