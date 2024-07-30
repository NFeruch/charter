import requests
import os
import json
from typing import List, Dict
from httpx import QueryParams
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TRELLO_API_KEY')
API_TOKEN = os.getenv('TRELLO_API_TOKEN')
BASE_API_URL = 'https://api.trello.com/1'

def get_auth_url(extra_params: dict | None = None) -> str:
	params = {
		'expiration': 'never',
		'name': 'Trello Job Application Tracker',
		'scope': 'read,write',
		'response_type': 'token',
		'key': API_KEY,
		'return_url': 'http://localhost:8000/static/callback.html',
		'callback_method': 'fragment',
		**(extra_params or {})
	}

	return f"{BASE_API_URL}/authorize?{QueryParams(params)}"

def get_boards(token: str) -> List[Dict]:
	url = f"{BASE_API_URL}/members/me/boards?{QueryParams({'key': API_KEY, 'token': token})}"
	response: List[Dict] = requests.get(url).json()

	# Sort boards by date of last activity
	response = sorted(response, key=lambda x: x['dateLastActivity'], reverse=True)

	return response

def get_single_board(board_id: str, token: str) -> Dict:
	url = f"{BASE_API_URL}/boards/{board_id}?{QueryParams({'key': API_KEY, 'token': token})}"
	response = requests.get(url)

	return response.json()

def get_lists(board_id: str, token: str) -> List[Dict]:
	url = f"{BASE_API_URL}/boards/{board_id}/lists?{QueryParams({'key': API_KEY, 'token': token})}"
	response = requests.get(url)

	return response.json()

def create_job_card(list_id: str, title: str, desc: str, token: str) -> Dict:
	params = {
		'key': API_KEY,
		'token': token,
		'idList': list_id,
		'name': title,
		'desc': desc,
		'pos': 'top'
	}
	url = f"{BASE_API_URL}/cards?{QueryParams(params)}"
	response = requests.post(url)

	return response.json()