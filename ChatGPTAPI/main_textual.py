# main_textual.py
from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static
from nutrition import analyze_day

class NutritionApp(App):
    CSS = """
    Screen { align: center middle; }
    #inputs { layout: vertical; width: 60%; }
    Input, Button { margin: 1 0; }
    #output { border: heavy; height: 40%; overflow: auto; padding: 1; }
    """

    def compose(self) -> ComposeResult:
        with Static(id="inputs"):
            yield Input(placeholder="Foods (comma-separated)", id="foods")
            yield Input(placeholder="Current weight (kg)", id="weight")
            yield Input(placeholder="Target weight (kg)", id="target_weight")
            yield Input(placeholder="Gender (male/female)", id="gender")
            yield Button(label="Analyze", id="go")
        yield Static("", id="output")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        foods = self.query_one("#foods", Input).value
        weight = float(self.query_one("#weight", Input).value)
        target = float(self.query_one("#target_weight", Input).value)
        gender = self.query_one("#gender", Input).value
        data = await analyze_day([f.strip() for f in foods.split(",")], weight, target, gender)
        out = f"Total: {data['total_calories']} kcal, {data['total_protein']} g protein\n\n"
        out += "Per item:\n" + "\n".join(
            f"{food}: {v['calories']} kcal, {v['protein']} g"
            for food, v in data["per_item"].items()
        ) + "\n\nRecommendation:\n"
        rec = data["recommendation"]
        out += f"Calories: {rec['advice']['calories']} (rec {rec['recommended_calories']} kcal)\n"
        out += f"Protein: {rec['advice']['protein']} (rec {rec['recommended_protein']:.1f} g)\n"
        self.query_one("#output", Static).update(out)

if __name__ == "__main__":
    NutritionApp().run()
