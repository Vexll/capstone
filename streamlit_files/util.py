import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
from ultralytics.utils.plotting import Annotator


@st.cache_resource
def get_models(model_paths):
    models = {path: YOLO(path) for path in model_paths}
    return models


def plot_bounding_boxes(yolo_result):
    """Draw bounding boxes from yolo.predict() result"""
    image = yolo_result.orig_img[..., ::-1]
    annotate = Annotator(np.ascontiguousarray(image))
    names = map(yolo_result.names.get, yolo_result.boxes.cls.tolist())

    scores = yolo_result.boxes.conf.tolist()
    boxes = yolo_result.boxes.xyxy
    for box, label, score in zip(boxes, names, scores):
        # color = np.random.randint(0, 255, 3).tolist()
        color = [0, 0, 255]
        tag = f"{label.title()}: {score:.0%}"
        annotate.box_label(box, tag, color)
    return Image.fromarray(annotate.result())


def stream(model, file: str = 0):
    # Capture video from webcam
    try:
        cap = cv2.VideoCapture(file)
    except Exception:
        st.error("Failed to capture video")
        return

    frame_placeholder = st.empty()  # Placeholder for video frame

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to PIL Image
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform object detection
        result = model(pil_img)[0]
        img_with_boxes = plot_bounding_boxes(result)

        # Convert image with boxes back to numpy array
        img_with_boxes_np = np.array(img_with_boxes)

        # Display the image
        frame_placeholder.image(img_with_boxes_np, channels="RGB")

    frame_placeholder.empty()
    cap.release()
