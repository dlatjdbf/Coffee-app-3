import streamlit as st
import requests
import base64
import json

# ----------------- 기본 설정 -----------------
st.set_page_config(page_title="AI 카페인 분석기 ☕", layout="centered")
st.title("☕ AI 기반 카페인 함유량 분석기")

# ----------------- 파일 업로드 -----------------
uploaded_file = st.file_uploader("음식 또는 음료 사진을 업로드하세요", type=["jpg", "png", "jpeg"])

# ----------------- API 키 확인 -----------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ API 키를 찾을 수 없습니다. .streamlit/secrets.toml 또는 Streamlit Cloud Secrets에 등록해 주세요.")
else:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    # ----------------- 업로드 시 실행 -----------------
    if uploaded_file:
        st.image(uploaded_file, caption="업로드한 이미지", use_container_width=True)

        # 이미지를 base64로 인코딩
        img_bytes = uploaded_file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # OpenAI Vision API 요청
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

        payload = {
            "model": "gpt-4o-mini",  # 이미지 인식 가능 모델
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 사진 속 음식 또는 음료를 인식하고, 카페인 함유 여부와 예상 함량(mg)을 알려줘."},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_base64}"}
                    ]
                }
            ]
        }

        with st.spinner("AI가 분석 중입니다..."):
            response = requests.post(url, headers=headers, json=payload)
            result_json = response.json()

        # ----------------- 응답 처리 -----------------
        if "choices" in result_json:
            result = result_json["choices"][0]["message"]["content"]
            st.success("AI 분석 결과")
            st.write(result)
        else:
            st.error("⚠️ OpenAI API 응답 오류가 발생했습니다.")
            st.json(result_json)
