PyTorch docs vision models:
https://docs.pytorch.org/vision/stable/models.html

Note: After running these pytorch programs with `uv run hotdog_or_not.py`, uv will have installed the large pytorch libraries in .venv. If you want to free up that space:
```
rm -r .venv
uv cache clean torch torchvision
uv cache prune
```
Don't worry, uv will reinstall them when needed next time you run the programs.


