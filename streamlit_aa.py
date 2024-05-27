import subprocess

import cv2
import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
from ultralytics.utils.plotting import Annotator
import os

# Set page configuration
st.set_page_config(page_title="Real-time Object Detection", layout="wide")
bg = os.path.abspath("/Users/rabuazzah/Downloads/kepler.gl (1).png")
m_paths = ['best.pt', 'best_80_10_10.pt']
# Custom CSS to style the Streamlit app
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url('file:///{bg}');
        background-size: cover;
        background-position: center;
    }}
    .css-1v3fvcr {{
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
    }}
    .stButton button {{
        background-color: #ff4b4b;
        color: white;
    }}
    .css-1d391kg {{
        color: black;
    }}
    .css-17eq0hr {{
        color: black;
    }}
    .stSlider .css-yiuvkt {{
        color: black;
    }}
    .stImage {{
        border: 2px solid #ff4b4b;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_resource
def get_models():
    models = [YOLO(p) for p in m_paths]
    return models


models = get_models()
model = models[0]


def plot_bounding_boxes(yolo_result):
    """Draw bounding boxes from yolo.predict() result"""
    image = yolo_result.orig_img[..., ::-1]
    annotate = Annotator(np.ascontiguousarray(image))
    names = map(yolo_result.names.get, yolo_result.boxes.cls.tolist())

    scores = yolo_result.boxes.conf.tolist()
    boxes = yolo_result.boxes.xyxy
    for box, label, score in zip(boxes, names, scores):
        color = np.random.randint(0, 255, 3).tolist()
        tag = f"{label.title()}: {score:.0%}"
        annotate.box_label(box, tag, color)
    return Image.fromarray(annotate.result())


def main():
    st.title('Object Detection using YOLOv5')

    # Sidebar for Image/Video Configuration
    st.sidebar.header("Image/Video Config")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "webp"])
    confidence_threshold = st.sidebar.slider('Select Model Confidence', 25, 100, 40)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        if uploaded_file is not None:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

            # Perform object detection
            result = model(uploaded_image)[0]
            img_with_boxes = plot_bounding_boxes(result)

            with col2:
                st.subheader("Detected Image")
                st.image(img_with_boxes, caption='Detected Image', use_column_width=True)

    st.subheader('Real-time Object Detection with YOLOv5')

    if 'run' not in st.session_state:
        st.session_state.run = False

    start_button = st.button('Start', key='start_button')
    stop_button = st.button('Stop', key='stop_button')

    if start_button:
        st.session_state.run = True

    if stop_button:
        st.session_state.run = False

    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    frame_placeholder = st.empty()  # Placeholder for video frame

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video")
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

    cap.release()


if __name__ == "__main__":
    main()
