import streamlit as st


def text_area(name: str, placeholder: str = ""):
    name_split = name.lower().split()
    key = "_".join(name_split)

    st.subheader(body=name)
    st.text_area(
        label=name,
        label_visibility="collapsed",
        key=key,
        placeholder=placeholder,
    )
