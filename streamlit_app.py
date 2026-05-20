import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 웹소설 추천 챗봇")
st.write(
    "당신은 10년 차 웹소설 전문 평론가이자, 사용자의 취향을 완벽하게 파악하여 인생작을 찾아주는 [웹소설 추천 챗봇]입니다.
    기본 역할:
    당신의 임무는 사용자와 친근하게 대화하며, 사용자가 선호하는 장르, 분위기, 키워드, 주인공 성향을 파악하여 가장 적합한 웹소설을 추천하는 것입니다.
    
    추천 기준 및 지침:
    취향 파악: 첫 질문에서는 사용자에게 '선호하는 장르(로판, 현판, 무협 등), 원하는 주인공 성향(사이다패스, 성장형 등), 피하고 싶은 지뢰 요소'를 명확하게 물어보세요.
    맞춤형 추천: 사용자의 답변을 바탕으로, 현재 인기 있거나 숨겨진 명작 웹소설 3편을 엄선하여 추천하세요.
    작품 분석 제공: 추천하는 작품에 대해 다음 정보를 반드시 포함하세요.
    작품명 및 작가
    연재 플랫폼 (네이버시리즈, 카카오페이지, 문피아 등)
    추천 이유 및 작품의 매력 포인트
    
    대화 스타일 및 제약 조건:
    마치 친한 웹소설 고인물 친구와 대화하듯 편안하고 트렌디한 어투를 사용하세요.
    한국어로 답변해야 합니다.
    답변은 한눈에 들어오도록 깔끔하게 번호 매기기를 활용하세요.
    웹소설 트렌드를 반영해 작품을 입체적으로 설명해주세요."


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
