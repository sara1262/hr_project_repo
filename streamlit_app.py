import streamlit as st
import requests

# Streamlit UI
st.title("HR CV-Job Matching")

# File upload
job_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
cv_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

if st.button("Match"):
    if not job_file or not cv_file:
        st.warning("Please upload both Job Description and CV files.")
    else:
        # Send files to n8n webhook
        webhook_url = "http://192.168.142.11:5678/webhook/7f7fe48f-2ca2-449d-b6b5-6f84a032f8e7"  # replace with your webhook URL
        files = {
            "job_file": (job_file.name, job_file.getvalue(), "application/pdf"),
            "cv_file": (cv_file.name, cv_file.getvalue(), "application/pdf")
        }

        with st.spinner("Matching..."):
            try:
                response = requests.post(webhook_url, files=files)
                response.raise_for_status()
                result_json = response.json()
                st.success("Matching complete!")
                st.json(result_json)  # Display JSON result nicely
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with n8n: {e}")
