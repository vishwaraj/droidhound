import requests

def push_msg(package,current_version):

	data = [
	('key', '53jHSm'),
	('title', package),
	('msg', 'Newer Version '+current_version+' detected \nStarted pwning!'),]
	requests.post('https://api.simplepush.io/send', data=data)
