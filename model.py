import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scraper import Scraper

def generate_model(car_type = "sedan", num_pages = -1):
	"""
	Scraper(car_type, num_pages)
	- car_type is one of the strings: "sedan", "suv", "coupe" or "convertible"

	- num_pages is the number of pages to get the data from, by default it parses throught the data
	of all the pages but the user can specifiy a smaller number of pages as the Scraper will take
	the minimum of the the total number of pages on the website and num_pages
	"""
	my_scraper = Scraper(car_type, num_pages)
	data_dict = my_scraper.get_data_dict()

	df = pd.DataFrame(data_dict)
	columns = ['Name', 'Seats', 'Length', 'Height', 'Horsepower', 'Torque', 'Wheelbase', 
				'Trunk_volume', 'Curb_Weight', 'Price']
	df.columns = columns

	imputer = SimpleImputer(missing_values=np.NaN, strategy='mean')
	df_imputed = pd.DataFrame(imputer.fit_transform(df.iloc[0:, 1:]))
	df_imputed.columns = ['Seats', 'Length', 'Height', 'Horsepower', 'Torque', 'Wheelbase', 
				'Trunk_volume', 'Curb_Weight', 'Price']
	df_imputed

	x = df_imputed[['Seats', 'Length', 'Height', 'Horsepower','Torque', 'Wheelbase', 'Trunk_volume', 'Curb_Weight']]

	y = df_imputed[['Price']]

	x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.85, test_size = 0.15)
	model = LinearRegression()
	model.fit(x_train, y_train)
	y_predict= model.predict(x_test)
	print("Train score:")
	print(model.score(x_train, y_train))

	print("Test score:")
	print(model.score(x_test, y_test))
	return model
