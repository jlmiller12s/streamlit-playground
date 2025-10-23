import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(page_title="Streamlit Workfront Sandbox", layout="wide")

# --- HEADER ---
st.title("Streamlit + Workfront Sandbox")

st.write("""
Streamlit supports a wide range of data visualizations, including 
[Plotly, Altair, and Bokeh charts](https://docs.streamlit.io/develop/api-reference/charts). 
And with over 20 input widgets, you can easily make your data interactive!
""")

# --- CHART SECTION ---
all_users = ["Alice", "Bob", "Charly"]

with st.container(border=True):
    users = st.multiselect("Users", all_users, default=all_users)
    rolling_average = st.toggle("Rolling average")

np.random.seed(42)
data = pd.DataFrame(np.random.randn(20, len(users)), columns=users)
if rolling_average:
    data = data.rolling(7).mean().dropna()

tab1, tab2 = st.tabs(["Chart", "Dataframe"])
tab1.line_chart(data, height=250)
tab2.dataframe(data, height=250, use_container_width=True)

# --- API TEST SECTION ---
st.markdown("---")
st.header("API Tests")

# ---- JSONPLACEHOLDER TEST ----
st.subheader("Public API Test (No Auth)")
if st.button("Fetch Tasks (JSONPlaceholder)"):
    try:
        r = requests.get("https://jsonplaceholder.typicode.com/todos")
        r.raise_for_status()
        data = r.json()[:10]  # limit results
        st.success("✅ Success! Showing sample data:")
        st.dataframe(data)
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ---- WORKFRONT MOCK TEST ----
st.subheader("Workfront-style API Test")
url = "https://jsonplaceholder.typicode.com/users"  # placeholder for real Workfront endpoint
params = {"fields": "name,email,username"}  # simulate Workfront query

if st.button("Fetch Workfront Users (Simulated)"):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        users = response.json()
        st.success("✅ Retrieved Workfront-style data successfully.")
        st.dataframe(users)
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ---- REAL WORKFRONT CALL (Optional, if token added) ----
st.subheader("Real Workfront API Test (Requires Valid Token)")
if "WF_TOKEN" in st.secrets:
    if st.button("Fetch Real Workfront Tasks"):
        try:
            headers = {"Authorization": f"Bearer {st.secrets['WF_TOKEN']}"}
            r = requests.get(
                "https://yourdomain.my.workfront.com/attask/api/v16.0/task/search",
                headers=headers
            )
            r.raise_for_status()
            wf_data = r.json()
            st.success("✅ Connected to Workfront successfully!")
            st.json(wf_data)
        except Exception as e:
            st.error(f"❌ Workfront Error: {e}")
else:
    st.info("ℹ️ Add your Workfront API token to Streamlit secrets as `WF_TOKEN` to enable this test.")
