import struct
import json

dsa = open('dsa.json')
dsa = json.load(dsa)
flags = open('flag.json')
flags = json.load(flags)

class progress:
    def __init__(self):
        self.length = length
        self.content = f[offset:offset+length]

def count(address):
    return struct.unpack('h',f[address:address+2])[0]

for world in range(19):
    filename = ['zz','es','tt','di','hb','bb','he','al','mu','po','lk','lm',
                'dc','wi','nm','wm','ca','tr','eh'][world]
    flagamt  = [0x11,0x0A,0xFF,0x01,0xC4,0x55,0x7F,0x51,0x58,0x53,0x33,0x48,
                0x22,0x2A,0x3F,0x11,0x64,0x3B,0x53][world]
    filelen  = [0x13C,0x66,0x16DA,0x1C,0xD74,0x6C2,0xA2E,0x680,0x6C2,0x594,
                0x630,0x5E4,0x2EE,0x3E2,0x6C8,0x44,0x9DE,0x536,0x54A]
    f = open('00progress.bin/'+filename+'.bin','rb').read()
    g = {}

    #Get Flag Length & Commands
    for flag in range(flagamt+1):
        offset = count(flag*2)
        if offset == 0 or f[offset] == 0:
            g[flag] = 0
            continue
        length = 0
        while f[offset+length] > 0:
            args = f[offset+length+1]
            length += 2 + 2*args
        length += 2 #Include Termination Code
        g[flag] = progress()

    #Write Flag
    h = open('00progress.bin/trimmed/'+filename+'.bin','wb')
    totallength = 0
    initoffset  = (flagamt+1)*2
    for flag in range(flagamt+1):
        if g[flag] == 0:
            h.write(b'\x00\x00')
            pass
        else:
            h.write(struct.pack('H',initoffset+totallength))
            totallength += g[flag].length
    for flag in range(flagamt+1):
        if g[flag] != 0:
            h.write(g[flag].content)
            pass

    #Pad out the file
    x = filelen[world] - (initoffset+totallength)
    if x < 0:
        print(filename+' exceeds original size by '+str(-x)+' bytes.')
    else:
        print(filename+' has '+str(x)+' free bytes.')
        h.write(bytearray(x))
    h.close()

    
