# WakeDrive: Driver Drowsiness Detection System 🚗💤

WakeDrive is a real-time computer vision project that monitors a driver's eyes and triggers an audio alarm if they show signs of drowsiness or fall asleep at the wheel. This system aims to prevent road accidents caused by driver fatigue.

## Features 🌟
- **Real-time Face & Eye Tracking**: Uses a webcam to continuously monitor the driver's face.
- **Accurate Landmark Detection**: Utilizes Google's MediaPipe Face Mesh for precise 3D facial landmark detection.
- **Eye Aspect Ratio (EAR)**: Calculates the EAR to accurately determine if the eyes are open or closed.
- **Audio Alert System**: Triggers a loud alarm using Pygame if the driver's eyes remain closed beyond a safe threshold.

## Tech Stack 🛠️
- **Python** 🐍
- **OpenCV** (cv2) - For video capture and frame processing
- **MediaPipe** - For face mesh and facial landmark detection
- **Pygame** - For playing the audio alarm
- **Math / NumPy** - For geometric distance calculations

## How It Works 💡
1. The script captures video from the computer's webcam.
2. MediaPipe detects the face and plots 468 landmarks.
3. The script extracts the specific landmarks corresponding to the left and right eyes.
4. The Euclidean distance between the vertical and horizontal eye landmarks is calculated to find the Eye Aspect Ratio (EAR).
5. If the EAR falls below a specific threshold (indicating closed eyes) for a continuous number of frames, the system triggers `alarm.wav` to wake the driver up.

## Installation & Setup 🚀

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/WakeDrive-Drowsiness-Detector.git
   cd WakeDrive-Drowsiness-Detector
   ```

2. **Install required dependencies:**
   Make sure you have Python installed. Then run:
   ```bash
   pip install opencv-python mediapipe pygame
   ```

3. **Add your alarm sound:**
   Ensure you have an audio file named `alarm.wav` in the same directory as the Python script.

4. **Run the script:**
   ```bash
   python WakeDrive.py
   ```

## Demo
*(Add a screenshot or a GIF here showing the system detecting open/closed eyes)*

## License
This project is open-source and available under the [MIT License](LICENSE).
