bytes, bytearrays, memoryviews

str 'hello'
bytes b'hello' 
bytearray(b'hello')
s = 'happy😀'
>>> b = s.encode('utf-8')
>>> b

int.from_bytes( b)
ba.hex()

# from iterable of ints
ba1 = bytearray([65, 66, 67])      # b'ABC'
# from literal
ba2 = bytearray(b'hello world')
# from size
ba3 = bytearray(5)                 # b'\x00\x00\x00\x00\x00'

len(ba), ba[0], ba[-1]

slice = ba2[0:5]                 # b'hello'

isinstance(ba2, bytearray)         # True
ba2[0] = 72                        # mutates to b'Hello world'

ba = bytearray(b'abc')
ba.append(100)       # b'abcd'
ba.extend(b'efg')    # b'abcdefg'
ba.insert(3, 88)     # b'abcXdefg'
ba.pop(2)            # removes 99 (‘c’)
ba.remove(100)       # removes first 100 (‘d’)
ba.clear()           # b''

Mutating methods change the original

Slicing / concatenation produce new objects

b = bytes(ba)        # freeze a mutable buffer
ba_new = bytearray(b)


mv = memoryview(ba)
mv[1:4] = b'XYZ'     # affects ba directly

zero-copy slicing mv[10:20] new view into buffer. ba[10:20] makes a copy
mv.cast('I')
mv( array, bytes, bytearray, NumPy types...)

data = bytearray(open('file.bin','rb').read())
data[10:14] = (1234).to_bytes(4,'big')
open('file.bin','wb').write(data)


change mp3 tag
tail -c 128 song.mp3 | xxd -g1
id3v2 -l song.mp3
