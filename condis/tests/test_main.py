from flask import url_for


def test_home_page_loads(test_client):
	""" Test a GET request against home page is successful """
	response = test_client.get(url_for('main.home'),
		follow_redirects=True)

	assert b'How it works:' in response.data and \
		b'Optional: if you check' in response.data and \
		b"Search Form" in response.data


