# Pyodide

- Python inside the browser
- automate interactive browser, work with the DOM
- interact with Javascript


Interactive REPL at:

https://pyodide.org/en/stable/console.html

Call Python from Javascript.
Output goes to the console.
01_hello_console.html

Import libraries
02_import_numpy.html

Virtual filesystem in the browser
03_filesystem.html

Synchronous call: pyodide.runPython(code, opts?)
- fast, immediate result, BLOCKS everything until done

Asynchronous call: await pyodide.runPythonAsync(code, opts?)
- calls async, will NOT block, returns a Promise object which will get the result when it is ready

```
// write from JS → Python
pyodide.globals.set("x", 42);

// read from Python → JS
const y = pyodide.globals.get("x");   // 42
```

04_calculator.html
05_calc_async.html

matplotlib example
06_plot.html

- js await pyodide.loadPackage(["numpy","pandas","matplotlib"]);
  large download (≈10-15 MB), first call is cached by browser.
-  everything runs in the main thread; vectorised NumPy still fast enough for small-medium data.
- the default backend renders SVG strings—no <canvas> needed.
- All code runs inside the WASM sandbox, single thread (no GIL escape).
- Large arrays & plots are fine (≈ tens of MB); gigabyte-scale data will crawl.
- No direct GPU; WebAssembly SIMD helps but still slower than native CPython.
- Long-running loops block the UI → always prefer await runPythonAsync

Alternatives for heavier/interactive viz
- Plotly.js, Vega-Lite, D3 — call from JS, pass data via pyodide.globals; interactive & WebGL-accelerated.
- pythreejs / ipyvolume — render with WebGL; still experimental in Pyodide.
- Offload compute — web worker + Pyodide, or move heavy lifting to a server and keep the browser for rendering only.
