import os

import random

import streamlit as st

from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials

from ibm_watsonx_ai.foundation_models import ModelInference



# -----------------------------

# Load Environment Variables

# -----------------------------

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



# -----------------------------

# Page

# -----------------------------

st.set_page_config(

    page_title="Fitness Hub AI",

    page_icon="🏋️",

    layout="centered"

)



st.title("🏋️ Fitness Hub AI")

st.write("Your Personal AI Fitness Coach powered by IBM Granite")



st.markdown("---")



# -----------------------------

# User Inputs

# -----------------------------



age = st.number_input(

    "Age",

    min_value=10,

    max_value=100,

    value=20

)



weight = st.number_input(

    "Weight (kg)",

    min_value=20,

    max_value=200,

    value=60

)



goal = st.selectbox(

    "Fitness Goal",

    [

        "Gain Muscle",

        "Lose Fat",

        "Maintain Fitness"

    ]

)



location = st.selectbox(

    "Workout Location",

    [

        "Home",

        "Gym"

    ]

)



days = st.slider(

    "Workout Days per Week",

    min_value=3,

    max_value=7,

    value=4

)



equipment = st.selectbox(

    "Available Equipment",

    [


        "Adjustable Dumbbells",

        "Resistance Bands",

        "Full Gym"

    ]

)



user_prompt = st.text_area(

    "Additional Requirements",

    height=150,

    placeholder="Example: I want bigger shoulders and stronger legs."

)



# -----------------------------

# Generate Button

# -----------------------------



if st.button("Generate Plan"):



    with open("system_prompt.txt", "r", encoding="utf-8") as f:

        system_prompt = f.read()



    # Makes Granite generate more unique plans

    variation = random.randint(1000, 999999)



    full_prompt = f"""

Workout Variation ID: {variation}



{system_prompt}



User Information



Age: {age}



Weight: {weight} kg



Fitness Goal: {goal}



Workout Location: {location}



Workout Days: {days}



Available Equipment: {equipment}



Additional Requirements:

{user_prompt}



Assistant:

"""



    try:



        response = model.generate_text(

            prompt=full_prompt,

            params={

                "max_new_tokens": 800,

                "temperature": 0.5,

                "top_p": 0.9,

                "repetition_penalty": 1.15

            }

        )



        st.markdown("---")

        st.subheader("🏆 AI Response")

        st.write(response)



    except Exception as e:

        st.error(f"Error: {e}")
        
st.caption("💡 If the response looks incomplete, click Generate Plan again for a better result.")