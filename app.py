import streamlit as st
import pandas as pd
import numpy as np
from model import generate_model


# body dict
body_dic = {'sedan': 0, 'suv': 1, 'coupe': 2, 'convertible': 3}


# list of categorical label
body_list = ["sedan", "suv", "coupe", "convertible"]


# setting custome tab
st.set_page_config(page_title='Car Scraper made by web scraping cars.com', page_icon='🚗')


# # writing header
# st.title('# Used Car Price Predition™  🚗')
st.markdown("<h2 style='text-align: center;'>🚗  Car Price Predictor  🚗</h2>", unsafe_allow_html=True)


col1, col2 = st.columns(2)
columns = ['Seats', 'Length', 'Height', 'Horsepower', 'Torque', 'Wheelbase', 
              'Trunk_volume', 'Curb_Weight', 'Price']
# start taking inpouts
# 1. taking milage info integer
body_type = col2.selectbox(label='Enter the body type of the car', options=body_list, help='select the body type of the car')
body_type = body_dic[body_type]
num_pages =  col1.slider('Number of pages to get data from website', 3,10,1)
seats =  col1.slider('Number of seats in the car', 1,10,4)
length =  col1.slider('Length of car (inches)', 1,300,150)
height =  col1.slider('Height the car (inches)', 1,300,50)
horsepower =  col1.slider('Horsepower the car', 1,1000,200)
torque =  col1.slider('Torque the car', 1,1000,200)
wheelbase =  col1.slider('Wheelbase the car', 1,300,100)
trunk_volume =  col1.slider('Trunk Volume the car', 1,50,10)
curb_weight =  col1.slider('Weight of car', 1000,7000,3500)


# creatng a input array for prediction
inp_array = np.array([[float(seats), float(length), float(height), float(horsepower), float(torque), float(wheelbase), float(trunk_volume), float(curb_weight)]])

# loding the model
@st.cache()
def model_loader():
    model = generate_model(body_type, num_pages)
    return model


# loading both models

with st.spinner('🚕🛺🚙🚜🚚🚓🚗🚕 Hold on, the app is loading !! 🚕🛺🚙🚜🚚🚓🚗🚕'):
    model = model_loader()

predict = col1.button('Predict') # creating a predict buutton

if predict:
	print(inp_array)
	pred = model.predict(inp_array)
	if pred < 0: # handeling negative outputs.
		st.error('Sorry for this error, the model has very little data as of right now as it is creating its own dataset by web scraping')
	pred = round(float(pred),3)
	write = 'The predicted price of the car is $ '+ str(pred) + ' 🚙' # showing the price prediction.
	st.success(write)
	st.balloons()


# writing some information about the projects.

st.header('🧭 Little Info About the Project')
prj_info = """
            You can predict used car 🚙 price by giving some information about the car such as the number of seats, weight, horsepower and other cool features.\n
            
            Want to look at the code and data visualizations? - [Github](https://github.com/amaanirfan19) \n
            In case want to contact with me -  madhada@uwaterloo.ca 📫
"""
st.write(prj_info)
st.header("""Untll then ❤""")