class SmartList(list):

  def __init__(self, l):/
    self.l = l

  def __add__(self, l2):
    result = []
    
    # enumerate
    # for i, v in enumerate(self.l):
    #     result.append(v + l2[i])


    for i1, i2 in zip(self.l, l2):
       result.append(i1 + i2)

    
    for i in range(len(self.l)):
      result.append(self.l[i] + l2[i])
    return result


myl = SmartList([1, 2, 3])
print(myl + [10, 20, 30])


d = { 'name': 'pete', 'score': 99}

d['name']

def main():
  tests 

if __name__ == '__main__':
  main()




