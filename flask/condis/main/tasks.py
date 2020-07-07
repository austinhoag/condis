from condis import cel, db

@cel.task
def send_daily_emails():
	print(db.User())
	return "Sent daily emails"
