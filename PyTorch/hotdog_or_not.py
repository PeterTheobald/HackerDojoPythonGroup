# hotdog_or_not.py
import argparse
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision.models import resnet50, ResNet50_Weights

def is_hotdog(image_path: str, threshold: float = 0.5):
    weights = ResNet50_Weights.IMAGENET1K_V2
    model = resnet50(weights=weights)
    model.eval()

    preprocess = weights.transforms()
    img = Image.open(image_path).convert("RGB")
    x = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        logits = model(x)
        probs = F.softmax(logits, dim=1)[0]

    recognized_class_names = weights.meta["categories"]
    for name in recognized_class_names:
        print(name)
    hotdog_idx = next(i for i, name in enumerate(recognized_class_names) if "hotdog" in name.lower() or "hot dog" in name.lower())
    # Note: next(generator) is a nice idiom. It returns the first item without calling for the entire list.
    #       [list comprehension][0] would execute the entire list first
    p_hotdog = float(probs[hotdog_idx].item())
    label = "HOT DOG" if p_hotdog >= threshold else "NOT HOT DOG"
    return label, p_hotdog

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="path to image file")
    ap.add_argument("--threshold", type=float, default=0.5, help="probability threshold for HOT DOG")
    args = ap.parse_args()

    label, p = is_hotdog(args.image, args.threshold)
    print(f"{label} (p_hotdog={p:.3f})")

