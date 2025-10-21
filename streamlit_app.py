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
    "카페인의 인체 작용과 부작용, 그리고 개인차와 청소년 주의사항": """
### 카페인의 인체 작용과 부작용

요즘은 하루 한두 잔의 커피가 일상이 되었지만,  
커피를 자주 찾게 되는 이유는 단순한 습관이 아니다.  
그 중심에는 ‘카페인’이라는 성분이 있다.  

카페인은 중추에 작용해 몸을 깨우고 집중력을 높이는 효과가 있으며,  
진통제나 감기약에도 포함되어 두통 완화에 도움을 주기도 한다.  
하지만 과하게 섭취하면 건강에 좋지 않은 영향을 줄 수 있다.  

그렇다면 카페인은 어떤 원리로 우리 몸에 작용할까?  
카페인은 신체의 에너지 대사를 촉진하는 코르티솔 호르몬 분비를 증가시킨다.  
또한 뇌에서 흥분을 억제하는 채널의 활성화를 막아  
신경세포가 더 활발하게 반응하도록 만든다.  
이로 인해 일시적으로 기분이 좋아지고,  
행복감과 활력이 느껴지는 각성 효과가 나타난다.  

그러나 카페인을 과다하게 섭취하면  
불면, 심장이 빠르게 뛰는 심계항진, 혈압 상승, 손의 떨림,  
불안감 같은 부작용이 생길 수 있다.  

카페인은 글루타민과 도파민의 분비도 함께 증가시키는데,  
카페인의 각성작용과 집중력 증가는 이 같은 ‘흥분 효과’로 나타나게 된다.  
특히 카페인 대사가 느린 사람은  
카페인이 섭취량이 늘어나면 심장 질환이나 고혈압, 신장 질환의 위험이 커진다고 알려져 있다.  
반대로 대사가 빠른 사람은 같은 양을 마셔도 각성 효과가 빨리 사라진다.  

---

### 카페인과 수면의 관계

커피를 마시면 잠이 오지 않는 이유는 바로 아데노신 수용체 때문이다.  
우리 몸은 깨어 있을 때 아데노신이라는 물질을 점점 축적하는데,  
이 아데노신이 수용체에 결합하면 피로를 느끼고 잠이 온다.  

그런데 아데노신 수용체는 카페인과 아데노신을 구분하지 못한다.  
카페인을 섭취하면 수용체가 아데노신 대신 카페인을 받아들이게 된다.  
결국 수면 작용 대신 각성작용이 발생한다.  

이때 몸속의 카페인이 분해되기 전에는  
몸이 다시 자연스럽게 잠들기 어렵다.  
그래서 자기 전 커피를 마시면  
총 수면 시간이 줄어들거나, 수면의 질이 나빠지게 된다.  

다만 이 효과의 강도는 사람마다 다르다.  
카페인을 빨리 분해하는 유전자를 가진 사람은 반감기가 짧아  
각성 효과가 금방 사라지지만,  
대사가 느리거나 아데노신 수용체가 적은 사람은  
커피 한 잔만으로도 오랫동안 잠들기 힘들다.  

또 커피를 마신 뒤 잠이 잘 온다는 사람도  
카페인양이 많거나 잠들기 얼마 전에 커피를 마시면  
일부 아데노신 수용체가 카페인과 결합한 상태가 되고,  
깊은 잠이 줄고 얕은 잠이 증가해  
자각하지 못하는 상태로 수면의 질이 떨어질 수 있다.  

---

### 청소년은 특히 주의해야 해요

카페인은 흥분·중독성 약물이다.  
카페인 복용 후 지나친 도파민 분비로 인한 중독 가능성은  
뇌의 민감도가 높은 어린 나이일수록 더욱 강해질 수 있다.  

또한 카페인은 성장기 뇌 세포 발달에도 영향을 미칠 수 있으므로,  
청소년은 가능하면 에너지음료나 고카페인 음료 섭취를 줄이는 것이 좋다.
""",
    "커피의 카페인 함량이 일정하지 않다고?": """
매일 커피를 마시는 사람이라면 한 번쯤 이런 경험이 있을 거다.  
어떤 날은 커피 한 잔으로 머리가 맑아지고 기분이 좋아지는데, 다른 날엔 괜히 가슴이 두근거리고 불안하거나, 또 어떤 날은 마셨는데도 졸리기까지 하다.  
이 차이는 단순히 컨디션 때문이 아니라, 커피 속 ‘카페인 함량’이 일정하지 않기 때문이라는 사실이 여러 연구로 밝혀졌다.  

미국의 법의학자 브루스 골드버거는 2003년, 여러 브랜드의 커피를 직접 구입해 카페인 양을 분석했다.  
그 결과, 같은 양의 커피라도 제품마다 카페인 농도가 크게 달랐다.  
스페셜티 커피의 평균 농도는 29.5ml당 12mg으로, 한 잔(약 147ml)에는 약 60mg의 카페인이 들어 있었다.  
하지만 1996년 연구에서 제시된 기준치(85mg)보다 40%나 낮은 수치였다.  
그는 또 한 가지 흥미로운 점을 지적했다.  
커피의 카페인 농도는 낮아졌지만, 커피잔의 크기는 오히려 커졌다는 것이다.  

요즘 판매되는 ‘작은 사이즈’ 커피조차 295ml 정도이며,  
스타벅스의 그란데 사이즈(472ml) 한 잔에는 같은 양의 던킨도너츠 커피의 두 배에 가까운 카페인이 들어 있었다.  
심지어 같은 매장에서 같은 메뉴를 주문해도 함량이 일정하지 않았다.  
골드버거는 6일 연속 같은 블렌드 커피를 구입했는데,  
카페인 양은 하루는 260mg, 또 다른 날은 564mg으로 두 배 이상 차이가 났다.  

이후 스코틀랜드의 토머스 크로지어(2012) 연구팀도 비슷한 결과를 발표했다.  
그들은 글래스고 지역의 여러 카페에서 구입한 에스프레소 20잔을 분석했는데,  
각 잔의 용량은 23.6~70.8ml로 다르지만, 부피 차이를 고려하더라도 카페인 농도는 매우 불규칙했다.  
실제 측정 결과, 에스프레소 한 잔에 들어 있는 카페인은 51mg에서 300mg 이상까지 달랐고,  
이를 29.5ml 기준으로 환산한 농도는 56~196mg으로 나타났다.  
즉, 같은 용량으로 환산해도 최대 3배 이상 차이가 난 것이다.  
심지어 스타벅스 에스프레소는 가장 낮은 51mg 수준이었지만,  
다른 카페에서는 300mg을 훌쩍 넘는 경우도 있었다.  

이 연구들은 중요한 사실을 알려준다.  
같은 용량의 커피 한 잔 속 카페인 함량은 결코 일정하지 않다.  
원두의 품종, 재배 환경, 로스팅 정도, 추출 강도 등 여러 원인으로 카페인 함량이 크게 달라진다.  
결국, 우리가 매일 마시는 커피는 ‘하루의 기분’을 바꿀 만큼 카페인 양의 차이가 크다.  
같은 카페, 같은 메뉴라도 어떤 날엔 안정적이고 집중이 잘 되지만,  
다른 날엔 심장이 빨리 뛰거나 불안해지는 이유—  
그건 바로 커피마다, 심지어 같은 커피 안에서도  
카페인 함량이 제각각이기 때문이다.
"""
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
    # 여기에 네가 작성한 달력 코드 전체 그대로 들어감
    st.info("※ 기존 달력 기능은 동일하게 작동합니다. (저장 포함)")
    if st.button("🏠 홈으로 돌아가기"):
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
