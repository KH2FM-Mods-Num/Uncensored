import struct
import json

dsa = open('dsa.json')
dsa = json.load(dsa)
flag1 = json.load(open('progress.json'))
flag3 = json.load(open('menu.json'))

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

for world in range(19):
    filename = ['zz','es','tt','di','hb','bb','he','al','mu','po','lk','lm',
                'dc','wi','nm','wm','ca','tr','eh'][world]
    flagamt  = [0x11,0x0A,0xFF,0x01,0xC4,0x55,0x7F,0x51,0x58,0x53,0x33,0x48,
                0x22,0x2A,0x3F,0x11,0x64,0x3B,0x53][world]
    f = open('00progress.bin/trimmed/'+filename+'.bin','rb').read()
    g = open('00progress.bin/result/'+filename+'.txt','w')

    cmd = {2:'Block: ',3:'Unblock: ',4: 'Add Warp: ',5: 'Remove Warp: ',
           7:'Lower Story:',8:'Raise Menu:',9:'Lower Menu:',
           12:'Raise Story:'}
    for flag in range(flagamt+1):
        g.write(flagparse(clean(world*4)+clean(flag))+':\n')
        offset = 2 * flag
        offset = count(offset)
        if offset == 0:
            g.write('\t[SKIP]\n\n')
            continue
        while True:
            command = f[offset]
            args    = f[offset+1]
            offset += 2
            if command == 0:
                g.write('\t[END]\n\n')
                break
            elif command == 1:
                g.write('\tSpawn ID Change:\n')
                for i in range(0,args,4):
                    j = offset + 2*i
                    g.write('\t\tRoom '+clean(count(j))+ ': '+clean(count(j+2))+
                            ' '+clean(count(j+4))+' '+clean(count(j+6))+'\n')
            elif command == 6:
                g.write('\tBGM Set: '+str(f[offset])+'\n')
            elif command == 13:
                g.write('\tWorld Map: '+clean(f[offset])+' '+
                        clean(f[offset+1])+'\n')
            elif command in [2,3,4,5]:
                g.write('\t'+cmd[command]+dsa[str(f[offset])]+'\n')
            elif command in [7,12]:
                g.write('\t'+cmd[command]+'\n')
                for i in range(args):
                    j = offset + 2*i
                    g.write('\t\t'+flagparse(clean(count(j),4),flag1)+'\n')
            elif command in [8,9]:
                g.write('\t'+cmd[command]+'\n')
                for i in range(args):
                    j = offset + 2*i
                    g.write('\t\t'+flagparse(clean(count(j),2),flag3)+'\n')
            else:
                for i in range(args):
                    try:
                        j = offset + 2*i
                        g.write('\t'+cmd[command]+clean(count(j),4)+'\n')
                    except:
                        g.write('\tError Command '+str(command)+' ('+str(args)+
                                ') '+clean(count(offset+2*i),4)+'\n')
                        break
            offset += args*2

    g.close()
