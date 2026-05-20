News:

BayPIGgies, Mon 5/28 at Palo Alto

PyCon 2026. Check out programs, pick which ones we should recap:
https://us.pycon.org/2026/schedule/
- Build your first MCP server
- Building a RAG
- Several all about sessions: Decorators, Testing, Database (ORM, SQL), Generators and Iterators, Types, 
- Cloudflare workers
- Python Security: AI and Glasswing
- Several AI coding howto sessions
- Pydantic "Monty": A minimal Python in Rust for AI Agents coding
So so many more...

# How to protect your libraries from supply-chain malware:

## Pin dependencies to known trusted versions of your libraries, or at least never use the latest release before people have tested it.

```
# create a uv.lock file once:
uv run myprog
# or
uv lock
# uses the current exact version number of every library in your pyproject.toml and saves it in the uv.lock file

uv run --locked myprog # (only uses the versions in the uv.lock file, never updates to a newer version)
```
Note: `uv run` only updates if the pyproject.toml versions **require** it to update to newer versions.
If you want to make sure you don't accidentally run `uv run` without `--locked` add this to your shell:
```
UV_LOCKED=1
```

Also, when you DO update versions, don't use the very latest that haven't been thoroughly tested by the public:
```
pyproject.toml:
[tool.uv]
exclude-newer = "30 days"
```
Add this **before** the first time you `uv run`

## Run inside a docker container
Any damage is limited to the files inside the container

## watch PyPI/package advisories

## Scan library code for malware
- `pip-audit`, `osv-scanner`, Snyk, GitHub Dependabot, or Safety
- or just AI assistant request


