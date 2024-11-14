import streamlit as st
import pandas as pd
import plotly.express as px
from model import load_data, predict, add_user_input
from powerbi_output import render_powerbi_page_1, render_powerbi_page_2

# Load dataset and encoders
df, agent_encoder, topic_encoder = load_data("data/Call_Center_Dataset.csv")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Home",
        "Predictive Analysis",
        "Add New Session",
        "Power BI Output - Page 1",
        "Power BI Output - Page 2",
    ],
)

if page == "Home":
    st.title("Call Center Operations Analysis")
    st.subheader("Project Introduction")
    st.write(
        """
        This BI project aims to analyze ESPN Cable Company’s call center operations, identifying key factors influencing customer satisfaction, such as agent performance, call topics, speed of response, and average talk duration. The goal is to enhance customer service and operational efficiency, helping ESPN Cable Company improve service quality, reduce customer churn, and strengthen brand loyalty.
        """
    )

elif page == "Predictive Analysis":
    st.title("Predictive Analysis")
    st.subheader("Predict customer satisfaction based on call center session details.")

    # Select agent and topic using actual values
    selected_agent = st.selectbox("Select Agent", agent_encoder.classes_)
    selected_topic = st.selectbox("Select Topic", topic_encoder.classes_)
    speed_of_answer = st.number_input("Speed of Answer (in seconds)", min_value=0)
    avg_talk_duration = st.number_input("Average Talk Duration (in seconds)", min_value=0)

    if st.button("Predict"):
        # Create a DataFrame for input data
        input_data = pd.DataFrame(
            {
                "Agent": [selected_agent],
                "Topic": [selected_topic],
                "Speed of answer in seconds": [speed_of_answer],
                "AvgTalkDuration": [avg_talk_duration],
            }
        )

        # Encode the categorical features
        try:
            input_data["Agent"] = agent_encoder.transform(input_data["Agent"])
            input_data["Topic"] = topic_encoder.transform(input_data["Topic"])
        except ValueError as e:
            st.error(f"Encoding error: {str(e)}")
            st.stop()  # Stops execution of the app

        # Make the prediction
        try:
            prediction = predict(input_data)
            st.write(f"Predicted Satisfaction Rating: {prediction[0]}")

            # Visualizations
            st.subheader("Historical Satisfaction Ratings")

            # Box Plot
            historical_data = df[["Agent", "Topic", "Satisfaction rating"]]
            fig = px.box(
                historical_data,
                x="Agent",
                y="Satisfaction rating",
                color="Topic",
                title="Box Plot of Satisfaction Ratings by Agent and Topic"
            )
            st.plotly_chart(fig)

            # Count of Satisfaction Ratings
            satisfaction_counts = df["Satisfaction rating"].value_counts().reset_index()
            satisfaction_counts.columns = ["Satisfaction Rating", "Count"]
            fig2 = px.bar(
                satisfaction_counts,
                x="Satisfaction Rating",
                y="Count",
                title="Count of Satisfaction Ratings"
            )
            st.plotly_chart(fig2)

            # Average Satisfaction by Agent
            avg_satisfaction_by_agent = df.groupby("Agent")["Satisfaction rating"].mean().reset_index()
            fig3 = px.bar(
                avg_satisfaction_by_agent,
                x="Agent",
                y="Satisfaction rating",
                title="Average Satisfaction Rating by Agent",
                labels={"Satisfaction rating": "Average Satisfaction"}
            )
            st.plotly_chart(fig3)

            # Average Satisfaction by Topic
            avg_satisfaction_by_topic = df.groupby("Topic")["Satisfaction rating"].mean().reset_index()
            fig4 = px.bar(
                avg_satisfaction_by_topic,
                x="Topic",
                y="Satisfaction rating",
                title="Average Satisfaction Rating by Topic",
                labels={"Satisfaction rating": "Average Satisfaction"}
            )
            st.plotly_chart(fig4)

            # Response Time Distribution
            fig5 = px.histogram(
                df,
                x="Speed of answer in seconds",
                nbins=30,
                title="Distribution of Speed of Answer",
                labels={"Speed of answer in seconds": "Speed of Answer (seconds)"}
            )
            st.plotly_chart(fig5)

        except ValueError as e:
            st.error(f"Error in prediction: {str(e)}")

elif page == "Add New Session":
    st.title("Add New Session")
    st.subheader("Add new session data for further analysis and model training.")

    # Use actual agent names and topics instead of encoded values
    agent = st.selectbox("Select Agent", agent_encoder.classes_)
    topic = st.selectbox("Select Topic", topic_encoder.classes_)
    speed_of_answer = st.number_input("Speed of Answer (in seconds)", min_value=0)
    avg_talk_duration = st.number_input("Average Talk Duration (in seconds)", min_value=0)
    satisfaction_rating = st.slider("Satisfaction Rating", min_value=1, max_value=5, step=1)

    if st.button("Add Session"):
        add_user_input(
            df,
            agent,
            topic,
            speed_of_answer,
            avg_talk_duration,
            satisfaction_rating,
            agent_encoder,
            topic_encoder,
        )
        st.success("Session added successfully!")

elif page == "Power BI Output - Page 1":
    st.title("Power BI Output - Page 1")
    render_powerbi_page_1()

elif page == "Power BI Output - Page 2":
    st.title("Power BI Output - Page 2")
    render_powerbi_page_2()
