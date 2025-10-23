import streamlit as st
import datetime
import calendar
import json
import os

# ------------------- 기본 설정 -------------------
KST = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(KST).date()
st.set_page_config(page_title="카페인 관리 앱", layout="centered")

# ------------------- 데이터 불러오기 -------------------
DATA_FILE = "data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        st.session_state.data = json.load(f)
else:
    st.session_state.data = {}

# ------------------- 상태 초기화 -------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "intake_input" not in st.session_state:
    st.session_state.intake_input = 0
if "selected_products" not in st.session_state:
    st.session_state.selected_products = []
if "selected_article" not in st.session_state:
    st.session_state.selected_article = None

# ------------------- 아카이브 글 데이터 -------------------
archive_articles = {
    "카페인의 인체 작용과 부작용, 그리고 개인차와 청소년 주의사항": """(중략 — 이전에 작성한 내용 그대로)""",
    "커피의 카페인 함량이 일정하지 않다고?": """(중략 — 이전에 작성한 내용 그대로)"""
}

# ------------------- 홈 화면 -------------------
if st.session_state.page == "home":
    st.title("☕ 카페인 관리 앱")
    st.write("기능을 선택하세요.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 카페인 달력", use_container_width=True):
            st.session_state.page = "calendar"
    with col2:
        if st.button("📚 카페인 아카이브", use_container_width=True):
            st.session_state.page = "archive"

# ------------------- 카페인 달력 -------------------
elif st.session_state.page == "calendar":
    st.title("📅 카페인 달력")
    st.write("목표 섭취량을 설정하고 달성 여부를 기록하세요.")

    # 현재 연도 / 월
    year = today.year
    month = st.selectbox("월 선택", range(1, 13), index=today.month - 1, format_func=lambda x: f"{x}월")

    # 달력 생성
    month_days = calendar.monthrange(year, month)[1]
    cols = st.columns(7)
    for i, day in enumerate(range(1, month_days + 1)):
        col = cols[i % 7]
        with col:
            key = f"{year}-{month:02d}-{day:02d}"
            entry = st.session_state.data.get(key)
            label = f"{day}일"
            if entry:
                label += f"\n{entry['intake']}mg {'✅' if entry['achieved'] else '❌'}"
            if st.button(label, key=f"btn_{key}"):
                st.session_state.selected_date = key
                st.session_state.intake_input = 0
                st.session_state.selected_products = []

    # 날짜 클릭 시 입력창
    if "selected_date" in st.session_state:
        date = st.session_state.selected_date
        st.markdown("---")
        st.subheader(f"{date} 기록")

        # 목표 섭취량 입력
        goal = st.number_input("목표 섭취량 (mg)", min_value=0, step=10, key="goal_input")

        # 제품 목록
        products = {
            "몬스터 에너지 355ml": 100,
            "레드불 에너지 드링크 355ml": 88.75,
            "핫식스 더킹 파워 355ml": 100,
            "핫식스 더킹 크러쉬피치 355ml": 100,
            "핫식스 더킹 퍼플그레이프 355ml": 100,
            "핫식스 더킹 제로 355ml": 100,
            "핫식스 더킹 러쉬 355ml": 100,
            "핫식스 더킹 포스 355ml": 100
        }

        # 제품 선택 및 자동 추가
        selected_product = st.selectbox("제품 선택", ["선택 안 함"] + list(products.keys()), key="product_select")
        if selected_product != "선택 안 함":
            if st.button("선택한 제품 추가"):
                caffeine_value = products[selected_product]
                st.session_state.selected_products.append((selected_product, caffeine_value))
                st.session_state.intake_input += caffeine_value
                st.success(f"{selected_product} 추가됨 (+{caffeine_value}mg)")

        # ------------------- 수동 입력 추가 -------------------
        st.markdown("---")
        st.write("직접 mg 단위로 추가하기")
        manual_value = st.number_input("직접 입력 (mg)", min_value=0, step=10, key="manual_add_value")
        if st.button("직접 추가"):
            if manual_value > 0:
                st.session_state.selected_products.append((f"수동 입력 {manual_value}mg", manual_value))
                st.session_state.intake_input += manual_value
                st.success(f"수동 입력으로 +{manual_value}mg 추가됨")

        # ------------------- 결과 표시 -------------------
        if st.session_state.selected_products:
            st.write("### 오늘 추가한 항목")
            for name, mg in st.session_state.selected_products:
                st.write(f"- {name}: {mg}mg")
            st.metric(label="총 섭취량", value=f"{st.session_state.intake_input} mg")

        # 저장 / 취소 / 홈으로
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("저장"):
                achieved = st.session_state.intake_input <= goal
                st.session_state.data[date] = {
                    "goal": goal,
                    "intake": st.session_state.intake_input,
                    "achieved": achieved,
                    "products": st.session_state.selected_products.copy()
                }
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(st.session_state.data, f, ensure_ascii=False, indent=2)
                del st.session_state.selected_date
                st.success(f"{date} 기록이 저장되었습니다!")
        with col2:
            if st.button("취소"):
                del st.session_state.selected_date
        with col3:
            if st.button("🏠 홈으로"):
                st.session_state.page = "home"
                if "selected_date" in st.session_state:
                    del st.session_state.selected_date

    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.session_state.page = "home"

# ------------------- 카페인 아카이브 -------------------
elif st.session_state.page == "archive":
    st.title("📚 카페인 아카이브")

    # 본문이 선택되지 않았을 때 → 목록 화면
    if st.session_state.selected_article is None:
        st.write("카페인 관련 정보를 선택하세요:")
        for title in archive_articles.keys():
            if st.button(title, use_container_width=True):
                st.session_state.selected_article = title
                st.experimental_rerun()

        st.markdown("---")
        if st.button("🏠 홈으로 돌아가기", use_container_width=True):
            st.session_state.page = "home"

    # 본문이 선택된 상태 → 글 보기 화면
    else:
        title = st.session_state.selected_article
        st.header(title)
        st.markdown(archive_articles[title])
        st.markdown("---")
        if st.button("⬅ 목록으로 돌아가기"):
            st.session_state.selected_article = None
            st.experimental_rerun()

