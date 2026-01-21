import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# 1. 페이지 설정
st.set_page_config(page_title="어린이 바이브 코딩 놀이터", page_icon="🎨", layout="wide")

# 2. API 보안 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets 설정에서 'GEMINI_API_KEY'를 입력해주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. UI 스타일링
st.markdown("""
    <style>
    .stApp { background-color: #f0faff; }
    .main-title { color: #2E86C1; text-align: center; font-size: 35px; font-weight: bold; }
    .vibe-card { background-color: #ffffff; padding: 15px; border-radius: 15px; border-left: 5px solid #FF8C00; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚀 어린이 바이브 코딩 놀이터</h1>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("💡 상상력 채우기")
    q1 = st.text_input("1. 무엇을 만들고 싶나요?", placeholder="예: 칭찬 스티커 보드")
    q2 = st.text_area("2. 어떤 기능이 필요해요?", placeholder="예: 버튼을 누르면 별이 나타나고 축하 음악이 나와야 해")
    q3 = st.text_input("3. 어떤 색깔이 좋아요?", placeholder="예: 노란색과 하늘색")
    
    make_btn = st.button("마법의 앱 만들기 ✨")

# 4. 앱 생성 로직
if make_btn:
    if not (q1 and q2 and q3):
        st.warning("모든 칸을 채워주세요!")
    else:
        with st.spinner("AI 마법사 선생님이 코딩과 프롬프트를 만들고 있어요..."):
            try:
                # 모델 설정 (gemini-2.5-flash)
                model = genai.GenerativeModel("models/gemini-2.5-flash")
                
                # 초등학생 맞춤형 요청 프롬프트
                prompt = f"""
                입력 데이터: 주제({q1}), 기능({q2}), 디자인({q3})
                
                당신은 어린이 코딩 선생님입니다. 다음 두 가지를 작성하세요:

                1. [Vibe Prompt]: Replit Agent나 Cursor 같은 도구에 그대로 복사해서 넣을 수 있는 개발 지시서입니다. 
                   초등학생이 이해할 수 있게 "선생님, 저는 ~를 만들고 싶어요. ~기능을 넣어주세요"라는 말투로 아주 구체적으로 적어주세요.
                
                2. [Live HTML]: 위 기능을 실제로 구현한 단일 HTML/CSS/JS 코드.
                
                형식:
                [Vibe Prompt]
                (내용 작성)
                
                [Live HTML]
                ```html
                (코드 작성)
                ```
                """
                
                response = model.generate_content(prompt)
                full_response = response.text
                
                # 데이터 분리 (정규식 및 문자열 처리)
                vibe_prompt_part = ""
                html_code = ""
                
                if "[Vibe Prompt]" in full_response:
                    vibe_prompt_part = full_response.split("[Vibe Prompt]")[1].split("[Live HTML]")[0].strip()
                
                html_match = re.search(r'```html(.*?)```', full_response, re.DOTALL)
                if html_match:
                    html_code = html_match.group(1).strip()

                with col_out:
                    st.subheader("🎮 실시간 미리보기")
                    if html_code:
                        components.html(html_code, height=500, scrolling=True)
                    else:
                        st.info("미리보기를 준비 중입니다.")
                    
                    st.divider()
                    
                    # 초등학생 수준의 바이브 코딩 프롬프트 노출
                    st.subheader("📝 친구를 위한 '코딩 마법 주문서'")
                    st.markdown(f"""
                    <div class='vibe-card'>
                        {vibe_prompt_part if vibe_prompt_part else "주문서를 만드는 중이에요!"}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info("위 '주문서' 내용을 복사해서 Replit Agent에 넣으면 이 앱을 진짜로 가질 수 있어요!")
                    
                    with st.expander("💻 실제 코드 구경하기"):
                        st.code(html_code, language="html")
                        
                st.balloons()

            except Exception as e:
                st.error(f"오류가 발생했어요. 다시 시도해볼까요? (에러: {e})")

st.divider()
st.caption("Gemini 2.5 Flash 기반 | 아이들의 첫 코딩 경험을 응원합니다!")
