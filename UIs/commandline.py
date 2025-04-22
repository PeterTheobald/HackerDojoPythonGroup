 Command line python programs

 cmd line: ls top grep curl etc
  cmd -opt val -opt2 val

sys.argv

argparse
 positional optional defaults help-msgs, types

gooey
1. from gooey import Gooey, GooeyParser
2. @Gooey(program_name="Weather Report GUI", default_size=(600, 400))
   def main():
3. parser = GooeyParser(description='xxx')

Better libraries:
Click
Typer (uses type hints)
Docopt
Fire

Interactive screens like `top`:
curses (the old default)
Textual (rich text, formatting, advanced layouts, uses Rich)
Prompt toolkit (advanced)
PyInquirer (simplest)
asciimatics (animations, games)
