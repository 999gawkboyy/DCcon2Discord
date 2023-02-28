from urllib import response
import requests
import base64

def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')

def PutEmoji(name, channel, image, token) :

	url = f'https://discord.com/api/v9/guilds/{channel}/emojis'
	print(token)

	headers = {
		'authorization': token,
	}

	img = image_to_data_url(image)
	print(img)

	payload = {
		'image': img,
		'name': 'qwe123'
	}

	response = requests.post(url, headers=headers, json=payload)
	print(response.status_code)
	if response.status_code != 201:
		print("fail")
	else:
		print("success")