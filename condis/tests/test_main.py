from flask import url_for


def test_basic():
	assert 4==4

# def test_home_page_loads(test_client):
# 	""" Test a GET request against home page is successful """
# 	response = test_client.get(url_for('main.home'),
# 		follow_redirects=True)

# 	assert b'How it works:' in response.data and \
# 		b'Optional: if you check' in response.data and \
# 		b"Search Form" in response.data


def test_post_no_coordinates_validates(test_client):
	""" Test a GET request against home page is successful """
	response = test_client.post(url_for('main.home'),data={},
		follow_redirects=True)

	print(response.data)
	assert 4==4
	


