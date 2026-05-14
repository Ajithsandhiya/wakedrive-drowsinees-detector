import cv2
import pygame
import os
import mediapipe as mp
import math

# -----------------------------
# CONFIGURATION
# -----------------------------
EYE_AR_THRESH = 0.22        # Eye Aspect Ratio threshold
EYE_AR_CONSEC_FRAMES = 15   # Frames the eyes must be closed to trigger alarm
COUNTER = 0                 # Counter for consecutive frames
ALARM_ON = False            # Alarm state

# -----------------------------
# MUSIC PLAYER SETUP
# -----------------------------
# Initialize Pygame Mixer
try:
    # Pre-initialize mixer with common settings to avoid errors on some systems
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    print("Pygame mixer initialized successfully.")
except pygame.error as e:
    print(f"Pygame Error during initialization: {e}")
except Exception as e:
    print(f"Unexpected error initializing pygame mixer: {e}")

def play_alarm():
    global ALARM_ON
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # The file in the 'songs' folder is 'sleep.mp3'
    path = os.path.join(script_dir, "songs", "sleep.mp3")


    
    if not os.path.exists(path):
        print(f"ERROR: Alarm file not found at {path}")
        return

    if not ALARM_ON:
        try:
            print(f"Attempting to load alarm from: {path}")
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1) # Loop indefinitely
            ALARM_ON = True
            print("ALARM STARTED!")
        except pygame.error as e:
            print(f"Pygame Error while playing: {e}")
        except Exception as e:
            print(f"Unexpected error playing alarm: {e}")


def stop_alarm():
    global ALARM_ON
    if ALARM_ON:
        pygame.mixer.music.stop()
        ALARM_ON = False
        print("ALARM STOPPED")

# -----------------------------
# MEDIAPIPE FACE MESH
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# Eye landmark indexes (standard MediaPipe)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# -----------------------------
# EYE ASPECT RATIO FUNCTION
# -----------------------------
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def eye_aspect_ratio(eye_points):
    # vertical distances
    v1 = euclidean(eye_points[1], eye_points[5])
    v2 = euclidean(eye_points[2], eye_points[4])
    # horizontal distance
    h = euclidean(eye_points[0], eye_points[3])
    ear = (v1 + v2) / (2.0 * h)
    return ear

# -----------------------------
# CAMERA START
# -----------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open camera. Please check if your camera is connected and not used by another app.")
    exit()

print("Camera opened successfully.")
print("Driver Drowsiness System Started...")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) # Flip for mirror effect
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = []
            right_eye = []

            # Extract Left Eye Landmarks
            for idx in LEFT_EYE:
                lm = face_landmarks.landmark[idx]
                left_eye.append((int(lm.x * w), int(lm.y * h)))

            # Extract Right Eye Landmarks
            for idx in RIGHT_EYE:
                lm = face_landmarks.landmark[idx]
                right_eye.append((int(lm.x * w), int(lm.y * h)))

            # Calculate EAR
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            # -----------------------------
            # DROWSINESS LOGIC
            # -----------------------------
            if avg_ear < EYE_AR_THRESH:
                COUNTER += 1
                # If eyes are closed for a sufficient number of frames, trigger alarm
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if not ALARM_ON:
                        print(f"Drowsiness detected! (Frames: {COUNTER})")
                    play_alarm()
                    cv2.putText(frame, "!!! DROWSINESS ALERT !!!", (10, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)
            else:
                if COUNTER > 0:
                    # Reset counter and stop alarm when eyes open
                    COUNTER = 0
                    stop_alarm()

            # Visual EAR status
            status_color = (0, 255, 0) if avg_ear >= EYE_AR_THRESH else (0, 0, 255)
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # Draw eye contours (optional but helpful)
            for p in left_eye + right_eye:
                cv2.circle(frame, p, 2, (0, 255, 255), -1)

    else:
        # If no face detected, maybe stop alarm or show warning
        stop_alarm()
        cv2.putText(frame, "No Face Detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Driver Drowsiness Detector", frame)

    # Press 'q' or ESC to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()