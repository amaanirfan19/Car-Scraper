import requests
import numpy as np
import re
from bs4 import BeautifulSoup as bs
import math

class Scraper:
	
	def __init__(self, car_type = "sedan", num_pages = -1):
		self.links = []
		self.data_dict = []
		self.car_type = car_type
		
		if num_pages == -1:
			self.NUM_OF_PAGES = 3
		else:
			self.NUM_OF_PAGES = num_pages	
		
	def get_data_dict(self):
		self.find_links()
		self.populate_data_dict()
		return self.data_dict

	def find_links(self):
		for page_number in range(self.NUM_OF_PAGES):
			#URL is modified to show a particular page of the listings and to show the maximum number of listing in the page which is 40
			URL = f"https://www.cars.com/research/sedan/?page={page_number}"
			page = requests.get(URL)
			soup = bs(page.content, 'html.parser')

			matches = soup.find("div", class_="filter-section").span.text
			num_matches = int(matches.replace(" ", "").split("m", 1)[0])

			self.links += soup.findAll("a", class_="research-vehicle-card-visited-tracking-link")

	def populate_data_dict(self):
		NaN = np.nan
		for link in self.links:
			car_url = 'https://www.cars.com' + str(link['href'])
			car_page = requests.get(car_url)
			car_soup = bs(car_page.content, 'html.parser')

			#NAME
			name = car_soup.find("h1", class_="sds-heading--1 sds-page-section__title").text
			spec_link = car_soup.find("p", class_="mmy-specs-link").a
			specs_url = 'https://www.cars.com' + str(spec_link['href'])
			specs_page = requests.get(specs_url)
			specs_soup = bs(specs_page.content, 'html.parser')
			key_specs = specs_soup.findAll("div", class_="key-spec")

			#SEATS
			try:
				seats = int(key_specs[1].label.text[0])
			except:
				seats = NaN
			measurements = str(key_specs[4].label.text)

			measurements = [float(s) for s in re.findall(r'-?\d+\.?\d*', measurements)]

			#LENGTH, HEIGHT
			try:
				length = measurements[0]
				height = measurements[1]
			except:
				length = NaN
				height = NaN

			#PRICE
			price = specs_soup.find("div", class_="price-amount").text
			try:
				price = float(price.replace('$', '').replace(',',''))
			except:
				price = NaN

			#HORSEPOWER
			engine = specs_soup.find("div", id="specifications-panel4").findAll("td")
			engine = [info.text for info in engine]
			it = iter(engine)
			engine_dct = dict(zip(it, it))
			try:
				horsepower = float(engine_dct['SAE Net Horsepower @ RPM']
							.replace(" ", "").split("@", 1)[0])
			except:
				horsepower = NaN


			#TORQUE
			try:
				torque = float(engine_dct['SAE Net Torque @ RPM']
							.replace(" ", "").split("@", 1)[0])
			except:
				torque = NaN

			#WHEELBASE
			dimensions = specs_soup.find("div", id="specifications-panel14").findAll("td")
			dimensions = [info.text for info in dimensions]
			it = iter(dimensions)
			dimensions_dict = dict(zip(it, it))
			try:
				wheelbase = float(dimensions_dict['Wheelbase']
								.replace(" ", "").split("i", 1)[0])
			except:
				wheelbase = NaN

			#TRUNK VOLUME
			try:
				trunk_volume = float(dimensions_dict['Trunk Volume']
							.replace(" ", "").split("f", 1)[0])
			except:
				trunk_volume = NaN


			#CURB WEIGHT
			weight = specs_soup.find("div", id="specifications-panel13").findAll("td")
			weight = [info.text for info in weight]
			it = iter(weight)
			weight_dct = dict(zip(it, it))

			try:
				curb_weight = float(weight_dct['Base Curb Weight']
									.replace(" ", "").split("l", 1)[0])
			except:
				curb_weight = NaN
			
			self.data_dict.append([name, seats, length, height, horsepower, torque, wheelbase, trunk_volume, curb_weight, price])

