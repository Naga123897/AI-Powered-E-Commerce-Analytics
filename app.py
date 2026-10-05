import streamlit as st
from src.llm_api import process_question


st.title("AI E-Commerce Analytics Assistant")

st.write("Ask a business question about the e-commerce data.")

question = st.text_input(
    "Ask your business question:"
)


if st.button("Ask Question"):

    if not question.strip():

        st.warning("Please enter a business question.")

    else:

        question_type, result_data, answer = process_question(question)

        if question_type is None:

            st.error(answer)

        else:

            st.subheader("Question Type")
            st.write(question_type)

            st.subheader("Verified Data")
            st.json(result_data)

            st.subheader("AI Answer")
            st.write(answer)