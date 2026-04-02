import streamlit as st
import cv2
import numpy as np

st.set_page_config(layout="wide")

if "filter" not in st.session_state:
    st.session_state.filter = "Smooth"

# ---------- UI ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&display=swap');

.stApp {
    background: radial-gradient(circle at top, #1a001f, #000000);
    color: #ffe4f2;
    font-family: 'Fredoka', sans-serif;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 52px;
    font-weight: 600;
    letter-spacing: 1px;

    background: linear-gradient(90deg, #ff4ecd, #c084fc, #ff4ecd);
    background-size: 200% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: shimmer 3s linear infinite;
}

/* STAR */
.star {
    font-size: 52px;
    background: linear-gradient(45deg,#ff4ecd,#c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow: 0 0 15px rgba(255, 78, 205, 0.8);
}

/* SHIMMER ANIMATION */
@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* PANEL */
.panel {
    background: rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 102, 204, 0.25);
}

/* BUTTONS */
.stButton>button {
    border-radius: 999px;
    background: transparent;
    color: #ff66cc;
    border: 1px solid #ff66cc;
}

.stButton>button:hover {
    background: #ff66cc;
    color: white;
}

/* SLIDER */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #ff4ecd, #c084fc) !important;
}

/* UPLOADER */
[data-testid="stFileUploader"] {
    border: 1px dashed #ff66cc;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'><span class='star'>★</span> Smoothify</div>", unsafe_allow_html=True)

# ---------- FILTER (UNCHANGED) ----------
def beauty_filter(img, intensity):
    strength = intensity / 100

    smooth = cv2.bilateralFilter(img, d=25, sigmaColor=80, sigmaSpace=80)
    detail = cv2.subtract(img, cv2.GaussianBlur(img, (0,0), 3))

    result = cv2.addWeighted(smooth, 0.7 + 0.2*strength, detail, 0.3, 0)

    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    result = cv2.filter2D(result, -1, kernel)

    return result

# ---------- LAYOUT ----------
left, right = st.columns([1,1.2])

# ---------- LEFT ----------
with left:

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Filters")

    filters = ["Smooth", "Gaussian", "Median", "Blur", "Sharpen"]
    cols = st.columns(len(filters))

    for i, f in enumerate(filters):
        if cols[i].button(f):
            st.session_state.filter = f

    st.write(f"Selected: {st.session_state.filter}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Adjust")

    k = st.slider("Kernel Size", 3, 15, step=2)
    intensity = st.slider("Intensity", 0, 100, 80)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RIGHT ----------
with right:

    if file:
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        f = st.session_state.filter

        if f == "Smooth":
            output = beauty_filter(img, intensity)

        elif f == "Gaussian":
            output = cv2.GaussianBlur(img, (k*3, k*3), 0)

        elif f == "Median":
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            output = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        elif f == "Blur":
            output = cv2.blur(img, (k*4, k*4))

        elif f == "Sharpen":
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            output = cv2.filter2D(img, -1, kernel)

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        st.subheader("Before & After")

        c1, c2 = st.columns(2)
        c1.image(img, caption="Original", width=300)
        c2.image(output, caption="Processed", width=300)

        # DOWNLOAD
        result_bgr = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.png', result_bgr)

        st.download_button(
            "⬇ Download Image",
            buffer.tobytes(),
            file_name="smoothified.png"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### Preview\nUpload an image to see results ✨")
        st.markdown('</div>', unsafe_allow_html=True)