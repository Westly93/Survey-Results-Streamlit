import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide", page_icon=":bar_chat:",
                   page_title="Survey Results")
hide_streamlit_styles = """
<style>
#MainMenu{
    visibility: hidden;
}
footer{
    visibility: hidden;
}
header{
    visibility: hidden;
}
</style>
"""

st.markdown(hide_streamlit_styles, unsafe_allow_html=True)
st.header(":bar_chart: Survey Results 2021")
excel_file = "./data/Survey_Results.xlsx"

sheet_name = "DATA"

df = pd.read_excel(
    io=excel_file,
    sheet_name=sheet_name,
    usecols="B:D",
    header=3,
)

df_participants = pd.read_excel(
    io=excel_file,
    sheet_name=sheet_name,
    usecols="F:G",
    header=3
)
df_participants.dropna(inplace=True)

department = df["Department"].unique().tolist()
ages = df["Age"].unique().tolist()

age_selection = st.slider(
    "Age",
    min_value=min(ages),
    max_value=max(ages),
    value=(min(ages), max(ages)),
)

department_selection = st.multiselect(
    "Department: ", department, default=department)

# Filter dataframe based on selection
mask = (df["Age"].between(*age_selection)
        ) & (df["Department"].isin(department_selection))
number_of_results = df[mask].shape[0]

st.markdown(f"*Available Results: {number_of_results}*")

# Group dataframe after selection

df_grouped = df[mask].groupby("Rating").count()[["Age"]]

df_grouped = df_grouped.rename(columns={"Age": "Votes"})

df_grouped = df_grouped.reset_index()

bar_chart = px.bar(
    df_grouped,
    x="Rating",
    y="Votes",
    # text="Votes",
    color_discrete_sequence=["#f63366"] * len(df_grouped),
    template="plotly_white"
)
st.plotly_chart(bar_chart)
pie_chart = px.pie(df_participants, title="Total number of Participants",
                   values="Participants", names="Departments")
st.plotly_chart(pie_chart)
