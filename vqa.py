import torchvision
import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image, ImageDraw
import random
from utils.storage import StorageManager

# ---------------- COCO LABELS ----------------
COCO_CLASSES = [
'__background__','person','bicycle','car','motorcycle','airplane','bus','train','truck','boat',
'traffic light','fire hydrant','stop sign','parking meter','bench','bird','cat','dog','horse',
'sheep','cow','elephant','bear','zebra','giraffe','backpack','umbrella','handbag','tie','suitcase',
'frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard',
'surfboard','tennis racket','bottle','wine glass','cup','fork','knife','spoon','bowl','banana',
'apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','couch',
'potted plant','bed','dining table','toilet','tv','laptop','mouse','remote','keyboard','cell phone',
'microwave','oven','toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear',
'hair drier','toothbrush'
]

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    detector = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
    detector.eval()

    classifier = torchvision.models.resnet18(weights="DEFAULT")
    classifier.eval()

    return detector, classifier

detector, classifier = load_models()

# ---------------- TRANSFORMS ----------------
detect_transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
])

classify_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

IMAGENET_LABELS = torchvision.models.ResNet18_Weights.DEFAULT.meta["categories"]

# ---------------- DETECTION ----------------
def detect_objects(image):
    img_tensor = detect_transform(image)

    with torch.no_grad():
        predictions = detector([img_tensor])[0]

    detected = []

    for label, box, score in zip(
        predictions["labels"],
        predictions["boxes"],
        predictions["scores"]
    ):
        if score.item() < 0.8:
            continue

        label_id = label.item()
        coco_name = COCO_CLASSES[label_id]

        x1, y1, x2, y2 = map(int, box.tolist())

        # ✅ Preserve PERSON detection
        if coco_name == "person":
            final_name = "person"
        else:
            cropped = image.crop((x1, y1, x2, y2))
            input_tensor = classify_transform(cropped).unsqueeze(0)

            with torch.no_grad():
                outputs = classifier(input_tensor)
                pred = torch.argmax(outputs, dim=1).item()

            final_name = IMAGENET_LABELS[pred]

        detected.append({
            "name": final_name,
            "box": [x1, y1, x2, y2],
            "score": float(score.item())
        })

    return detected

# ---------------- DRAW ----------------
def draw_boxes(image, detections):
    img = image.copy()
    draw = ImageDraw.Draw(img)

    for d in detections:
        x1, y1, x2, y2 = d["box"]
        label = d["name"]
        score = round(d["score"] * 100, 1)

        draw.rectangle([x1, y1, x2, y2], outline="green", width=3)
        draw.text((x1, y1 - 10), f"{label} ({score}%)", fill="green")

    return img

# ---------------- ANSWER ----------------
def predict_answer(detections, question):

    if len(detections) == 0:
        return "No object detected.", 0.0

    detections = sorted(detections, key=lambda x: x["score"], reverse=True)

    objects = [d["name"] for d in detections]
    unique = list(dict.fromkeys(objects))

    confidence = round(detections[0]["score"] * 100, 2)

    if "person" in question.lower():
        if "person" in unique:
            return "Yes, a person is detected in the image.", confidence
        else:
            return "No person detected.", confidence

    return f"Detected objects: {', '.join(unique)}.", confidence

# ---------------- STORY ----------------
def generate_story(detections, style):

    if len(detections) == 0:
        return ""

    main = detections[0]["name"]

    places = ["in a sunny park", "in a peaceful garden", "on a quiet street", "near a house"]
    moods = ["cheerful", "calm", "excited", "playful"]
    actions = ["moving around", "posing naturally", "exploring", "enjoying the moment"]

    place = random.choice(places)
    mood = random.choice(moods)
    action = random.choice(actions)

    if style == "Funny":
        return f"A {main} was seen {place}, acting very {mood} while {action}. Suddenly, it behaved like a celebrity posing for a camera, making the moment extremely funny and entertaining. Anyone watching this would definitely smile."

    elif style == "Emotional":
        return f"In this scene, a {main} is present {place}, creating a deeply {mood} atmosphere. The way it is {action} reflects peace and simplicity, reminding us of the beauty in small moments of life."

    elif style == "Professional":
        return f"This image captures a {main} {place}. The subject appears {mood} and is observed {action}. The composition, clarity, and focus make this image suitable for analytical and professional interpretation."

    elif style == "Creative":
        return f"Imagine a world where a {main} exists {place}, surrounded by imagination. It is {action} with a {mood} energy, turning this simple moment into a magical story."

    return f"A {main} is present {place}."

# ---------------- MAIN ----------------
def main():
    st.title("Visual Question Answering (Final Improved)")

    if not st.session_state.get("logged_in"):
        st.warning("Please login first")
        return

    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    question = st.text_input("Ask a question about image")
    style = st.selectbox("Story Style", ["Funny","Emotional","Professional","Creative"])

    if st.button("Generate Answer"):

        if uploaded_file is None:
            st.warning("Upload image first")
            return

        if question.strip() == "":
            st.warning("Ask a question first")
            return

        image = Image.open(uploaded_file).convert("RGB")

        detections = detect_objects(image)

        boxed_img = draw_boxes(image, detections)
        st.image(boxed_img, caption="Detected Objects")

        answer, confidence = predict_answer(detections, question)

        st.success(f"Answer: {answer}")
        st.write(f"Confidence Score: {confidence}%")

        # ✅ SHOW STORY ONLY IF OBJECT DETECTED
        if len(detections) > 0:
            story = generate_story(detections, style)
            st.info("Story: " + story)

        storage = StorageManager()
        storage.save_history(
            st.session_state.username,
            uploaded_file.name,
            question,
            answer,
            story if len(detections) > 0 else ""
        )

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
