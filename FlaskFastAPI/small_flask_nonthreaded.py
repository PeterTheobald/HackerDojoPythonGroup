from flask import Flask, render_template_string
import time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a sample Flask HTML page.</p>
</body>
</html>
"""

@app.route("/")
def home():
    time.sleep(3)  # simulate a time‐consuming task
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(threaded=False, debug=False)

