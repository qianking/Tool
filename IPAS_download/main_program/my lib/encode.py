import keyword
a = 'Qianking0706'


def encode(ch):
    b = []
    for k in ch:
        chi = ord(k) - 2
        b.append(chr(chi))
    b_n = ''.join(b)
    return b_n

def decode(ch):
    c = []
    for k in ch:
        ch = ord(k) + 2
        c.append(chr(ch))
    b_m =''.join(c)
    #print(b_m)
    return b_m 

    





