import streamlit as st
import pickle
import numpy as np

# Load trained model
with open('svcmodel.pkl', 'rb') as file:
    scv_model = pickle.load(file)

# --- Styling ---
st.set_page_config(page_title="Malnutrition Risk Assessment", page_icon="🍽️", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #2C3E50;'>🍽️ Malnutrition Risk Assessment</h1>",
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

st.write("Please provide the information below to assess malnutrition risk based on health and environmental factors.")

# --- Categorical Inputs ---
with st.expander("🏠 Household & Environment Information"):
    parental_education = st.selectbox("Parental Education", ["No Education", "Primary", "Secondary", "Tertiary"])
    access_healthcare = st.radio("Access to Healthcare", ["No", "Yes"], horizontal=True)
    clean_water = st.radio("Access to Clean Water", ["No", "Yes"], horizontal=True)
    sanitation = st.radio("Sanitation Facilities", ["No", "Yes"], horizontal=True)
    food_availability = st.radio("Availability of Food", ["No", "Yes"], horizontal=True)
    seasonal_variation = st.radio("Seasonal Variations", ["No", "Yes"], horizontal=True)
    market_access = st.radio("Market Access", ["No", "Yes"], horizontal=True)

# --- Numeric Inputs ---
with st.expander("🧒 Child Nutrition Metrics"):
    weight_for_age = st.number_input("Weight-for-Age", min_value=-5.0, max_value=5.0, step=0.1)
    height_for_age = st.number_input("Height-for-Age", min_value=-5.0, max_value=5.0, step=0.1)
    weight_for_height = st.number_input("Weight-for-Height", min_value=-5.0, max_value=5.0, step=0.1)
    dietary_diversity = st.slider("Dietary Diversity (0–10)", 0, 10, 5)
    meal_frequency = st.slider("Frequency of Meals per Day", 1, 5, 3)

# --- Encoding ---
edu_map = {"No Education": 0, "Primary": 1, "Secondary": 2, "Tertiary": 3}
bin_map = {"No": 0, "Yes": 1}

features = np.array([[
    edu_map[parental_education],
    bin_map[access_healthcare],
    bin_map[clean_water],
    bin_map[sanitation],
    bin_map[food_availability],
    bin_map[seasonal_variation],
    bin_map[market_access],
    weight_for_age,
    height_for_age,
    weight_for_height,
    dietary_diversity,
    meal_frequency
]])

# --- Prediction ---
if st.button("🔍 Predict Risk"):
    prediction = scv_model.predict(features)[0]
    risk_labels = {0: "High", 1: "Low", 2: "Moderate"}
    colors = {"High": "red", "Moderate": "orange", "Low": "green"}
    risk = risk_labels[prediction]

    st.markdown(
        f"<h3 style='text-align: center; color:{colors[risk]};'>⚠️ Predicted Malnutrition Risk: {risk}</h3>",
        unsafe_allow_html=True
    )

