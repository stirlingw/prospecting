from selenium import webdriver
import json
import csv
import os
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from input_cities import AddCities



def ScrapeCities(cities):

	## Establish email list
	email_list = list()
	print('\n')
	for listings in cities:

		try:

			city = listings.split(',')[0]
			state = listings.split(',')[1].replace(' ', '')
			agent_list = []

			if not os.path.exists('./{}Listings'.format(state)):
				os.makedirs('./{}Listings'.format(state))

			print("Prospecting: {}, {}".format(city, state))

			driver = webdriver.Chrome()
			URL = "http://www.realtor.com/realestateagents/"+city+"_"+state+"/pg-"

			driver.get(URL+str(1))

			## Scrape total number of pages
			total_pages = str()
			total_realtors = driver.find_element_by_css_selector("div.fullpage-wrapper.result-wrapper.hidden-xs.hidden-xxs > div.container > div.search-result  > span").text
			for char in total_realtors:
				try:
					total_pages += str(int(char))
				except:
					pass
			
			total_pages = math.ceil(int(total_pages)/20)
			## Total number of pages complete

			for page in range(2, total_pages+1):

				REGION = city+', '+state
				agent_listings = {}
				agent_listings['Region'] = REGION
				agent_listings['data'] = []
				out_file_path = './'+state+'Listings/'
				out_csv_name = city+'.csv'

				agent_list_nth_child = 22
				for x in range(2,agent_list_nth_child):
					try:
						number = driver.find_element_by_css_selector('div.agent-list-card.clearfix:nth-child('+str(x)+') div.agent-phone.hidden-xs.hidden-xxs').text
						if 'Ext' not in number or 'ext' not in number or 'EXT' not in number:
							agent_list.append(number)
					except: pass

				driver.get(URL+str(page))

			driver.quit()

			for number in agent_list:
				agent_listings['data'].append(number)

			agents = agent_listings['data']
			csv_file = out_file_path+out_csv_name
			email_list.append(csv_file)

			with open(csv_file, 'w+', newline='') as csvfile:

				fieldnames = ['Phone Number']
				csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

				csvwriter.writeheader()

				for number in range(len(agents)):
					csvwriter.writerow({'Phone Number':agents[number]})

			csvfile.close()

		except:
			print('Failed Execution:')
			print('  City: {}'.format(city))
			print('  State: {}'.format(state))
			print('  Total Pages: {}'.format(total_pages))
			print()

	## Send email with every list scraped as attachment
	print('Sending Email...\n')
	BODY = '<h1 style="color:#387a9c;">Prospecting Results</h1>'
	SUBJECT = 'Prospecting Results'

	fromaddr = 'from_email_address@gmail.com'
	toaddr = 'to_email_address@gmail.com'
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = SUBJECT

	part1 = MIMEText(BODY, 'html')
	msg.attach(part1)

	for file in email_list:
		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(file,"r").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition','attachment; filename="{0}"'.format(os.path.basename(file)))
		msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com', 25)
	server.starttls()
	server.login('from_email_address@gmail.com', 'password')
	server.sendmail(fromaddr, toaddr, msg.as_string())

if __name__ == "__main__":

	cities = AddCities()

	if type(cities) is str:
		print(cities)

	if type(cities) is list:
		print("\nLoading all cities...")
		for city in cities:
			print(city)
		ScrapeCities(cities)
	print('Prospecting Complete')
