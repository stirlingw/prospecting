import json

with open('cities_states.json','r') as f:
	CITY_STATES = json.load(f)

def AddCities():
	finished = False
	cities = []

	def Cities(cities):
		if len(cities) > 0:
			return cities
		else:
			return '\nNo cities added'

	def FormatCity(city):
		if city != '':
			if city[0] == " ":
				city = city[1::]
			if city[-1] == " ":
				city = city[0:-1]
			city = city.replace(" ","-")
			if city in CITY_STATES['cities']:
				return city
		city = 'Invalid city'
		print(city)
		return city

	while not finished:
		adding_new_listing = True

		while adding_new_listing:
			city = input("\nCity: ").title()
			city = FormatCity(city)
			while city == 'Invalid city':
				city = input("\nPlease type a City or 'done': ").title()
				if city.lower() == 'done':
					return Cities(cities)
				city = FormatCity(city)

			state = input("State Abbreviation: ").upper()
			state = state.replace(" ","")
			if state not in CITY_STATES['states']:
				state = ''
				while state == '':
					print('Invalid state abbreviation')
					state = input("\nPlease type a State Abbreviation or 'done': ").upper()
					state = state.replace(" ","")
				if state.lower() == 'done':
					return Cities(cities)
				if state not in CITY_STATES['states']:
					state = ''

			listing = city+", "+state

			if listing not in cities:
				cities.append(listing)
				adding_new_listing = False

			elif listing in cities:
				print('\nCity and state already added')
				already_added = True
				while already_added:
					response = input("Press 'Enter' to add a new city or type 'done': ").lower()
					if response == 'done':
						return cities
					if response == '':
						already_added = False

		response = input("\nTo add another city press 'Enter' or type 'done': ").lower()
		correct_response = False

		while not correct_response:

			if response == '':
				correct_response = True
				break

			if response == 'done':
				finished = True
				correct_response = True
				return Cities(cities)

			else:
				response = input("Please press 'Enter' or type 'done': ")

if __name__ == "__main__":
	cities = AddCities()

	if type(cities) is str:
		print(cities)

	if type(cities) is list:
		print("\nLoading all cities...")
		print("-------------------------")
		for city in cities:
			print(city)