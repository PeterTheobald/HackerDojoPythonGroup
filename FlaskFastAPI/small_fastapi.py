from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>Sample Page</title>
  </head>
  <body>
    <h1>Hello, FastAPI!</h1>
    <p>This is a sample HTML page served at “/”.</p>
  </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    await asyncio.sleep(3)  # simulate a slow request
    return HTML

if __name__ == "__main__":
    print(f'Uvicorn running on http://127.0.0.1:5000 (Press Control+C to quit)')
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")

