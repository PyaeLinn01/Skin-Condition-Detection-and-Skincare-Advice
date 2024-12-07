import streamlit as st
import cv2
import numpy as np
import cvzone
from ultralytics import YOLO
import os

# Global model variables
YOLO_MODEL = None

# Class labels for detection
class_labels = {
    0: 'acne',
    1: 'dry',
    2: 'eyebag',
    3: 'normal',
    4: 'oily',
    5: 'wrinkles',
}

# Skincare advice based on condition
def get_skincare_advice(condition_name):
    advice = {
        "acne": {
            "advice": "Keep your skin clean, avoid harsh scrubbing, and avoid touching your face frequently.",
            "products": [
                "Salicylic Acid Cleanser",
                "Benzoyl Peroxide Cream",
                "Non-comedogenic Moisturizer"
            ],
            "prevention": [
                "Wash your face twice daily with a mild cleanser.",
                "Avoid oily makeup products.",
                "Maintain a balanced diet with less sugar and processed foods."
            ]
        },
        "wrinkles": {
            "advice": "Stay hydrated, use sunscreen daily, and consider anti-aging products.",
            "products": [
                "Retinol Serum",
                "Vitamin C Cream",
                "Broad-Spectrum SPF 30+ Sunscreen"
            ],
            "prevention": [
                "Avoid prolonged sun exposure.",
                "Use a daily moisturizer with antioxidants.",
                "Quit smoking to prevent premature aging."
            ]
        },
        "dry": {
            "advice": "Use gentle, hydrating products and avoid hot showers.",
            "products": [
                "Hyaluronic Acid Serum",
                "Ceramide-based Moisturizer",
                "Gentle Cream Cleanser"
            ],
            "prevention": [
                "Drink plenty of water.",
                "Use a humidifier in dry environments.",
                "Avoid using strong soaps or alcohol-based toners."
            ]
        },
        "oily": {
            "advice": "Keep your skin clean and use oil-free, mattifying products.",
            "products": [
                "Oil-Free Gel Moisturizer",
                "Clay Mask",
                "Niacinamide Serum"
            ],
            "prevention": [
                "Avoid overwashing your face, as it can cause more oil production.",
                "Blot your skin with oil-absorbing sheets.",
                "Use lightweight, non-comedogenic products."
            ]
        },
        "eyebag": {
            "advice": "Get enough sleep, stay hydrated, and use eye-specific skincare products.",
            "products": [
                "Caffeine Eye Cream",
                "Cold Compress Gel Mask",
                "Hyaluronic Acid Eye Serum"
            ],
            "prevention": [
                "Sleep for 7-8 hours daily.",
                "Reduce salt intake to prevent fluid retention.",
                "Apply cold compresses to reduce puffiness."
            ]
        },
        "normal": {
            "advice": "Maintain your skin's natural balance with gentle, nourishing products.",
            "products": [
                "Daily Moisturizer with SPF",
                "Gentle Cleanser",
                "Vitamin E Cream"
            ],
            "prevention": [
                "Stick to a simple skincare routine.",
                "Avoid overusing harsh treatments.",
                "Protect your skin from environmental damage."
            ]
        }
    }
    return advice.get(condition_name.lower(), {
        "advice": "No specific advice available for this condition.",
        "products": [],
        "prevention": []
    })

# Function to get the YOLO model
def get_yolo_model():
    global YOLO_MODEL
    if YOLO_MODEL is None:
        model_path = "skincond.pt"
        if not os.path.exists(model_path):
            st.error(f"Model file '{model_path}' not found. Please ensure it is in the correct directory.")
            return None
        YOLO_MODEL = YOLO(model_path)
    return YOLO_MODEL

# Function to process a frame with YOLO model results
def process_frame_with_results(cv_image):
    yolo_model = get_yolo_model()
    if yolo_model is None:
        return cv_image, []

    results = yolo_model(cv_image)
    detection_results = []
    detected_classes = set()

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            confidence = box.conf[0]
            class_name = class_labels.get(cls, "Unknown")

            cvzone.putTextRect(cv_image, f'{class_name} ({confidence:.2f})', (x1, y1 - 10), scale=2, thickness=2)
            cvzone.cornerRect(cv_image, (x1, y1, x2 - x1, y2 - y1))

            detected_classes.add(class_name)

            detection_results.append({
                'name': class_name,
                'confidence': float(confidence),
                'box': [x1, y1, x2, y2]
            })

    return cv_image, list(detected_classes)

# Streamlit Application
st.title("Skin Condition Detection and Skincare Advice")

uploaded_file = st.file_uploader("Upload an image for skin condition detection", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    try:
        # Load image and convert it to RGB format
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the uploaded image in its original colors
        st.image(image_rgb, caption="Uploaded Image", use_container_width=True)

        st.write("Detecting skin conditions...")
        processed_image, detected_classes = process_frame_with_results(image)

        # Convert processed image back to RGB for display
        processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        st.image(processed_image_rgb, caption="Detection Results", use_container_width=True)

        if detected_classes:
            st.subheader("Skincare Advice:")
            for class_name in detected_classes:
                advice = get_skincare_advice(class_name)
                st.write(f"**Condition:** {class_name.capitalize()}")
                st.write(f"**Advice:** {advice['advice']}")
                st.write("**Recommended Products:**")
                for product in advice['products']:
                    st.write(f"- {product}")
                st.write("**Prevention Tips:**")
                for tip in advice['prevention']:
                    st.write(f"- {tip}")
        else:
            st.write("No detections found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
