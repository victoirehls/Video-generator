# pip install requests
import json
import requests
import tempfile
import shutil

api_base_url = 'https://api.moneyeti.com/api/1.0/'
country_info_api_url = api_base_url+'currencyGeneralWidget/country/{0}/info/{1}'
city_name_api_url_0 = api_base_url+'grammar/locationId/{0}/lang/{1}'
city_name_api_url = api_base_url+'location/{0}/lang/{1}'
tipping_api_url = api_base_url+'/localLifeWidget/country/{0}/lang/{1}'
budget_api_url = api_base_url+'/location/{0}/budget/lang/{1}'
payment_api_url = api_base_url+'/paymentPreference/country/{0}'
photo_api_url = api_base_url+'photoheader/{0}'
headers = {'Content-Type': 'application/json'}

def get_city_name0(location_id, iso_639):
	resp = requests.get(city_name_api_url_0.format(location_id, iso_639), headers=headers)
	info_resp = None
	if resp.status_code == 200:
		data = json.loads(resp.content.decode('utf-8'))
	return data['grammarLocation']['grammar']

def get_city_name(location_id, iso_639):
	resp = requests.get(city_name_api_url.format(location_id, iso_639), headers=headers)
	data = None
	if resp.status_code == 200:
		data = json.loads(resp.content.decode('utf-8'))
		data = data['singleLocation']['name']
	return data

def get_currency(iso_3166, iso_639):
	resp = requests.get(country_info_api_url.format(iso_3166,iso_639), headers=headers)
	data = None
	if resp.status_code == 200:
		data = json.loads(resp.content.decode('utf-8'))
		data = data['currencyGeneralInfoWidget']['currencyLocalSentence']
	return data

def get_tipping(iso_3166, iso_639):
	resp = requests.get(tipping_api_url.format(iso_3166, iso_639), headers=headers)
	data = None
	if resp.status_code == 200:
		data = json.loads(resp.content.decode('utf-8'))
		data = data['localLifeWidget']['tipExpetedSentence']
	return data

def get_budget(location_id, iso_639):
	resp = requests.get(budget_api_url.format(location_id, iso_639), headers=headers)
	data = None
	if resp.status_code == 200:
		data = json.loads(resp.content.decode('utf-8'))
		data = data['budgetBE']['localBudget']['mid']
	return data

def get_payment_info(iso_3166):
	resp = requests.get(payment_api_url.format(iso_3166), headers=headers)
	data = None
	if resp.status_code == 200:
		data = json.loads(resp.content.decode('utf-8'))
		data = data['paymentInformations']
	return data

def get_photos(location_id):
	resp = requests.get(photo_api_url.format(location_id), headers=headers)
	img_resp = None
	photos_array = []
	if resp.status_code == 200:
		data = json.loads(resp.content.decode('utf-8'))
		for photo in data['photoHeader']['photo']:
			downloaded_file = download_file(photo['imageUrl'])
			if downloaded_file != None:
				photos_array.append(downloaded_file[1])
	return photos_array

def download_file(file_url):
	stream = requests.get(file_url, stream = True)
	targetfilepath = None
	if stream.status_code == 200:
		stream.raw.decode_content = True
		filename = file_url.split("/")[-1]
		tmp_file = tempfile.mkstemp(suffix=filename)
		with open(tmp_file[1],'wb') as targetfile:
			shutil.copyfileobj(stream.raw, targetfile)
			targetfilepath = tmp_file
	return targetfilepath

iso_639_language = 'fr'

# location_id = 'wnvanw' # Paris
# iso_3166_country = 'fr'
# location_id = 'ewxe8j' # Hong-Kong
# iso_3166_country = 'hk'
location_id = 'ozkjra' # New-york
iso_3166_country = 'us'
# location_id = 'rx4q6m' # Berlin
# iso_3166_country = 'de'
# location_id = 'p8xoyx' # London
# iso_3166_country = 'gb'


print(get_city_name(location_id, iso_639_language))
print(get_currency(iso_3166_country, iso_639_language))
print(get_tipping(iso_3166_country, iso_639_language))
print('budget moyen: '+str(get_budget(location_id, iso_639_language)))
payment_info = get_payment_info(iso_3166_country)
print(payment_info)
print('vat: '+str(payment_info['vatRate'])+', contactlessLimit:'+str(payment_info['contactlessLimit'])+', paymentPreference: '+payment_info['paymentPreference'])
print(get_photos(location_id))