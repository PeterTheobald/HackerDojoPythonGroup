Iterators = tuple, list, string, others (`__next__`)

Standard Library


len(iterable)
sum(iterable, start=0)
pack multiple arguments into one tuple: def fn(*args)
unpack an iterable into multiple separate arguments: call_fn(*mylist)

zip(*iterables)
enumerate(iterable, start=0)
all(iterable) # {True or False}
any(iterable) # {True or False}
sorted(iterable, key=None, reverse=False)
reversed(sequence)
map(function, iterable, ...)
filter(function, iterable)
sum(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, data))) # combining iterables

Itertools

count(start=0, step=1)
cycle(iterable)
repeat(object, times=None)
chain(*iterables)
zip_longest(*iterables, fillvalue=None)
islice(iterable, start, stop, step=1)

***resume here** (add examples)

product(*iterables, repeat=1)
permutations(iterable, r=None)
combinations(iterable, r)
combinations_with_replacement(iterable, r)
accumulate(iterable, func=operator.add) # returns all intermediate results
  (see map)

Functools

reduce(function, iterable[, initializer]) # returns final result
partial(func, *args, **keywords) # returns a new function with some args filled in
@functools.cache
@functools.lru_cache(maxsize=128, typed=False)
@functools.total_ordering # expands __eq__ and __lt__ into all of the comparison operators
@functools.singledispatch # call multiple functions depending on arg type

itertoolz
functoolz
Toolz

compose
curry # see partial
@memoize # see cache
concat # see chain
partition
sliding_window
interleave
merge(dict1, dict2)
valmap(fn, dict) and keymap(fn, dict)
groupby(fn, dict)
pipe # see chain
take



# Example using partial
```
import re
import functools

def add_suffix(match, suffix):
    return match.group(0) + suffix

# Partial function that will always append "!!!"
partial_exclaim = partial(add_suffix, suffix="!!!")

text = "Hello world. This is fun."
result = re.sub(r"\b\w+\b", partial_exclaim, text)

print(result)  # Output: Hello!!! world.!!! This!!! is!!! fun.!!!
```

# My actual code:
```
import re
import functools

# def replace_word(match: re.Match[str], in_header: bool) -> str:
for line in infile:
  if re.match(r'^[a-zA-Z]+( [a-zA-Z]+)?[\r\n]*$', line):
      in_header=True
  else:
      in_header=False
  replacement_fn=functools.partial(replace_word, in_header=in_header) # pass extra arg to replace_word
  new_line = word_pattern.sub(replacement_fn, line)
  outfile.write( new_line)

 word_pattern.sub( lambda x: replace_word(x, in_header), line)
