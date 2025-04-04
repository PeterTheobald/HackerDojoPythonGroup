# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "objgraph",
# ]
# ///
import objgraph

class MyC:
  def __init__(self):
    self.x = []
  def bump(self, v):
    self.x.append(v)

x=MyC()
for i in range(100):
  x.bump(100)

# After running your app for a while:
objgraph.show_growth(limit=10)  # Shows which object types are growing

# To trace references to a specific object type:
objs = objgraph.by_type('MyC')
objgraph.show_backrefs([objs[0]], filename='backrefs.png')


