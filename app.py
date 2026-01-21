import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# 1. 페이지 설정
st.set_page_config(page_title="어린이 바이브 코딩 놀이터", page_icon="🎨", layout="wide")

# 2. API 보안 설정 및 모델 로드 함수
def tool_setup():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secrets 설정에서 'GEMINI_API_KEY'를 입력해주세요.")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # 모델 설정 (안전 설정 포함하여 500 에러 방지)
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    # 모델 ID에 'models/' 접두사를 붙여 식별을 명확히 함
    return genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        generation_config=generation_config
    )

model = tool_setup()

# 3. UI 디자인
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .main-title { color: #FF6B6B; text-align: center; font-size: 40px; font-weight: bold; margin-bottom: 20px; }
    .input-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚀 어린이 바이브 코딩 놀이터</h1>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.markdown("### 💡 나의 아이디어 적기")
    q1 = st.text_input("1. 만들고 싶은 서비스 이름", placeholder="예: 우주 전쟁 게임")
    q2 = st.text_area("2. 꼭 있어야 하는 기능", placeholder="예: 화성인이 나타나면 클릭해서 잡아야 해")
    q3 = st.text_input("3. 전체적인 분위기", placeholder="예: 어두운 배경에 형광색 글자들")
    
    make_btn = st.button("마법의 앱 만들기 ✨")

# 4. 앱 생성 로직
if make_btn:
    if not (q1 and q2 and q3):
        st.warning("모든 칸을 채워주세요!")
    else:
        with st.spinner("AI 마법사가 서버와 통신 중입니다... (잠시만 기다려주세요)"):
            try:
                # 프롬프트 엔지니어링
                prompt = f"""
                Create a single-file HTML/CSS/JS application based on:
                - Name: {q1}
                - Features: {q2}
                - Design: {q3}
                
                Instructions:
                1. Use a modern and kid-friendly design.
                2. Return ONLY the code within a ```html code block.
                3. Ensure the app is fully functional and interactive.
                """
                
                # 콘텐츠 생성
                response = model.generate_content(prompt)
                
                if response.text:
                    # HTML 코드 추출
                    html_match = re.search(r'```html(.*?)```', response.text, re.DOTALL)
                    html_code = html_match.group(1).strip() if html_match else response.text
                    
                    with col_out:
                        st.subheader("🎮 실시간 결과물")
                        components.html(html_code, height=600, scrolling=True)
                        st.balloons()
                        
                        with st.expander("📝 개발자용 프롬프트 보기"):
                            st.code(response.text.split("```html")[0])
                else:
                    st.error("AI가 답변을 생성하지 못했습니다. 다시 한번 버튼을 눌러주세요.")

            except Exception as e:
                # 500 에러 등에 대한 상세 피드백
                st.error(f"⚠️ 서버 오류가 발생했습니다: {str(e)}")
                st.info("Tip: Google AI Studio의 일시적 과부하일 수 있습니다. 5~10초 후 다시 시도해 보세요.")

st.divider()
st.caption("Gemini 2.5 Flash 기반 | 문제가 지속되면 API 키의 할당량을 확인해 주세요.")
