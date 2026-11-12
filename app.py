import streamlit as st
from src.llm_api import process_question


st.title("AI E-Commerce Analytics Assistant")
st.write("Ask a business question about the e-commerce data.")

question = st.text_input("Ask your business question:")

if st.button("Ask Question"):
    if not question.strip():
        st.warning("Please enter a business question.")
    else:
        with st.spinner("Retrieving verified data and generating an AI insight..."):
            question_type, result_data, insight, usage_data, error = process_question(question)

        if error:
            st.error(error)
        else:
            st.subheader("Question Type")
            st.write(question_type)

            st.subheader("Verified Data from MySQL")
            st.json(result_data)

            st.subheader("AI-Generated Insight")
            st.write(insight.summary)

            st.markdown("**Key Points**")
            for point in insight.key_points:
                st.markdown(f"- {point}")

            st.markdown("**Recommendation**")
            st.write(insight.recommendation)

            if usage_data:
                with st.expander("Token Usage and Estimated API Cost"):
                    st.write("Input tokens:", usage_data["input_tokens"])
                    st.write("Output tokens:", usage_data["output_tokens"])
                    st.write("Total tokens:", usage_data["total_tokens"])
                    st.write("Cached input tokens:", usage_data["cached_input_tokens"])
                    st.write(f"Input cost: ${usage_data['input_cost_usd']:.10f}")
                    st.write(f"Output cost: ${usage_data['output_cost_usd']:.10f}")
                    st.write(f"Total estimated cost: ${usage_data['total_cost_usd']:.10f}")
                    st.caption(usage_data["pricing_note"])
