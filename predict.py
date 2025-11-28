import torch
from torchvision import models, transforms
from PIL import Image
import os

CLASS_NAMES = ["glioma", "meningioma", "no_tumor", "pituitary"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transforms_fn = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def load_image(path):
    img = Image.open(path).convert('RGB')
    img = transforms_fn(img)
    return img.unsqueeze(0)

def build_model(num_classes=len(CLASS_NAMES)):
    model = models.resnext50_32x4d(weights=None)
    in_features = model.fc.in_features
    model.fc = torch.nn.Sequential(
        torch.nn.Dropout(p=0.5),
        torch.nn.Linear(in_features, num_classes)
    )
    return model.to(device)

def load_checkpoint(model, path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
    state = torch.load(path, map_location=device)
    state_dict = state.get("model_state_dict", state) if isinstance(state, dict) else state
    new_state = {k.replace("module.", "") if k.startswith("module.") else k: v for k, v in state_dict.items()}
    model.load_state_dict(new_state, strict=True)
    model.eval()
    return model

def predict_image(image_path, model, topk=1):
    input_tensor = load_image(image_path).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        top_probs, top_idx = probs.topk(topk, dim=1)
    top_probs = top_probs.cpu().numpy()[0]
    top_idx = top_idx.cpu().numpy()[0]
    results = [(CLASS_NAMES[idx], float(prob)) for idx, prob in zip(top_idx, top_probs)]
    return results
