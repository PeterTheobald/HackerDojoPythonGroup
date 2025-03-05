import sys
import requests
from rich.pretty import pprint

print(" ".join(sys.argv[1:]))
resp = requests.get("https://peps.python.org/api/peps.json")
pprint(resp.json())

