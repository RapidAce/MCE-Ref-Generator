import streamlit as st
import json
import os
import pandas as pd
from datetime import date

# File to store data
data_file = 'reference_data.json'

# Load or initialize data
def load_data():
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {"last_number": 3458, "records": []}
    else:
        return {"last_number": 3458, "records": []}

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

# Streamlit App
st.title("🔧 MCE Reference Generator")

# Load data
store = load_data()

# User Authentication (Simple Identity Field)
st.sidebar.header("User Login")
user_identity = st.sidebar.text_input("Enter your username")
if not user_identity:
    st.warning("Please enter your username in the sidebar to use the tool.")
    st.stop()

# Input Form
with st.form("reference_form"):
    st.subheader("Enter Tender/Project Details")

    category = st.selectbox("Select Category", ["MCE", "ELEC", "CIVIL", "OTHER"])
    project_name = st.text_input("Project Name")
    description = st.text_area("Project Description")
    rfq_number = st.text_input("RFQ / Tender Number")
    issue_date = st.date_input("Issue Date", value=date.today())
    deadline_date = st.date_input("Deadline Date")

    submitted = st.form_submit_button("Generate Reference Number")

    if submitted:
        if not all([project_name, description, user_identity, rfq_number]):
            st.error("Please fill in all fields.")
        else:
            store["last_number"] += 1
            ref_num = f"{category}-{store['last_number']}"

            entry = {
                "reference_number": ref_num,
                "category": category,
                "project_name": project_name,
                "description": description,
                "user": user_identity,
                "rfq_number": rfq_number,
                "issue_date": str(issue_date),
                "deadline_date": str(deadline_date)
            }

            store["records"].append(entry)
            save_data(store)

            st.success(f"✅ Reference Number Generated: **{ref_num}**")
            st.json(entry)

            st.download_button(
                label="Download Entry as JSON",
                data=json.dumps(entry, indent=4),
                file_name=f"{ref_num}.json",
                mime="application/json"
            )

# Record Viewer Section
st.markdown("---")
st.subheader("📋 View All Records")

if store["records"]:
    df = pd.DataFrame(store["records"])

    # Filter by project name or user
    with st.expander("🔍 Filter Records"):
        filter_project = st.text_input("Filter by Project Name")
        filter_user = st.text_input("Filter by User")

        if filter_project:
            df = df[df['project_name'].str.contains(filter_project, case=False, na=False)]
        if filter_user:
            df = df[df['user'].str.contains(filter_user, case=False, na=False)]

    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download All Records as CSV",
        data=csv,
        file_name='mce_records.csv',
        mime='text/csv'
    )
else:
    st.info("No records available yet.")
