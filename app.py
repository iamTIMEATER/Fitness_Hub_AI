import os
import streamlit as st
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

credentials = Credentials(
    url=os.getenv("IBM_URL"),
    api_key=os.getenv("IBM_API_KEY")
)

model = ModelInference(
    model_id="ibm/granite-8b-code-instruct",
    credentials=credentials,
    project_id=os.getenv("IBM_PROJECT_ID")
)

st.title("🏋️ Fitness Hub AI")
st.write("Your personal AI fitness assistant.")

user_prompt = st.text_area(
    "Ask anything about workouts, diet, or fitness:",
    height=180
)

if st.button("Generate Plan"):
    if user_prompt.strip():

        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        full_prompt = f"""
{system_prompt}

User:
{user_prompt}

Assistant:
"""

        try:
            response = model.generate_text(
                prompt=full_prompt,
                params={
                    "max_new_tokens": 1000,
                    "temperature": 0.4
                }
            )

            st.subheader("AI Response")
            st.write(response)

        except Exception as e:
            st.error(f"Error: {e}")