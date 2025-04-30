buf = bytearray(open("roadrunner.mp3", "rb").read())

title = "My New Title".encode("latin1").ljust(30, b'\x00')

# prepend TAG if missing
if buf[-128:-125] != b"TAG":
    buf[-128:] = b"TAG" + b"\x00"*125
# overwrite title field (bytes 3–32 of that footer)
buf[-125:-95] = title
open("song.mp3","wb").write(buf)

