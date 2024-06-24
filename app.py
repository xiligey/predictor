from sklearn.preprocessing import StandardScaler
import streamlit as st
import pandas as pd
import polars as pl
import pickle

DATASET_PATH = "data/data.csv"
RF_MODEL_PATH = "model/rf_model.pkl"


def main():
    @st.cache_data
    def load_dataset() -> pd.DataFrame:
        return pl.read_csv(DATASET_PATH).to_pandas()

    def user_input_features() -> pd.DataFrame:
        race = st.sidebar.selectbox("Race", options=(race for race in heart.Race.unique()))
        sex = st.sidebar.selectbox("Sex", options=(sex for sex in heart.Sex.unique()))
        age_cat = st.sidebar.selectbox("Age category",
                                       options=(age_cat for age_cat in heart.AgeCategory.unique()))
        bmi = st.sidebar.number_input("BMI", 0, 50, 21)
        sleep_time = st.sidebar.number_input("How many hours on average do you sleep?", 0, 24, 7)
        gen_health = st.sidebar.selectbox("How can you define your general health?",
                                          options=(gen_health for gen_health in heart.GenHealth.unique()))
        phys_health = st.sidebar.number_input("For how many days during the past 30 days was"
                                              " your physical health not good?", 0, 30, 0)
        ment_health = st.sidebar.number_input("For how many days during the past 30 days was"
                                              " your mental health not good?", 0, 30, 0)
        phys_act = st.sidebar.selectbox("Have you played any sports (running, biking, etc.)"
                                        " in the past month?", options=("No", "Yes"))
        smoking = st.sidebar.selectbox("Have you smoked at least 100 cigarettes in"
                                       " your entire life (approx. 5 packs)?)",
                                       options=("No", "Yes"))
        alcohol_drink = st.sidebar.selectbox("Do you have more than 14 drinks of alcohol (men)"
                                             " or more than 7 (women) in a week?", options=("No", "Yes"))
        stroke = st.sidebar.selectbox("Did you have a stroke?", options=("No", "Yes"))
        diff_walk = st.sidebar.selectbox("Do you have serious difficulty walking"
                                         " or climbing stairs?", options=("No", "Yes"))
        diabetic = st.sidebar.selectbox("Have you ever had diabetes?",
                                        options=(diabetic for diabetic in heart.Diabetic.unique()))
        asthma = st.sidebar.selectbox("Do you have asthma?", options=("No", "Yes"))
        kid_dis = st.sidebar.selectbox("Do you have kidney disease?", options=("No", "Yes"))
        skin_canc = st.sidebar.selectbox("Do you have skin cancer?", options=("No", "Yes"))

        features = pd.DataFrame({
            "PhysicalHealth": [phys_health],
            "MentalHealth": [ment_health],
            "SleepTime": [sleep_time],
            "BMI": [bmi],
            "Smoking": [smoking],
            "AlcoholDrinking": [alcohol_drink],
            "Stroke": [stroke],
            "DiffWalking": [diff_walk],
            "Sex": [sex],
            "AgeCategory": [age_cat],
            "Race": [race],
            "Diabetic": [diabetic],
            "PhysicalActivity": [phys_act],
            "GenHealth": [gen_health],
            "Asthma": [asthma],
            "KidneyDisease": [kid_dis],
            "SkinCancer": [skin_canc]
        })
        features.to_excel('1.xlsx')
        return features

    st.set_page_config(
        page_title="Heart Disease Prediction App",
        page_icon="images/heart-fav.png"
    )

    st.title("Heart Disease Prediction")
    st.subheader("Are you wondering about the condition of your heart? "
                 "This app will help you to diagnose it!")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("images/doctor.png",
                 caption="I'll help you diagnose your heart health! - Dr. Random Forest Classifier",
                 width=150)
        submit = st.button("Predict")
    with col2:
        st.markdown("""
        Did you know that machine learning models can help you
        predict heart disease pretty accurately? In this app, you can
        estimate your chance of heart disease (yes/no) in seconds!
        
        Here, a random forest classifier model using an undersampling technique
        was constructed using survey data of over 300k US residents from the year 2020.
        This application is based on it because it has proven to be better than the random forest
        (it achieves an accuracy of about 87.86%, which is quite good).
        
        To predict your heart disease status, simply follow the steps bellow:
        1. Enter the parameters that best describe you;
        2. Press the "Predict" button and wait for the result. 
        """)

    heart = load_dataset()

    st.sidebar.title("Feature Selection")
    st.sidebar.image("images/heart-sidebar.png", width=100)

    input_df = user_input_features()

    df = pd.concat([input_df, heart], axis=0)
    df = df.drop(columns=["HeartDisease"])
    df = pd.get_dummies(df, drop_first=True)
    scaler = StandardScaler()
    df = scaler.fit_transform(df)
    df = df[:1]

    rf_model = pickle.load(open(RF_MODEL_PATH, "rb"))

    if submit:
        prediction = rf_model.predict(df)
        prediction_prob = rf_model.predict_proba(df)
        if prediction == 0:
            st.markdown(f"**The probability that you'll have"
                        f" heart disease is {round(prediction_prob[0][1] * 100, 2)}%."
                        f" You are healthy!**")
            st.image("images/heart-okay.jpg",
                     caption="Your heart seems to be okay! - Dr. RandomForest Classifier")
        else:
            st.markdown(f"**The probability that you will have"
                        f" heart disease is {round(prediction_prob[0][1] * 100, 2)}%."
                        f" It sounds like you are not healthy.**")
            st.image("images/heart-bad.jpg",
                     caption="I'm not satisfied with the condition of your heart! - Dr. RandomForest Classifier")


if __name__ == "__main__":
    main()
