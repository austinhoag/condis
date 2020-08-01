from condis import cel, db, smtp_connect
from .utils import hit_grid_api
from email.message import EmailMessage
from datetime import datetime


@cel.task
def send_daily_emails():
	""" Loop through the GridLocation() table and for each 
	entry do the lookup and if there are results, send a summary 
	email to the user """
	grid_db_contents = db.GridSearchParams() 
	print()
	print(len(grid_db_contents))
	for grid_param_dict in grid_db_contents:
		print(grid_param_dict)
		all_print_strs = hit_grid_api(**grid_param_dict)
		email = grid_param_dict['email']
		latitude = grid_param_dict['latitude']
		longitude = grid_param_dict['longitude']
		time_min = grid_param_dict['min_time']
		time_max = grid_param_dict['max_time']
		time_min_str = datetime.strptime(time_min,'%H').strftime('%-I %p')
		time_max_str = datetime.strptime(time_max,'%H').strftime('%-I %p')
		time_str = f"{time_min_str} - {time_max_str}"
		temp_min = grid_param_dict['min_temp']
		temp_max = grid_param_dict['max_temp']
		
		humidity_min = grid_param_dict['min_humidity']
		humidity_max = grid_param_dict['max_humidity']
		precip_min = grid_param_dict['min_precip']
		precip_max = grid_param_dict['max_precip']
		if len(all_print_strs) == 0:
			print("No good condis found")
			subject = "Condis: No conditions yet found."
			body = ("Unfortunately we have not found conditions "
					"that meet the criteria you set at coordinates:\n"
					f"\t{latitude},{longitude}. We will keep looking!")
		else:
			print("good condis found")
			subject = "Condis: Good weather conditions found!"
			body = ("We found weather conditions "
					"that meet the criteria you set at coordinates:\n"
					f"\t{latitude},{longitude}.\n\n"
					f"The conditions you requested were:\n"
					f"\tTime of day: {time_str}\n"
					f"\tTemperature: {temp_min}-{temp_max} deg. F\n"
					f"\tRelative Humidity: {humidity_min}-{humidity_max} percent \n"
					f"\tPrecipitation probability: {precip_min}-{precip_max} percent\n\n"
					 "Here are the times that meet those criteria:\n\n")
			for print_str in all_print_strs:
				body+=print_str 
				body+="\n"
		recipients=[email]
		send_email.delay(subject=subject,body=body,recipients=recipients)
	return "Sent daily emails"

@cel.task()
def send_email(subject,body,recipients):
	""" Send an automated email to one or more email addresses.
	---INPUT---
	subject        string
	body		   string
	recipients     list of email address strings
	"""
	
	""" Asynchronous task to send an email """
	msg = EmailMessage()
	msg['Subject'] = subject
	msg['From'] = 'teslaboaters@gmail.com'
	msg['To'] = ','.join(recipients) 
	msg.set_content(body)                    
	smtp_server = smtp_connect()
	smtp_server.send_message(msg)
	return "Email sent!"