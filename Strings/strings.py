# STRING LITERALS
s='hello "brave" world'
s="hello 'brave' world"
s="""hello 'brave' "new" world"""
s='hello\nworld'
s="hello\nworld"
s="""hello
world"""
s=r"hello\nworld" # raw string

# F-STRINGS
n="peter"
s=f'My name is {n}\nhow do you do?'
s=fr'My name is {n}\nhow do you do?'
f'5+5={5+5}'
f'number={99.12345:<10}'
f'number={99.12345:>10}'
f'number={99.12345:^10}'
f'number={99.12345:.2f}'
import datetime
d=datetime.datetime(2024,4,2,12,15,58)
f'{d:%Y-%m-%d %H:%M:%S}'

s="unicode (\N{CIRCLE WITH ALL BUT UPPER LEFT QUADRANT BLACK}_\N{CIRCLE WITH ALL BUT UPPER LEFT QUADRANT BLACK})"
s='unicode (◕_◕)'

# CONCATENATION
s='hello'+'world'
s='hello' 'world'
s=''.join( ('hello', 'world') )
s=','.join( ('hello', 'world') )
"yadda "*3 # repetition
s=''
for num in range(10):
  s=s+str(num) # many concatenates
for num in range(10):
  l.append(str(num))
s=','.join(l) # one join is faster than many concatenates

# IMMUTIBLE
l=[1,2,3]
l[1]=99
t=(1,2,3)
t[1]=99
s="hello world"
s[1]="x"
s[0:5], s[:5], s[6:], s[-3:] # slices

# SEQUENCE FUNCTIONS
len('zebra')
min('zebra')
max('zebra')

# CLASS STRING FUNCTIONS
str.upper('Hello') or 'Hello'.upper()
'Hello'.lower()
'hello there'.title()
'hello there'.capitalize()
'12345'.isdigit()
'hello'.isalpha() # lots more
'-sep-'.join(list)
'here there her'.find('her')
'here there her'.index('her')
'here there her'.rfind('her')
'here there her'.replace('her','AAA')

"this has many words".split()

# REGEX
match_obj = re.search( r'\d+', "this has 333 digits")

# third party libraries
pandas strings
textblob # natural language processing
python-docx # MS Word docs

# MORE...
unicode and bytes, encode, decode
normalization
maketrans and translate

