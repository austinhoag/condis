from flask import url_for


# def test_home_page_loads(test_client):
# 	""" Test a GET request against home page is successful """
# 	response = test_client.get(url_for('main.home'),
# 		follow_redirects=True)

# 	assert b'How it works:' in response.data and \
# 		b'Optional: if you check' in response.data and \
# 		b"Search Form" in response.data


def test_post_no_coordinates_validates(test_client):
	""" Test a GET request against home page is successful """
	
	gps_str = '36.131,-115.425'

	time = '9 AM - 4 PM'
	temp = '30 - 60'
	humidity = '0 - 50'
	precip = '0 - 30'
	data = {
		'gps_str':gps_str,
		'time':time,
		'temp':temp,
		'humidity':humidity,
		'precip':precip,
		'submit':True}
	response = test_client.post(url_for('main.home'),data=data,
		follow_redirects=True)
	assert b'How it works:' in response.data
	# assert 4==4
	


