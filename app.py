import streamlit as st
import cv2
import tempfile
import os
from crowd_utils import process_frame
import numpy as np
import time
import plotly.graph_objects as go

# -------------------- Page Config -------------------- #
st.set_page_config(page_title="Crowd Monitoring", layout="wide")

# ---------------- Session State Initialization ---------------- #
if "people_history" not in st.session_state:
    st.session_state["people_history"] = []

if "violation_history" not in st.session_state:
    st.session_state["violation_history"] = []

if "frame_count" not in st.session_state:
    st.session_state["frame_count"] = 0

# ---------------- Title ---------------- #
st.markdown("<h1 style='text-align: center;'>🔍 Real-Time Crowd Counting & Distance Violation Detection</h1>", unsafe_allow_html=True)

# ---------------- Sidebar Controls ---------------- #
st.sidebar.header("⚙️ Settings")
distance_threshold = st.sidebar.slider("Distance Threshold (px)", 20, 300, 100)
show_lines = st.sidebar.checkbox("Show Social Distance Lines", value=True)
video_source = st.sidebar.radio("Choose Input Source", ["📷 Webcam", "📁 Upload Video"])
reset_data = st.sidebar.button("🔄 Reset Graph Data")

if reset_data:
    st.session_state.people_history = []
    st.session_state.violation_history = []
    st.session_state.frame_count = 0
    st.experimental_rerun()

# ---------------- UI Placeholders ---------------- #
people_count_placeholder = st.empty()
violation_count_placeholder = st.empty()
frame_placeholder = st.empty()
chart_placeholder = st.empty()

# ---------------- Main Logic ---------------- #
def main(video_path=None):
    if video_path:
        cap = cv2.VideoCapture(video_path)
    else:
        cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (720, 480))
        annotated_frame, person_count, violation_count = process_frame(frame, distance_threshold, show_lines)

        # Convert BGR to RGB
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(annotated_frame, channels="RGB", use_column_width=True)

        people_count_placeholder.metric("👥 People Detected", person_count)
        violation_count_placeholder.metric("❌ Violations", violation_count)

        # Store history for graph
        st.session_state["frame_count"] += 1
        st.session_state.people_history.append(person_count)
        st.session_state.violation_history.append(violation_count)

        # Update graph
        chart_placeholder.plotly_chart(draw_graph(
            st.session_state.people_history,
            st.session_state.violation_history,
            st.session_state.frame_count
        ), use_container_width=True)

        time.sleep(0.03)  # Playback delay

    cap.release()


# ---------------- Graph Drawing ---------------- #
def draw_graph(people, violations, frame_count):
    x = list(range(1, frame_count + 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=people, mode='lines+markers', name="👥 People", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=x, y=violations, mode='lines+markers', name="❌ Violations", line=dict(color="red")))

    fig.update_layout(
        title="📈 Crowd Count & Violation Trend",
        xaxis_title="Frame #",
        yaxis_title="Count",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=30, b=30)
    )
    return fig


# ---------------- Handle Video Source ---------------- #
if video_source == "📁 Upload Video":
    uploaded_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        main(tfile.name)
else:
    if st.sidebar.button("▶ Start Webcam"):
        main()
