
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Mobile Phone Usage Analysis",
    page_icon="📱",
    layout="wide"
)

# Load dataset
df = pd.read_csv("mobile_user_behavior_100_rows.csv")

# Main title
st.title("📱 Mobile Phone Usage Analysis")
st.write("An interactive dashboard to analyse mobile phone usage and user behaviour.")

# Sidebar filters
st.sidebar.header("Filter Options")

# Operating System filter
os_options = ["All"] + sorted(df["Operating System"].dropna().unique().tolist())
selected_os = st.sidebar.selectbox("Select Operating System", os_options)

# Device Model filter
device_options = ["All"] + sorted(df["Device Model"].dropna().unique().tolist())
selected_device = st.sidebar.selectbox("Select Device Model", device_options)

# Age filter
min_age = int(df["Age"].min())
max_age = int(df["Age"].max())

selected_age = st.sidebar.slider(
    "Select Age Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# User Behaviour Class filter
class_options = sorted(df["User Behavior Class"].dropna().unique().tolist())
selected_class = st.sidebar.multiselect(
    "Select User Behavior Class",
    class_options,
    default=class_options
)

# Apply filters
filtered_df = df.copy()

if selected_os != "All":
    filtered_df = filtered_df[filtered_df["Operating System"] == selected_os]

if selected_device != "All":
    filtered_df = filtered_df[filtered_df["Device Model"] == selected_device]

filtered_df = filtered_df[
    (filtered_df["Age"] >= selected_age[0]) &
    (filtered_df["Age"] <= selected_age[1])
]

filtered_df = filtered_df[
    filtered_df["User Behavior Class"].isin(selected_class)
]

# Dashboard tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Data Analysis",
    "Visualizations",
    "Insights"
])

# Overview tab
with tab1:
    st.header("Dashboard Overview")

    if len(filtered_df) > 0:

        # KPI metrics
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Users", len(filtered_df))

        col2.metric(
            "Average App Usage",
            round(filtered_df["App Usage Time (min/day)"].mean(), 2)
        )

        col3.metric(
            "Average Screen Time",
            round(filtered_df["Screen On Time (hours/day)"].mean(), 2)
        )

        col4.metric(
            "Average Data Usage",
            round(filtered_df["Data Usage (MB/day)"].mean(), 2)
        )

        st.subheader("Dataset Preview")
        st.dataframe(filtered_df.head(10), use_container_width=True)

    else:
        st.warning("No records found. Please change the filters.")

# Data Analysis tab
with tab2:
    st.header("Data Analysis")

    if len(filtered_df) > 0:

        st.subheader("Basic Statistics")
        st.write(filtered_df.describe())

        st.subheader("Operating System Count")
        os_count = filtered_df["Operating System"].value_counts()
        st.dataframe(os_count)

        st.subheader("Device Model Count")
        device_count = filtered_df["Device Model"].value_counts()
        st.dataframe(device_count)

        st.subheader("User Behavior Class Count")
        class_count = filtered_df["User Behavior Class"].value_counts().sort_index()
        st.dataframe(class_count)

    else:
        st.warning("No data available for analysis.")

# Visualizations tab
with tab3:
    st.header("Data Visualizations")

    if len(filtered_df) > 0:

        # Bar Chart
        st.subheader("Average App Usage by Device Model")

        bar_data = filtered_df.groupby("Device Model")[
            "App Usage Time (min/day)"
        ].mean()

        fig1, ax1 = plt.subplots()
        bar_data.plot(kind="bar", ax=ax1)
        ax1.set_xlabel("Device Model")
        ax1.set_ylabel("Average App Usage (minutes/day)")
        ax1.set_title("App Usage by Device Model")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig1)
        plt.close(fig1)

        # Line Chart
        st.subheader("Average App Usage by Age")

        line_data = filtered_df.groupby("Age")[
            "App Usage Time (min/day)"
        ].mean().sort_index()

        fig2, ax2 = plt.subplots()
        line_data.plot(kind="line", marker="o", ax=ax2)
        ax2.set_xlabel("Age")
        ax2.set_ylabel("Average App Usage (minutes/day)")
        ax2.set_title("App Usage by Age")
        st.pyplot(fig2)
        plt.close(fig2)

        # Scatter Plot
        st.subheader("Screen Time vs App Usage")

        fig3, ax3 = plt.subplots()
        ax3.scatter(
            filtered_df["Screen On Time (hours/day)"],
            filtered_df["App Usage Time (min/day)"]
        )
        ax3.set_xlabel("Screen On Time (hours/day)")
        ax3.set_ylabel("App Usage Time (minutes/day)")
        ax3.set_title("Screen Time vs App Usage")
        st.pyplot(fig3)
        plt.close(fig3)

    else:
        st.warning("No data available to display charts.")

# Insights tab
with tab4:
    st.header("User Behaviour Insights")

    if len(filtered_df) > 0:

        avg_usage = filtered_df["App Usage Time (min/day)"].mean()
        avg_screen = filtered_df["Screen On Time (hours/day)"].mean()
        avg_battery = filtered_df["Battery Drain (mAh/day)"].mean()

        st.write("**Average App Usage:**", round(avg_usage, 2), "minutes per day")
        st.write("**Average Screen Time:**", round(avg_screen, 2), "hours per day")
        st.write("**Average Battery Drain:**", round(avg_battery, 2), "mAh per day")

        st.subheader("Highest App Usage Record")
        highest_usage = filtered_df.loc[
            filtered_df["App Usage Time (min/day)"].idxmax()
        ]
        st.write(highest_usage)

        st.subheader("Highest Battery Drain Record")
        highest_battery = filtered_df.loc[
            filtered_df["Battery Drain (mAh/day)"].idxmax()
        ]
        st.write(highest_battery)

    else:
        st.warning("No data available to display insights.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Mobile Phone Usage Analysis")
st.sidebar.caption("Streamlit Dashboard")
