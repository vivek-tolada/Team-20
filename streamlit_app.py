import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"  # backend running here

st.set_page_config(page_title="DevOps Copilot", layout="wide")
st.title("🤖 DevOps Copilot — AI-Powered DevOps Assistant")

tabs = st.tabs(["Generate Templates", "PR Reviewer", "Documentation", "Chat Assistant"])


# ---------------------------------------------------------
# TAB 1 — TEMPLATE GENERATOR
# ---------------------------------------------------------
with tabs[0]:
    st.header("Generate DevOps Templates")

    project_type = st.selectbox("Select Project Type", ["python", "nodejs", "java"])
    artifact = st.selectbox("Select Artifact", ["dockerfile", "github_actions", "k8s_deployment"])

    details_text = st.text_area("Additional Details (JSON)", "{}")

    if st.button("Generate Template"):
        # Parse JSON safely
        try:
            details = json.loads(details_text)
        except:
            st.error("Invalid JSON format. Please enter proper JSON.")
            details = {}

        payload = {
            "project_type": project_type,
            "artifact": artifact,
            "details": details
        }

        with st.spinner("Generating template..."):
            try:
                response = requests.post(f"{API_URL}/api/generate/template", json=payload)
                if response.ok:
                    data = response.json()
                    st.subheader("Generated Output:")
                    st.code(data["content"], language="dockerfile" if artifact == "dockerfile" else "yaml")

                    if "warnings" in data and data["warnings"]:
                        st.warning(data["warnings"])
                else:
                    st.error("Server Error: " + response.text)
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")


# ---------------------------------------------------------
# TAB 2 — PR REVIEWER
# ---------------------------------------------------------
with tabs[1]:
    st.header("AI Pull Request Reviewer")

    diff_text = st.text_area("Paste PR Diff Here", height=300)

    if st.button("Review PR"):
        payload = {"diff": diff_text}

        with st.spinner("Reviewing PR..."):
            response = requests.post(f"{API_URL}/api/review/pr", json=payload)

        if response.ok:
            data = response.json()
            st.subheader("AI Review Result")
            st.text_area("Review:", value=data["review"], height=300)
        else:
            st.error(response.text)


# ---------------------------------------------------------
# TAB 3 — DOCUMENTATION GENERATOR
# ---------------------------------------------------------
with tabs[2]:
    st.header("Generate README Documentation")

    repo_summary = st.text_area("Paste Folder Structure or Summary")

    if st.button("Generate README"):
        payload = {"repo_summary": repo_summary}

        with st.spinner("Generating README..."):
            response = requests.post(f"{API_URL}/api/generate/docs", json=payload)

        if response.ok:
            st.subheader("Generated README.md")
            st.code(response.json()["readme"], language="markdown")
        else:
            st.error(response.text)


# ---------------------------------------------------------
# TAB 4 — CHAT ASSISTANT
# ---------------------------------------------------------
with tabs[3]:
    st.header("DevOps Chat Assistant")

    message = st.text_input("Ask anything about DevOps, CI/CD, Docker, Terraform, Kubernetes...")

    if st.button("Ask"):
        payload = {"message": message}

        with st.spinner("Thinking..."):
            response = requests.post(f"{API_URL}/api/chat", json=payload)

        if response.ok:
            st.subheader("AI Response")
            st.write(response.json()["reply"])
        else:
            st.error(response.text)
