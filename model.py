import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib


# Load data function
def load_data(filepath):
    df = pd.read_csv(filepath)
    df["AvgTalkDuration"] = pd.to_timedelta(df["AvgTalkDuration"]).dt.total_seconds()
    df["Satisfaction rating"] = df["Satisfaction rating"].fillna(0).astype(int)

    # Encode categorical variables
    agent_encoder = LabelEncoder()
    topic_encoder = LabelEncoder()

    df["Agent"] = agent_encoder.fit_transform(df["Agent"])
    df["Topic"] = topic_encoder.fit_transform(df["Topic"])
    df["Resolved"] = df["Resolved"].map({"Y": 1, "N": 0})

    return df, agent_encoder, topic_encoder


# Predict satisfaction rating
def predict(data):
    model = joblib.load("model.joblib")
    return model.predict(data)


# Add user input to the DataFrame
def add_user_input(
    df,
    agent,
    topic,
    speed_of_answer,
    avg_talk_duration,
    satisfaction_rating,
    agent_encoder,
    topic_encoder,
):
    new_data = pd.DataFrame(
        {
            "Agent": [agent],
            "Topic": [topic],
            "Speed of answer in seconds": [speed_of_answer],
            "AvgTalkDuration": [avg_talk_duration],
            "Satisfaction rating": [satisfaction_rating],
        }
    )
    new_data["Agent"] = agent_encoder.transform(new_data["Agent"])
    new_data["Topic"] = topic_encoder.transform(new_data["Topic"])

    # Append and save to CSV
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("data/Call_Center_Dataset.csv", index=False)
