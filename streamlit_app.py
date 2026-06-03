import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/summarize-meeting"

st.set_page_config(
    page_title="Meeting Intelligence Assistant",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Meeting Intelligence Assistant")

st.markdown(
    "Analyze meeting transcripts and extract summaries, action items, and decisions."
)

transcript = st.text_area(
    "Paste Meeting Transcript",
    height=300
)

if st.button("Analyze Meeting"):

    if not transcript.strip():

        st.error("Please enter a meeting transcript")

    else:

        payload = {
            "transcript": transcript
        }

        with st.spinner("Analyzing meeting..."):

            response = requests.post(
                API_URL,
                json=payload
            )

        if response.status_code == 200:

            result = response.json()

            data = result["data"]

            st.success("Analysis Complete")

            st.subheader("Meeting Summary")

            st.write(data["meeting_summary"])

            st.subheader("Action Items")

            for item in data["action_items"]:

                st.write(item)

            st.subheader("Key Decisions")

            for decision in data["key_decisions"]:

                st.write("•", decision)

            st.subheader("Processing Time")

            st.write(
                f"{data['processing_time_seconds']} seconds"
            )

        else:

            st.error(
                response.json()
            )