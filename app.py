import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from ultralytics import YOLO

# === CONFIG ===
NORTH_VIDEO = r"C:\Users\rajiv\Downloads\video3.mp4"
SOUTH_VIDEO = r"C:\Users\rajiv\Downloads\video2.mp4"
DISPLAY_SIZE = (420, 320)
DETECT_INTERVAL_MS = 100
MIN_GREEN = 8
MAX_GREEN = 15

VEHICLE_LABELS = {"car", "truck", "bus", "motorbike", "motorcycle", "bicycle", "van"}
EMERGENCY_LABELS = {"ambulance", "firetruck", "fire truck", "police", "police car", "policecar"}

# === YOLO LOCAL MODEL PATHS ===
vehicle_model_path = r"C:\Users\rajiv\Documents\traffic-dashboard\yolov8m.pt"
emergency_model_path = r"C:\Users\rajiv\Documents\traffic-dashboard\yolov8n.pt"

# === LOAD MODELS ===
vehicle_model = YOLO(vehicle_model_path)
emergency_model = YOLO(emergency_model_path)

# === VIDEO CAPTURES ===
north_cap = cv2.VideoCapture(NORTH_VIDEO)
south_cap = cv2.VideoCapture(SOUTH_VIDEO)

# === GUI INIT ===
root = tk.Tk()
root.title("Smart Traffic — Live Detection")
root.configure(bg="black")

# Top labels
top_frame = tk.Frame(root, bg="black")
top_frame.pack()
north_label_text = tk.Label(top_frame, text="North: 0", fg="white", bg="black", font=("Arial", 14))
north_label_text.grid(row=0, column=0, padx=20)
timer_label = tk.Label(top_frame, text="Timer: 0s", fg="yellow", bg="black", font=("Arial", 16))
timer_label.grid(row=0, column=1, padx=40)
south_label_text = tk.Label(top_frame, text="South: 0", fg="white", bg="black", font=("Arial", 14))
south_label_text.grid(row=0, column=2, padx=20)

# Traffic lights
light_frame = tk.Frame(root, bg="black")
light_frame.pack(pady=6)
north_canvas = tk.Canvas(light_frame, width=80, height=200, bg="black", highlightthickness=0)
north_canvas.grid(row=0, column=0, padx=40)
south_canvas = tk.Canvas(light_frame, width=80, height=200, bg="black", highlightthickness=0)
south_canvas.grid(row=0, column=2, padx=40)

# Video frames
video_frame = tk.Frame(root, bg="black")
video_frame.pack(pady=6)
north_video_label = tk.Label(video_frame, bg="black")
north_video_label.grid(row=0, column=0, padx=10)
south_video_label = tk.Label(video_frame, bg="black")
south_video_label.grid(row=0, column=1, padx=10)

# Traffic state
north_count = 0
south_count = 0
north_emergency = False
south_emergency = False
green_lane = "North"
timer = MIN_GREEN
phase = "green"

# === FUNCTIONS ===
def draw_signal(canvas, color):
    canvas.delete("all")
    y_positions = [20, 70, 120]
    colors = ["red", "yellow", "green"]
    for i, col in enumerate(colors):
        fill = col if col == color else "grey"
        canvas.create_oval(10, y_positions[i], 70, y_positions[i]+40, fill=fill)

def detect_objects(frame):
    vehicle_count = 0
    emergency_present = False

    res_v = vehicle_model(frame)[0]
    for box in res_v.boxes:
        cls_name = vehicle_model.names[int(box.cls[0])].lower()
        x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
        if cls_name in VEHICLE_LABELS:
            vehicle_count += 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, cls_name, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    res_e = emergency_model(frame)[0]
    for box in res_e.boxes:
        cls_name = emergency_model.names[int(box.cls[0])].lower()
        x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
        if cls_name in EMERGENCY_LABELS:
            emergency_present = True
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, cls_name, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return frame, vehicle_count, emergency_present

# === PREPROCESS FIRST FRAME ===
ret_n, f_n = north_cap.read()
ret_s, f_s = south_cap.read()
if ret_n and ret_s:
    f_n = cv2.resize(f_n, DISPLAY_SIZE)
    f_s = cv2.resize(f_s, DISPLAY_SIZE)
    f_n, north_count, north_emergency = detect_objects(f_n)
    f_s, south_count, south_emergency = detect_objects(f_s)

    # Display first frame
    im_n = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(f_n, cv2.COLOR_BGR2RGB)))
    im_s = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(f_s, cv2.COLOR_BGR2RGB)))
    north_video_label.imgtk = im_n
    north_video_label.configure(image=im_n)
    south_video_label.imgtk = im_s
    south_video_label.configure(image=im_s)

    north_label_text.config(text=f"North: {north_count}")
    south_label_text.config(text=f"South: {south_count}")

    # Decide initial green lane
    green_lane = "North" if north_count >= south_count else "South"

# === FRAME UPDATE LOOP ===
def update_frames():
    global north_count, south_count, north_emergency, south_emergency

    ret_n, f_n = north_cap.read()
    ret_s, f_s = south_cap.read()

    if not ret_n:
        north_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_n, f_n = north_cap.read()
    if not ret_s:
        south_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_s, f_s = south_cap.read()

    f_n = cv2.resize(f_n, DISPLAY_SIZE)
    f_s = cv2.resize(f_s, DISPLAY_SIZE)

    f_n, north_count, north_emergency = detect_objects(f_n)
    f_s, south_count, south_emergency = detect_objects(f_s)

    im_n = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(f_n, cv2.COLOR_BGR2RGB)))
    im_s = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(f_s, cv2.COLOR_BGR2RGB)))
    north_video_label.imgtk = im_n
    north_video_label.configure(image=im_n)
    south_video_label.imgtk = im_s
    south_video_label.configure(image=im_s)

    north_label_text.config(text=f"North: {north_count}")
    south_label_text.config(text=f"South: {south_count}")

    root.after(DETECT_INTERVAL_MS, update_frames)

# === TIMER / SIGNAL LOGIC ===
def update_timer():
    global timer, phase, green_lane
    timer_label.config(text=f"Timer: {timer}s")

    if phase == "green":
        draw_signal(north_canvas, "green" if green_lane=="North" else "red")
        draw_signal(south_canvas, "green" if green_lane=="South" else "red")
    else:
        draw_signal(north_canvas, "yellow")
        draw_signal(south_canvas, "yellow")

    timer -= 1
    if timer <= 0:
        if phase == "green":
            phase = "yellow"
            timer = 3
        else:
            phase = "green"
            if north_emergency:
                green_lane = "North"
            elif south_emergency:
                green_lane = "South"
            else:
                green_lane = "North" if north_count >= south_count else "South"
            diff = abs(north_count - south_count)
            extra = min(10, (diff//5)*2)
            timer = MIN_GREEN + extra

    root.after(1000, update_timer)

# === START LOOPS ===
update_frames()
update_timer()
root.mainloop()
