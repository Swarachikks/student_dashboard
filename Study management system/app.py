import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("📊 Student Performance Analytics Dashboard")

uploaded_file = st.file_uploader("Upload Student CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Raw Data")
    st.dataframe(df)

    # ----------------------------
    # Feature Engineering
    # ----------------------------

    df["Total"] = df[["Math", "Science", "English"]].sum(axis=1)
    df["Average"] = df["Total"] / 3

    df["Result"] = np.where(df["Average"] >= 40, "Pass", "Fail")

    def assign_grade(avg):
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        else:
            return "D"

    df["Grade"] = df["Average"].apply(assign_grade)
    df["Rank"] = df["Total"].rank(ascending=False, method="min")

    # ----------------------------
    # KPIs
    # ----------------------------

    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Class Average", round(df["Average"].mean(),2))
    col2.metric("Top Score", df["Total"].max())
    col3.metric("Pass %",
                round((df["Result"].value_counts(normalize=True)["Pass"]*100),2))

    # ----------------------------
    # Top 3 Students
    # ----------------------------

    st.subheader("🏆 Top 3 Students")
    st.dataframe(df.sort_values("Rank").head(3))

    # ----------------------------
    # Visualizations
    # ----------------------------

    st.subheader("📈 Visualizations")

    col1, col2 = st.columns(2)

    fig1, ax1 = plt.subplots()
    ax1.bar(df["Student"], df["Total"])
    plt.xticks(rotation=45)
    ax1.set_title("Total Marks by Student")
    col1.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    df["Grade"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_title("Grade Distribution")
    col2.pyplot(fig2)

    # ----------------------------
    # Download Button
    # ----------------------------

    st.subheader("⬇ Download Analyzed Report")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Report as CSV",
        data=csv,
        file_name="analyzed_student_report.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file to begin.")