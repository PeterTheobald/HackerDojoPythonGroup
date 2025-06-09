# main_fastapi.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn
from nutrition import analyze_day

app = FastAPI()

FORM_HTML = """
<form method="post">
  Foods (comma-separated):<br>
  <textarea name="foods" rows="5" style="width:500px"></textarea><br>
  Current weight (kg):<br>
  <input name="weight" type="number" step="0.1"><br>
  Target weight (kg):<br>
  <input name="target_weight" type="number" step="0.1"><br>
  Gender (male/female):<br>
  <input name="gender"><br><br>
  <button type="submit">Submit</button>
</form>
"""

RESULT_HTML = """
<h2>Results</h2>
<p>Total calories: {total_calories} kcal</p>
<p>Total protein: {total_protein} g</p>
<h3>Per-item</h3>
<ul>
  {items}
</ul>
<h3>Recommendation</h3>
<p>Calories: {advice_calories} (recommended {rec_calories} kcal)</p>
<p>Protein: {advice_protein} (recommended {rec_protein:.1f} g)</p>
"""

@app.get("/", response_class=HTMLResponse)
async def form():
    return FORM_HTML

@app.post("/", response_class=HTMLResponse)
async def submit(
    foods: str = Form(...),
    weight: float = Form(...),
    target_weight: float = Form(...),
    gender: str = Form(...)
):
    lst = [f.strip() for f in foods.split(",")]
    res = await analyze_day(lst, weight, target_weight, gender)
    items_html = "".join(
        f"<li>{food}: {vals['calories']} kcal, {vals['protein']} g</li>"
        for food, vals in res["per_item"].items()
    )
    rec = res["recommendation"]
    return RESULT_HTML.format(
        total_calories=res["total_calories"],
        total_protein=res["total_protein"],
        items=items_html,
        advice_calories=rec["advice"]["calories"],
        rec_calories=rec["recommended_calories"],
        advice_protein=rec["advice"]["protein"],
        rec_protein=rec["recommended_protein"]
    )

if __name__ == "__main__":
    uvicorn.run("main_fastapi:app", host="127.0.0.1", port=8000, reload=True)

