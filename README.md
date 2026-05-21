## README.md

````md
# Air Canvas using OpenCV and MediaPipe

An AI-powered virtual drawing application that allows users to draw in the air using hand gestures through a webcam. Built using Python, OpenCV, and MediaPipe.

---

# Features

- Draw in the air using index finger
- Smooth drawing using interpolation and filtering
- Eraser mode using hand gestures
- Change drawing colors with gestures
- Fullscreen canvas
- Real-time hand tracking
- Gesture-controlled interaction
- Clear canvas option

---

# Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

---

# Hand Gestures

| Gesture | Action |
|---------|--------|
| Index finger up | Draw |
| Index + Middle finger up | Erase |
| All fingers up after fist | Change color |
| Fist | Used for color switch trigger |

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/air-canvas.git
cd air-canvas
````

## 2. Create virtual environment (Optional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Project

```bash
python air_canvas.py
```

---

# Controls

| Key | Function         |
| --- | ---------------- |
| q   | Quit application |
| c   | Clear canvas     |

---

# Project Structure

```bash
air-canvas/
│
├── air_canvas.py
├── requirements.txt
└── README.md
```

---

# How It Works

1. Webcam captures live video.
2. MediaPipe detects hand landmarks.
3. Finger positions are analyzed.
4. Specific gestures trigger actions:

   * Drawing
   * Erasing
   * Color changing
5. OpenCV renders the drawing canvas in real time.

---

# Future Improvements

* Save drawings as images
* Multiple brush sizes
* More gesture controls
* Shape drawing support
* AI-based handwriting recognition

---

# Output

The application opens a fullscreen window where users can draw in the air naturally using hand gestures.

---

# License

This project is open-source and available under the MIT License.

````