from flask import (Blueprint, 
	render_template, request, flash,
	url_for,jsonify)
import requests
import pandas
from functools import reduce
from datetime import datetime,timedelta
import pandas as pd

import numpy as np
from .forms import gpsForm, SetupForm
from .utils import expand_dataframe, splitme_zip

main = Blueprint('main',__name__)

time_format = '%-I %p' # e.g. "4 AM"

@main.route("/") 
def base(): 
	return "home"

@main.route("/test_slider",methods=['GET','POST']) 
def test_slider(): 
	form = SetupForm()
	return render_template('main/test_slider.html',form=form)

@main.route("/setup_form",methods=['GET','POST']) 
def setup(): 
	form = SetupForm()
	if request.method == 'POST':
		""" Get form input """
		gps_str = form.gps_str.data
		splitstr = gps_str.split(',')
		latitude = float(splitstr[0])
		longitude = float(splitstr[1])
		""" Make GET request to endpoint to 
		find the grid id and x and y 
		"""
		grid_response = requests.get(url_for('main.find_grid',
				latitude=latitude,longitude=longitude,_external=True))
		grid_dict = grid_response.json()

		grid_id = grid_dict['grid_id']
		grid_x = grid_dict['grid_x']
		grid_y = grid_dict['grid_y']
		temp_str = form.temp.data
		humidity_str = form.humidity.data
		precip_str = form.precip.data
		min_temp = int(temp_str.split('-')[0].strip())
		max_temp = int(temp_str.split('-')[1].strip())
		min_humidity = int(humidity_str.split('-')[0].strip())
		max_humidity = int(humidity_str.split('-')[1].strip())
		min_precip = int(precip_str.split('-')[0].strip())
		max_precip = int(precip_str.split('-')[1].strip())

		# Make GET request to weather API
		print('https://api.weather.gov/gridpoints/{}/{},{}'.format(
			grid_id,grid_x,grid_y))
		response = requests.get('https://api.weather.gov/gridpoints/{}/{},{}'.format(
			grid_id,grid_x,grid_y))
		# Convert response to python dict
		j=response.json()
		# print(j)
		# Get all properties and then extract the ones I will use
		properties=j['properties']
		temp_dicts=properties['temperature']
		hum_dicts=properties['relativeHumidity']
		precip_dicts=properties['probabilityOfPrecipitation']
		
		def calc_msr_duration(x):
			duration_str = str(x).split('P')[-1]
			if "D" in duration_str:
				n_days = int(duration_str[0])
				n_hours = int(duration_str.split("T")[-1].split('H')[0])
				n_hours += n_days*24
			else:
				n_hours = int(str(x).split('PT')[-1].split('H')[0])
			return n_hours
		def init_temp_df():
			temp_lists=temp_dicts['values']
			df_temp=pd.DataFrame(temp_lists)
			df_temp['temp_f']=df_temp['value']*9/5.+32
			df_temp['timestamp']=pd.to_datetime(df_temp['validTime'].map(lambda x: str(x).split('+')[0]))
			# set to local time from UTC (default)
			df_temp['timestamp']-=timedelta(hours=4)
			df_temp['msr_duration']=df_temp['validTime'].map(lambda x: calc_msr_duration(x))
			df_temp.drop(['validTime','value'],axis=1,inplace=True)
			df_temp = df_temp[['timestamp','msr_duration','temp_f']]
			return df_temp

		def init_hum_df():
			hum_lists=hum_dicts['values']
			df_hum=pd.DataFrame(hum_lists)
			df_hum['relativeHumidity'] = df_hum['value']
			df_hum['timestamp']=pd.to_datetime(df_hum['validTime'].map(lambda x: str(x).split('+')[0]))
			# set to local time from UTC (default)
			df_hum['timestamp']-=timedelta(hours=4)
			df_hum['msr_duration']=df_hum['validTime'].map(lambda x: calc_msr_duration(x))
			df_hum.drop(['validTime','value'],axis=1,inplace=True)
			df_hum = df_hum[['timestamp','msr_duration','relativeHumidity']]
			return df_hum

		def init_precip_df():
			precip_lists=precip_dicts['values']
			df_precip=pd.DataFrame(precip_lists)
			df_precip['probabilityOfPrecipitation'] = df_precip['value']
			df_precip['timestamp']=pd.to_datetime(df_precip['validTime'].map(lambda x: str(x).split('+')[0]))
			# set to local time from UTC (default)
			df_precip['timestamp']-=timedelta(hours=4)
			df_precip['msr_duration']=df_precip['validTime'].map(lambda x: calc_msr_duration(x))
			df_precip.drop(['validTime','value'],axis=1,inplace=True)
			df_precip = df_precip[['timestamp','msr_duration','probabilityOfPrecipitation']]
			return df_precip

		# initialize all dataframes
		df_temp = init_temp_df()
		df_hum = init_hum_df()
		df_precip = init_precip_df()
		# Expand all dataframes
		df_temp_expanded = expand_dataframe(df_temp)
		df_hum_expanded = expand_dataframe(df_hum)
		df_precip_expanded = expand_dataframe(df_precip)
		# Merge all three 
		dfs = [df_temp_expanded,df_hum_expanded,df_precip_expanded]
		df_final = reduce(lambda left,right: pd.merge(left,right,on='timestamp'), dfs)
		# Only show future times
		now = datetime.now()
		future_mask = df_final['timestamp']>now
		df_final = df_final[future_mask]
		# Now mask the forecast based on the user input
		temp_mask = (df_final['temp_f'] >= min_temp) & (df_final['temp_f'] <= max_temp)
		hum_mask = (df_final['relativeHumidity'] >= min_humidity) & (df_final['relativeHumidity'] <= max_humidity) 
		precip_mask = (df_final['probabilityOfPrecipitation'] >= min_precip) & \
			(df_final['probabilityOfPrecipitation'] <= max_precip)
		good_condis_mask = (temp_mask) & (hum_mask) & (precip_mask)
		df_good_condis = df_final[good_condis_mask]
		if len(df_good_condis) == 0:
			return render_template('main/condis_results.html',no_results=True)
		# Split up into groups by neighboring hours
		groups=splitme_zip(np.array(df_good_condis.index),d=1)
		all_print_strs = []
		for group in groups:
			print(group)
			mask = df_good_condis.index.isin(group)
			group_df = df_good_condis[mask]
			if len(group) > 1:
				first_timestamp = group_df['timestamp'].iloc[0]
				first_date = first_timestamp.date()
				first_time = first_timestamp.time()
				last_timestamp = group_df['timestamp'].iloc[-1]
				last_date = last_timestamp.date()
				last_time = last_timestamp.time()

				if first_date == last_date:
					print_str = f"{first_date}, from {first_time.strftime(time_format)} to {last_time.strftime(time_format)} "
				else:
					print_str = f"From {first_time.strftime(time_format)} on {first_date} to {last_time.strftime(time_format)} on {last_date} "
			else:
				timestamp = group_df['timestamp'].iloc[0]
				date = timestamp.date()
				time = timestamp.time()
				print_str = f"{date} at {time.strftime(time_format)}"
			all_print_strs.append(print_str)
		return render_template('main/condis_results.html',
			gps_str=gps_str,temp_str=temp_str,humidity_str=humidity_str,
			precip_str=precip_str,all_print_strs=all_print_strs,no_results=False)
	return render_template('main/setup_form.html',form=form)

@main.route("/find_grid/<latitude>/<longitude>",methods=['GET']) 
def find_grid(latitude,longitude): 	
	# Make GET request to weather API
	try:
		response = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}')
	except:
		# flash("Unable to reach weather API with those coordinates. Please try again later or with different coordinates")
		return 404
	# Convert response to python dict
	j=response.json()
	# print(j)
	# Get the grid code and x,y
	props=j['properties']
	grid_id = props['gridId']
	grid_x = props['gridX']
	grid_y = props['gridY']
	d={'grid_id':grid_id,'grid_x':grid_x,'grid_y':grid_y}
	# print("made it here")
	# print(grid_id,grid_x,grid_y)
	return jsonify(d)
	# return (grid_id,grid_x,grid_y)

# @main.route('/bokeh')
# def bokeh():

#     # init a basic bar chart:
#     # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
#     fig = figure(plot_width=600, plot_height=600)
#     fig.vbar(
#         x=[1, 2, 3, 4],
#         width=0.5,
#         bottom=0,
#         top=[1.7, 2.2, 4.6, 3.9],
#         color='navy'
#     )

#     # grab the static resources
#     js_resources = INLINE.render_js()
#     css_resources = INLINE.render_css()

#     # render template
#     script, div = components(fig)
#     html = render_template(
#         'index.html',
#         plot_script=script,
#         plot_div=div,
#         js_resources=js_resources,
#         css_resources=css_resources,
#     )
#     return encode_utf8(html)

# @main.route('/bokeh2')
# def bokeh2():

#     # Set up data
# 	N = 200
# 	x = np.linspace(0, 4*np.pi, N)
# 	y = np.sin(x)
# 	source = ColumnDataSource(data=dict(x=x, y=y))


# 	# Set up plot
# 	plot = figure(plot_height=400, plot_width=400, title="my sine wave",
# 	              tools="crosshair,pan,reset,save,wheel_zoom",
# 	              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

# 	plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# 	# Set up widgets
# 	text = TextInput(title="title", value='my sine wave')
# 	offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
# 	amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
# 	phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
# 	freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# 	# Set up callbacks
# 	def update_title(attrname, old, new):
# 	    plot.title.text = text.value

# 	text.on_change('value', update_title)

# 	def update_data(attrname, old, new):

# 	    # Get the current slider values
# 	    a = amplitude.value
# 	    b = offset.value
# 	    w = phase.value
# 	    k = freq.value

# 	    # Generate the new curve
# 	    x = np.linspace(0, 4*np.pi, N)
# 	    y = a*np.sin(k*x + w) + b

# 	    source.data = dict(x=x, y=y)

# 	for w in [offset, amplitude, phase, freq]:
# 	    w.on_change('value', update_data)


# 	# Set up layouts and add to document
# 	inputs = column(text, offset, amplitude, phase, freq)

# 	curdoc().add_root(row(inputs, plot, width=800))
# 	curdoc().title = "Sliders"
# 	# render template
# 	script, div = components(plot)
# 	# grab the static resources
# 	js_resources = INLINE.render_js()
# 	css_resources = INLINE.render_css()
# 	html = render_template(
# 	    'index.html',
# 	    plot_script=script,
# 	    plot_div=div,
# 	    js_resources=js_resources,
# 	    css_resources=css_resources,
# 	)
# 	return encode_utf8(html)