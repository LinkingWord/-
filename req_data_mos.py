import json
import requests


def get_data_mos(url):
	result = requests.get(url)
	if result.status_code == 200:
		return result.json()
	else:
		print('Что-то пошло не так')


if __name__ == '__main__':
	data = get_data_mos('https://apidata.mos.ru/v1/datasets/1903/rows?api_key=ecfad8408c3e025cb29fa7130aac2048&$top=1000')
	
	with open('places.json', 'w', encoding='utf-8') as places:
		json.dump(data, places)