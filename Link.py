import struct
import json

flag1 = json.load(open('progress.json'))
flag2 = json.load(open('world.json'))
flag3 = json.load(open('menu.json'))
flagdicts = [{},flag1,flag2,flag3]

def clean(num,char=2):
    if num >= 0:
        num = hex(num)[2:]
    elif num < 0:
        num = '-'+hex(num)[3:]
    return num.upper().zfill(char)

def count(address):
    return struct.unpack('h',f[address:address+2])[0]

def flagparse(flagid,flagdict=flag1):
    try:
        return flagid+' '+flagdict[flagid]
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
        else:
            if flagtype > 1:
                flagnum = flagnum[2:]
            flagtxt = 'Type '+str(flagtype)+' '
            flagtxt += flagparse(flagnum,flagdicts[flagtype])
        if j == 0:
            g.write(flagtxt+': ('+str(req)+')\n')
        else:
            g.write('\t'+flagtxt+'\n')
    g.write('\n')
g.close()
        
