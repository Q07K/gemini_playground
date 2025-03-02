import streamlit as st

from component import input_component
from llms import gemini
from utils.env import set_env

st.header("Gemini Playground")


api_key_input, model_select = st.columns(2)

if api_key := api_key_input.text_input(
    label="API KEY",
    key="api_key",
    type="password",
):
    set_env(key="api_key", value=api_key)
flag = gemini.valid_api_key()

if flag:
    model_select.selectbox(
        label="Models",
        # options=gemini.get_model_list(),
        options=gemini.get_model_list_legacy(),
        key="model_name",
    )

left, right = st.columns(2)
with left:
    input_component.text_area(
        name="System Prompt",
        placeholder="AI에게 부여할 역할을 설명해주세요.",
    )
with right:
    input_component.text_area(
        name="Document",
        placeholder="AI가 참고할 내용을 작성해주세요.",
    )

st.divider()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if flag:
    if query := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            stream = gemini.generate(
                model_name=st.session_state.model_name,
                system_prompt=st.session_state.system_prompt,
                document=st.session_state.document,
                query=query,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
