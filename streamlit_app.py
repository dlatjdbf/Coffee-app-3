import streamlit as st
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from PIL import Image
import numpy as np
import os

# ---------------------- 기본 설정 ----------------------
st.set_page_config(page_title="AI 카페인 분석기 (딥러닝)", layout="centered")
st.title("🤖 AI 카페인 분석기 (CNN 딥러닝 기반)")

MODEL_PATH = "caffeine_cnn_model.h5"

# ---------------------- 데이터 및 라벨 ----------------------
classes = ["coffee", "cola", "chocolate", "green_tea", "energy", "non_caffeine"]
caffeine_values = {
    "coffee": 120,
    "cola": 34,
    "chocolate": 9,
    "green_tea": 25,
    "energy": 80,
    "non_caffeine": 0
}

# ---------------------- CNN 모델 생성 ----------------------
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(len(classes), activation='softmax')
    ])
    model.compile(optimizer=Adam(0.001), loss="categorical_crossentropy", metrics=["accuracy"])
    return model

# ---------------------- 더미 데이터로 기본 학습 ----------------------
# (실제 데이터셋 없을 때 대비용 – 색상 기반 간이 학습)
def train_base_model():
    X, y = [], []
    base_colors = {
        "coffee": (90, 60, 40),
        "cola": (40, 40, 80),
        "chocolate": (120, 80, 60),
        "green_tea": (70, 110, 70),
        "energy": (220, 200, 60),
        "non_caffeine": (200, 200, 200)
    }

    for i, (label, rgb) in enumerate(base_colors.items()):
        for _ in range(200):
            arr = np.ones((64, 64, 3), dtype=np.uint8)
            noise = np.random.randint(-15, 15, size=(64, 64, 3))
            color = np.clip(arr * rgb + noise, 0, 255)
            X.append(color / 255.0)
            y.append(i)

    X = np.array(X)
    y = to_categorical(y, num_classes=len(classes))

    model = create_model()
    model.fit(X, y, epochs=8, batch_size=64, verbose=0)
    model.save(MODEL_PATH)
    return model

# ---------------------- 모델 불러오기 ----------------------
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    st.info("📚 AI 모델이 존재하지 않아 기본 학습을 시작합니다. (약 20초 소요)")
    model = train_base_model()
    st.success("✅ AI 모델 학습 완료!")

# ---------------------- Streamlit 파일 업로드 ----------------------
uploaded_file = st.file_uploader("음식 또는 음료 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

# ---------------------- 예측 ----------------------
def predict_caffeine(image):
    img = image.resize((64, 64)).convert("RGB")
    arr = img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    preds = model.predict(arr)
    idx = np.argmax(preds)
    label = classes[idx]
    confidence = round(preds[0][idx] * 100, 2)

    caffeine = caffeine_values[label]

    return label, caffeine, confidence

# ---------------------- 실행 ----------------------
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드한 이미지", use_container_width=True)

    with st.spinner("AI 딥러닝 모델이 이미지를 분석 중입니다... ⏳"):
        label, caffeine, confidence = predict_caffeine(img)

    st.success("✅ 분석 완료!")
    st.markdown(f"""
    **예측 결과:** {label}  
    **예상 카페인 함량:** {caffeine}mg  
    **AI 확신도:** {confidence}%  
    """)

    if confidence < 50:
        st.warning("⚠️ 이 이미지는 AI가 확신이 낮습니다. 더 명확한 사진을 업로드해보세요.")
else:
    st.info("사진을 업로드하면 CNN 딥러닝 AI가 카페인 함량을 예측합니다 ☕")
