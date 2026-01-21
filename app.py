import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="어린이 바이브 코딩 놀이터", page_icon="🎨", layout="wide")

# 어린이 친화적인 커스텀 스타일
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { 
        width: 100%; border-radius: 25px; height: 3em; 
        background: linear-gradient(45deg, #ff4b4b, #ff8a8a); 
        color: white; font-size: 20px; font-weight: bold; border: none;
    }
    .title-text { color: #4A90E2; text-align: center; font-family: 'Nanum Gothic', sans-serif; }
    .preview-box { border: 2px dashed #4A90E2; border-radius: 15px; padding: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. API 보안 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets 설정에서 'GEMINI_API_KEY'를 입력해주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 메인 화면 구성
st.markdown("<h1 class='title-text'>🚀 어린이 바이브 코딩 놀이터</h1>", unsafe_allow_html=True)
st.write("아이디어를 입력하면 AI가 바로 작동하는 웹앱을 만들어줘요!")

# 화면 분할 (입력창 | 결과창)
col_input, col_result = st.columns([1, 1.2])

with col_input:
    st.subheader("💡 상상을 적어보세요")
    
    q1 = st.text_input(
        "1. 어떤 웹서비스를 만들고 싶나요?",
        placeholder="예: 칭찬 스티커 게시판, 나만의 간식 도감"
    )
    
    q2 = st.text_area(
        "2. 필요한 기능은 무엇인가요?",
        placeholder="예: 버튼을 누르면 '참 잘했어요' 소리가 나야 해, 그림을 올릴 수 있으면 좋겠어"
    )
    
    q3 = st.text_input(
        "3. 디자인 느낌은 어떤가요?",
        placeholder="예: 노란색 배경에 귀여운 곰돌이 캐릭터가 가득했으면 좋겠어"
    )
    
    make_btn = st.button("마법의 앱 만들기 ✨")

# 4. AI 로직 및 실행
if make_btn:
    if not (q1 and q2 and q3):
        st.warning("세 가지 질문에 모두 답해줘야 마법이 시작돼요!")
    else:
        with st.spinner("AI 마법사가 코딩 중입니다... 🪄"):
            try:
                # 최신 안정화 모델 사용
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                # 프롬프트 구성: 전문가용 프롬프트와 미리보기용 HTML을 동시에 요청
                prompt_task = f"""
                당신은 어린이의 꿈을 현실로 만드는 마법사 코딩 선생님입니다.
                아래 입력값을 바탕으로 두 가지 결과물을 만드세요.

                [입력 데이터]
                - 주제: {q1}
                - 기능: {q2}
                - 디자인: {q3}

                [결과물 형식]
                1. 'Vibe Coding Prompt': Replit이나 Cursor 같은 도구에 넣을 아주 상세한 개발 지시서.
                2. 'Live Preview HTML': <html>, <style>, <script>가 포함된 '단 하나의 파일'로 작동하는 웹앱 코드.
                
                중요: 'Live Preview HTML' 코드는 반드시 ```html [코드] ``` 형식으로 감싸주세요.
                """
                
                response = model.generate_content(prompt_task)
                response_text = response.text
                
                # HTML 코드 추출
                html_match = re.search(r'```html(.*?)```', response_text, re.DOTALL)
                
                with col_result:
                    st.subheader("🎮 실시간 미리보기")
                    if html_match:
                        html_code = html_match.group(1).strip()
                        # HTML 렌더링
                        with st.container():
                            st.markdown("<div class='preview-box'>", unsafe_allow_html=True)
                            components.html(html_code, height=500, scrolling=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.success("짜잔! 왼쪽에서 만든 앱이 실제로 작동해요!")
                        
                        # 전문가용 프롬프트 제공
                        with st.expander("📝 더 멋진 앱으로 발전시키기 위한 '전문가 프롬프트'"):
                            st.info("이 내용을 복사해서 Replit Agent나 Cursor에 넣으면 진짜 개발자가 될 수 있어요!")
                            st.write(response_text.split("```html")[0]) # 코드 앞부분의 설명글만 출력
                            
                        # 코드 복사 기능
                        with st.expander("💻 원본 HTML 코드 보기"):
                            st.code(html_code, language="html")
                    else:
                        st.error("코드를 생성하는 중에 문제가 생겼어요. 다시 시도해볼까요?")
                        
                st.balloons()
                
            except Exception as e:
                st.error(f"오류가 발생했어요: {e}")

# 하단 안내
st.divider()
st.caption("Powered by Gemini 2.5 Flash | 어린이의 상상력이 코딩이 되는 공간")
