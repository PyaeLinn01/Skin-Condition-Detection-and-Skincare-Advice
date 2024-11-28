# Skin Condition Detection and Skincare Advice

This is a Streamlit-based web application for detecting various skin conditions from uploaded images using a YOLO model. The application provides tailored skincare advice, recommended products, and prevention tips for detected conditions.

## Features

- **Skin Condition Detection**: Detects common skin conditions like acne, wrinkles, dry skin, oily skin, eyebags, and more.
- **Skincare Advice**: Provides actionable advice, recommended products, and prevention tips for each detected condition.
- **Interactive UI**: Upload an image and view detection results with bounding boxes and confidence scores.
- **Supports YOLO Models**: Utilizes custom-trained YOLO models for skin condition detection.

## Streamlit Deploy

🎯 Check out my streamlit app: https://facecare.streamlit.app/

---

## Installation

### Prerequisites
- Python 3.9+
- `pip` package manager

### Clone the Repository
```bash
git clone https://github.com/your-username/skin-condition-detection.git
cd skin-condition-detection
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Additional Dependency for Deployment
If deploying on Streamlit Cloud, create a `packages.txt` file and include:
```
libgl1
```

---

## Usage

### Run the Application Locally
```bash
streamlit run app.py
```

### Upload an Image
- Upload a `.jpg`, `.jpeg`, `.png`, or `.webp` file.
- The app will display:
  - Original image with detections.
  - Skincare advice for detected conditions.

---

## File Structure

```
.
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── packages.txt           # Additional packages for deployment (optional)
├── skincond.pt            # YOLO model for skin condition detection
└── README.md              # Project documentation
```

---

## YOLO Model

This project uses a custom-trained YOLO model (`skincond.pt`) to detect six skin conditions:
- Acne
- Dry Skin
- Eyebags
- Normal Skin
- Oily Skin
- Wrinkles

---

## Deployment

### Streamlit Cloud
1. Push the repository to GitHub.
2. Connect the repository to [Streamlit Cloud](https://streamlit.io/cloud).
3. Ensure the `packages.txt` file is included with the following:
   ```
   libgl1
   ```

### Docker
Include the following in your `Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y libgl1
```

---

## Example Outputs

### Input Image
Uploaded via Streamlit interface.

### Detection Results
![Detection Results Screenshot](#)

### Skincare Advice
```plaintext
Condition: Acne
Advice: Keep your skin clean, avoid harsh scrubbing, and avoid touching your face frequently.
Recommended Products:
- Salicylic Acid Cleanser
- Benzoyl Peroxide Cream
- Non-comedogenic Moisturizer
Prevention Tips:
- Wash your face twice daily with a mild cleanser.
- Avoid oily makeup products.
- Maintain a balanced diet with less sugar and processed foods.
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository.
2. Create a new branch.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Developed by **Pyae Linn**. 
