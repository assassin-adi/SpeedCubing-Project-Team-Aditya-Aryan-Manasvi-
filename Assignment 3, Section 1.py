import cv2

c = ['White', 'Orange', 'Green', 'Red', 'Blue', 'Yellow']
values = {}

cap = cv2.VideoCapture(0)
counter = 0

while counter < 6:
    video = cap.read()[1]
    if video is None:
        break

    h, w = video.shape[:2]
    s = 150

    x1, y1 = (w - s) // 2, (h - s) // 2
    x2, y2 = x1 + s, y1 + s
    x, y = w // 2, h // 2

    cv2.rectangle(video, (x1, y1), (x2, y2), (255, 255, 255), 2)
    cv2.circle(video, (x, y), 8, (255, 255, 255), 2)
    cv2.putText(video, f"Scanned: {counter}/6", (w - 190, 40),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1)
    cv2.putText(video, f"Scanning: {c[counter]}", (w - 190, 80),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

    cv2.imshow('scanner', video)
    key = cv2.waitKey(1)

    if key == 32:
        b, g, r = video[y, x]
        values[c[counter]] = {'rgb': (r, g, b)}
        counter += 1

print("RGB values:")
for c, data in values.items():
    print(f"{c}: {data['rgb']}")






