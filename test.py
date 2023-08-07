HEX_Filter_repr = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])
HEX_Filter_chr = ''.join([(len(chr(i)) == 1) and chr(i) or '.' for i in range(256)])



for i in range(256):
    print(i,": ", HEX_Filter_chr[i])