import streamlit as st
import pickle
import numpy as np

# Load all components
vectorizer = pickle.load(open("countVectorizer.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
model = pickle.load(open("model_dt.pkl", "rb"))

# Streamlit config
st.set_page_config(page_title="Sentiment Analysis", page_icon="💬", layout="centered")
st.title("💬 Amazon Review Sentiment Analysis")
st.markdown("Enter a review below and we'll predict whether the sentiment is **positive** or **negative**.")

# Input text box
review = st.text_area("📝 Enter your review here", height=200)

# Predict button
if st.button("🔍 Analyze Sentiment"):
    if review.strip() == "":
        st.warning("Please enter a review.")
    else:
        # Vectorize and scale
        review_vector = vectorizer.transform([review])
        review_scaled = scaler.transform(review_vector.toarray())

        # Predict
        prediction = model.predict(review_scaled)

        # Output
        if prediction[0] == 1:
            st.success("✅ Positive Sentiment")
        else:
            st.error("❌ Negative Sentiment")
