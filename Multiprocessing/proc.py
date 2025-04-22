import subprocess
import time


def play():
  with subprocess.Popen(
    [
      '/nix/store/wdqh03wsbd2ad9f77f8hnl01bprnbbd1-bsd-games-2.17/bin/adventure'
    ],
      # stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      text=True) as proc:
    while proc.poll() is None:
      print('Adventure process is alive')
      time.sleep(5)
      print('getting output:')
      print(proc.stdout.read1())
      #i = input()
      #proc.stdin = i
    print('Adventure process died')


play()
