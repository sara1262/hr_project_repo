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
        webhook_url = "https://discreditable-northeastwardly-stanford.ngrok-free.dev:5678/webhook-test/6003c9e3-7a38-4fff-8344-8afed6546527"

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

                # ✅ Extract first object from response array
                result = result_json[0]

                # ---- UI DISPLAY ----

                st.subheader("Candidate Evaluation")

                # Match score
                st.metric("Match Score", f"{result.get('match_score', 'N/A')} / 10")

                # Summary
                st.write("### Summary")
                st.write(result.get("summary", "No summary available."))

                # Matching reason
                st.write("### Matching Reason")
                st.write(result.get("matching_reason", "No reason provided."))

                # Key skills
                st.write("### Key Skills")
                skills = result.get("key_skills", [])
                if skills:
                    for skill in skills:
                        st.markdown(f"- {skill}")
                else:
                    st.write("No skills listed.")

                # Recommendation
                st.write("### Recommendation")
                st.success(result.get("recommendation", "No recommendation provided."))


            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with n8n: {e}")
