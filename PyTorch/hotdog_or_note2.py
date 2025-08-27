# hotdog_or_not.py
import argparse
from PIL import Image
import torch
import torch.nn.functional as F

# Requires: pip install open_clip_torch
import open_clip


def is_hotdog(image_path: str, threshold: float = 0.5):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-H-14", pretrained="laion2b_s32b_b79k"
    )
    model = model.to(device)
    model.eval()

    img = Image.open(image_path).convert("RGB")
    x = preprocess(img).unsqueeze(0).to(device)

    # Prompt ensembling for robustness
    pos_prompts = [
        "a photo of a hot dog",
        "a photo of a hotdog",
        "a photo of a sausage in a bun",
        "a photo of a frankfurter in a bun",
    ]
    neg_prompts = [
        "a photo of food that is not a hot dog",
        "a photo of something that is not a hot dog",
        "a photo without a hot dog",
    ]

    with torch.no_grad():
        # Encode image
        image_features = model.encode_image(x)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        # Encode text prompts
        pos_tokens = open_clip.tokenize(pos_prompts).to(device)
        neg_tokens = open_clip.tokenize(neg_prompts).to(device)

        pos_feats = model.encode_text(pos_tokens)
        neg_feats = model.encode_text(neg_tokens)

        pos_feats = pos_feats / pos_feats.norm(dim=-1, keepdim=True)
        neg_feats = neg_feats / neg_feats.norm(dim=-1, keepdim=True)

        # Average within each class, then re-normalize
        pos_feat = pos_feats.mean(dim=0, keepdim=True)
        neg_feat = neg_feats.mean(dim=0, keepdim=True)
        pos_feat = pos_feat / pos_feat.norm(dim=-1, keepdim=True)
        neg_feat = neg_feat / neg_feat.norm(dim=-1, keepdim=True)

        text_feats = torch.cat([pos_feat, neg_feat], dim=0)  # [2, d]

        # CLIP similarity -> softmax probability over {hot dog, not hot dog}
        logits = 100.0 * image_features @ text_feats.T  # temperature scaling as in CLIP
        probs = F.softmax(logits, dim=-1)[0]

    p_hotdog = float(probs[0].item())
    label = "HOT DOG" if p_hotdog >= threshold else "NOT HOT DOG"
    return label, p_hotdog


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="path to image file")
    ap.add_argument("--threshold", type=float, default=0.5, help="probability threshold for HOT DOG")
    args = ap.parse_args()

    label, p = is_hotdog(args.image, args.threshold)
    print(f"{label} (p_hotdog={p:.3f})")

