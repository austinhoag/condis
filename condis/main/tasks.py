from condis import cel, db, smtp_connect
from .utils import hit_grid_api
from email.message import EmailMessage


@cel.task
def send_daily_emails():
	""" Loop through the GridLocation() table and for each 
	entry do the lookup and if there are results, send a summary 
	email to the user """
	grid_db_contents = db.GridSearchParams() 
	for grid_param_dict in grid_db_contents:
		all_print_strs = hit_grid_api(**grid_param_dict)
		email = grid_param_dict['email']
		latitude = grid_param_dict['latitude']
		longitude = grid_param_dict['longitude']
		temp_min = grid_param_dict['temp_min']
		temp_max = grid_param_dict['temp_max']
		humidity_min = grid_param_dict['humidity_min']
		humidity_max = grid_param_dict['humidity_max']
		precip_min = grid_param_dict['precip_min']
		precip_max = grid_param_dict['precip_max']
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
					f"\tTemperature: {temp_min}-{temp_max}\n"
					f"\tRelative Humidity: {humidity_min}-{humidity_max}\n"
					f"\tPrecipitation probability: {precip_min}-{precip_max}\n\n"
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