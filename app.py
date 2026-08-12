import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pickle


##loading the model

model = tf.keras.models.load_model('model.h5')

##loading the encoders and scaler

with open ('encoder.pkl','rb') as file:
    encoder = pickle.load(file)

with open ('ohe.pkl','rb') as file:
    ohe = pickle.load(file)

with open ('scaler.pkl','rb') as file:
    scaler = pickle.load(file)


##streamlit app
st.title('Customer Churn Prediction')
geography = st.selectbox('Geography', ohe.categories_[0])
gender = st.selectbox('Gender', encoder.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])


# Prepare the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
     'Geography': [geography],
    'Gender': [encoder.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

##geography column
geo_encoded = ohe.transform(input_data[['Geography']])
geo_encoded_df = pd.DataFrame(
    geo_encoded,
    columns=ohe.get_feature_names_out(['Geography'])
)


input_df = pd.concat([input_data.drop('Geography', axis=1), geo_encoded_df],axis=1)


input_scaled = scaler.transform(input_df)


prediction = model.predict(input_scaled)

prediction_pro = prediction[0][0]

st.write(f'Churn Probability: {prediction_pro:.2f}')

if prediction_pro > 0.5:
    st.error('The customer is likely to churn')
else:
    st.success('The customer is not likely to churn')