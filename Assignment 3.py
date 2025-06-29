import cv2
import numpy as np

face = ["White", "Orange", "Green", "Red", "Blue", "Yellow"]
calibrated_colors = {}
i = 0
cap = cv2.VideoCapture(0)

def get_avg_color(frame, center, radius=10):
    mask = np.zeros(frame.shape[:2], dtype="uint8")  
    cv2.circle(mask, center, radius, 255, -1)        
    mean = cv2.mean(frame, mask=mask)               
    return (int(mean[2]), int(mean[1]), int(mean[0]))  

def color_match(rgb):
    for name,ref in calibrated_colors.items():
        if all(abs(rgb[i]-ref[i])<=50 for i in range(3)):
            return name
    return '?'

# --- Calibration ---
while i < 6:
    x, frame = cap.read()
    if not x:
        break
    height, width = frame.shape[:2]
    square_size = 250
    x1 = width // 2 - square_size // 2
    y1 = height // 2 - square_size // 2
    x2 = width // 2 + square_size // 2
    y2 = height // 2 + square_size // 2
    centre = (width // 2, height // 2)
  
    key = cv2.waitKey(1)
    if key == 27:  
        break
    elif key == 32:  
        rgb = get_avg_color(frame, centre, radius=10)
        calibrated_colors[face[i]] = rgb
        print(f"Calibrated {face[i]}: {rgb}")
        i += 1

    if i < 6:
        cv2.putText(frame, f"Scanned:{i}/6", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.putText(frame, f"Scan:{face[i]}", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 3)
        cv2.circle(frame, centre, 4, (255, 255, 255), -1)
        cv2.imshow("Webcam", frame)

face_dic = {}
scanned_faces = 0  # <-- Only increment, never reset

while True:
    positions = []
    _, frame = cap.read()
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    for i in [-80, 0, 80]:
        for j in [-80, 0, 80]:
            x = cx + i
            y = cy + j
            positions.append((x, y))
            cv2.circle(frame, (x, y), 10, (255, 255, 255), 2)

    square_size = 250
    x1 = width // 2 - square_size // 2
    y1 = height // 2 - square_size // 2
    x2 = width // 2 + square_size // 2
    y2 = height // 2 + square_size // 2
    centre = (width // 2, height // 2)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 3)

    facelet = []
    face_color = [['' for _ in range(3)] for _ in range(3)]

    # Fill facelet and face_color in row-major order
    k = 0
    for row in range(3):
        for col in range(3):
            f = get_avg_color(frame, positions[k], radius=10)
            facelet.append(f)
            face_color[row][col] = color_match(f)
            k += 1

    # Preview box (top right)
    px, py, box = w - 90, 20, 20
    k = 0
    for row in range(3):
        for col in range(3):
            rgb = facelet[k]
            bgr = (rgb[2], rgb[1], rgb[0])
            x1 = px + col * box
            y1 = py + row * box
            cv2.rectangle(frame, (x1, y1), (x1 + box, y1 + box), bgr, -1)
            cv2.rectangle(frame, (x1, y1), (x1 + box, y1 + box), (100, 100, 100), 1)
            k += 1

    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1)

    if key == 27:
        break
    elif key == 32:
        x = face_color[1][1]  # center facelet color
        if x in face_dic:
            print(f"Face {x} already scanned.")
        else:
            face_dic[x] = [row[:] for row in face_color]
            print(f"Scanned face: {x}")
            for row in face_color:
                print(row)
            scanned_faces += 1
        if scanned_faces == 6:
            break

print(face_dic)

cap.release()
cv2.destroyAllWindows()






