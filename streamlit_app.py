import streamlit as st
import requests

st.title("HR CV–Job Matching")

# File upload
job_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
cv_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

st.divider()

if st.button("Match"):
    if not job_file or not cv_file:
        st.warning("Please upload both Job Description and CV files.")
    else:
        webhook_url = "https://anjanette-venular-vivian.ngrok-free.dev/webhook/0f152550-ac57-4497-aab2-2f4f253dfaba"

        files = {
            "job_file": (job_file.name, job_file.getvalue(), "application/pdf"),
            "cv_file": (cv_file.name, cv_file.getvalue(), "application/pdf")
        }

        with st.spinner("Matching CV against Job Description..."):
            try:
                response = requests.post(webhook_url, files=files)
                response.raise_for_status()
                result_json = response.json()

                st.success("Matching complete!")

                # ✅ Extract the actual result text
                match_text = result_json[0].get("result", "No result returned.")

                # ✅ Pretty display
                st.subheader("Matching Result")
                st.markdown(match_text)

                # Optional: raw JSON for debugging
                with st.expander("Show raw JSON response"):
                    st.json(result_json)

            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with n8n: {e}")
