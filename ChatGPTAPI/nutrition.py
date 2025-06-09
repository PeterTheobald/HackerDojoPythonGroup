# nutrition.py
import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def fetch_nutrition(food_items: list[str]) -> dict[str, dict[str, float]]:
    prompt = (
        "You are a nutrition assistant. For the following list of foods, "
        "return a JSON object mapping each food to its calories (kcal) "
        "and protein (g), output raw JSON only, no markdown fences, e.g.\n"
        '{"apple": {"calories": 95, "protein": 0.5}, ...}\n'
        f"Foods: {food_items}"
    )
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    return json.loads(resp.choices[0].message.content)

def calculate_totals(nutrition_data: dict[str, dict[str, float]]) -> tuple[int, float]:
    total_cal = sum(item["calories"] for item in nutrition_data.values())
    total_prot = sum(item["protein"] for item in nutrition_data.values())
    return total_cal, total_prot

def recommend(cal: int, prot: float, weight: float, target_weight: float, gender: str) -> dict[str, str | float]:
    rec_cal = 2500 if gender.lower() == "male" else 2000
    rec_prot = weight * 0.8
    advice = {
        "calories": "eat more" if cal < rec_cal else "eat less",
        "protein":  "eat more" if prot < rec_prot else "eat less"
    }
    return {
        "recommended_calories": rec_cal,
        "recommended_protein": rec_prot,
        "advice": advice
    }

async def analyze_day(
    food_items: list[str],
    weight: float,
    target_weight: float,
    gender: str
) -> dict:
    data = await fetch_nutrition(food_items)
    total_cal, total_prot = calculate_totals(data)
    rec = recommend(total_cal, total_prot, weight, target_weight, gender)
    return {
        "per_item": data,
        "total_calories": total_cal,
        "total_protein": total_prot,
        "recommendation": rec
    }
