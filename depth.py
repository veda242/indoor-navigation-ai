import torch
import cv2

# Load MiDaS model
model_type = "MiDaS_small"
midas = torch.hub.load("intel-isl/MiDaS", model_type, trust_repo=True)
midas.eval()

# Load transforms
transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
transform = transforms.small_transform


def get_depth_map(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_batch = transform(img)

    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth_map = prediction.cpu().numpy()
    return depth_map