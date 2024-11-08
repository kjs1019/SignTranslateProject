from packages import *

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      # Convert BGR -> RGB
    image.flags.writeable = False                       # Set the image to read-only mode
    results = model.process(image)                      # MediaPipe Model Prediction
    image.flags.writeable = True                        # Set the image back to writeable mode
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)      # Convert back to RGB -> BGR
    return results

def mediapipe_detection_draw_landmarks(image, results):
    mediapipe_drawing.draw_landmarks(image, results.face_landmarks, mediapipe_holistic.FACEMESH_TESSELATION,
                                     mediapipe_drawing.DrawingSpec(color=(255,0,0), thickness=1, circle_radius=1),  # Dot Color/Size
                                          mediapipe_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1))  # Line Color/Size

    mediapipe_drawing.draw_landmarks(image, results.pose_landmarks, mediapipe_holistic.POSE_CONNECTIONS,
                                     mediapipe_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3), # Dot Color/Size
                                     mediapipe_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)) # Line Color/Size

    mediapipe.solutions.drawing_utils.draw_landmarks(image, results.left_hand_landmarks, mediapipe_holistic.HAND_CONNECTIONS,
                                    mediapipe_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3), # Dot Color/Size
                                    mediapipe_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)) # Line Color/Size

    mediapipe.solutions.drawing_utils.draw_landmarks(image, results.right_hand_landmarks, mediapipe_holistic.HAND_CONNECTIONS,
                                    mediapipe_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3), # Dot Color/Size
                                    mediapipe_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)) # Line Color/Size

def keypoint_value_extraction(results):
    if results.face_landmarks:
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten()     # Flatten into 1-D array
    else:
        face = np.zeros(468 * 3)  # Fill with zeros if no face detected

    if results.pose_landmarks:
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten()     # Flatten into 1-D array
    else:
        pose = np.zeros(33 * 4)  # Fill with zeros if no pose detected

    if results.left_hand_landmarks:
        left_hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()     # Flatten into 1-D array
    else:
        left_hand = np.zeros(21 * 3)  # Fill with zeros if no left hand detected

    if results.right_hand_landmarks:
        right_hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()   # Flatten into 1-D array
    else:
        right_hand = np.zeros(21 * 3)  # Fill with zeros if no right hand detected

    keypoints = np.concatenate([face, pose, left_hand, right_hand]) # Concatenate into one array
    return keypoints

def myPutText(src, text, pos, font_size, font_color) :
    img_pil = Image.fromarray(src)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype('fonts/gulim.ttc', font_size)
    draw.text(pos, text, font=font, fill= font_color)
    return np.array(img_pil)