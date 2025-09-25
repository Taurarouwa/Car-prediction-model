import streamlit as st
import pickle
import pandas as pd

with open('random_forest_model.pkl', 'rb') as mod:
    model = pickle.load(mod)

# Load encoded data to get the columnss
encoded_df = pd.read_csv('encoded_data.csv', index_col=0)

st.image('car2.jpg', use_container_width=True)
st.title('Car Price Predictor')
st.write('A model to predict car prices')

def input_var():
    # Numerical inputs
    manufacturing_year = st.number_input('Manufacturing Year', min_value=1950, max_value=2025, value=2015)
    mileage_km = st.number_input('Mileage (km)', value=1000.0)
    engine_size = st.number_input('Engine Size', value=2000.0)
    car_age = 2025 - manufacturing_year

    # Categorical inputs
    region = st.selectbox('Region', encoded_df.filter(like='region_').columns.str.replace('region_', '').unique())
    manufacturer = st.selectbox('Manufacturer', encoded_df.filter(like='manufacturer_').columns.str.replace('manufacturer_', '').unique())
    car_model = st.selectbox('Model', encoded_df.filter(like='car_model_').columns.str.replace('car_model_', '').unique())
    color = st.selectbox('Color', encoded_df.filter(like='color_').columns.str.replace('color_', '').unique())
    car_condition = st.selectbox('Car Condition', encoded_df.filter(like='car_condition_').columns.str.replace('car_condition_', '').unique())
    selling_cond = st.selectbox('Selling Condition', encoded_df.filter(like='selling_cond_').columns.str.replace('selling_cond_', '').unique())
    bought_cond = st.selectbox('Bought Condition', encoded_df.filter(like='bought_cond_').columns.str.replace('bought_cond_', '').unique())
    fuel_type = st.selectbox('Fuel Type', encoded_df.filter(like='fuel_type_').columns.str.replace('fuel_type_', '').unique())
    transmission = st.selectbox('Transmission', encoded_df.filter(like='transmission_').columns.str.replace('transmission_', '').unique())
    car_city = st.selectbox('City', encoded_df.filter(like='car_city_').columns.str.replace('car_city_', '').unique())


    # Create a dictionary with all possible features used
    data = dict.fromkeys(encoded_df.drop('car_price', axis=1).columns, 0)

    # Adding the user inputs to the dict
    data['manufacturing_year'] = manufacturing_year
    data['mileage_km'] = mileage_km
    data['engine_size'] = engine_size
    data['car_age'] = car_age

    # Set the appropriate one-hot encoded columns to 1
    data[f'region_{region}'] = 1
    data[f'manufacturer_{manufacturer}'] = 1
    data[f'car_model_{car_model}'] = 1
    data[f'color_{color}'] = 1
    data[f'car_condition_{car_condition}'] = 1
    data[f'selling_cond_{selling_cond}'] = 1
    data[f'bought_cond_{bought_cond}'] = 1
    data[f'fuel_type_{fuel_type}'] = 1
    data[f'transmission_{transmission}'] = 1
    data[f'car_city_{car_city}'] = 1

    data_input = pd.DataFrame([data])

    return data_input

user_input = input_var()

if st.button('Predict Price'):
    prediction = model.predict(user_input)
    st.subheader('The Predicted Price is:')
    st.success(f'₦{round(prediction[0], 2)}')