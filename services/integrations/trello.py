import requests
import os
import json
from typing import List, Dict, Literal
from httpx import QueryParams
from dotenv import load_dotenv
from pydantic import BaseModel
from models.trello import Label, CardInputParams

load_dotenv()


class TrelloAuth:
	'''
	Methods to authenticate with trello
	'''
	BASE_API_URL = 'https://api.trello.com/1'

	def __init__(self, api_key: str, api_token: str) -> None:
		self.api_key = api_key or os.getenv('TRELLO_API_KEY')
		self.token = api_token or os.getenv('TRELLO_API_TOKEN')

	def auth_url(self, extra_params: dict | None = None) -> str:
		params = {
			'name': 'Trello Job Application Tracker',
			'scope': 'read,write',
			'expiration': 'never',
			'response_type': 'token',
			'return_url': 'http://localhost:8000/static/callback.html',
			'callback_method': 'fragment',
			'key': self.api_key,
			**(extra_params or {})
		}

		return f"{self.BASE_API_URL}/authorize?{QueryParams(params)}"

	def save_token_local(self, token: str) -> Dict:
		with open('token.txt', 'w') as f:
			f.write(token)
		return {'message': 'Token saved successfully'}


class TrelloGet(TrelloAuth):
	'''
	Methods to access trello boards, lists and cards
	'''
	def __init__(
			self, 
			api_key: str | None = None, 
			api_token: str | None = None
		) -> None:
		super().__init__(api_key, api_token)
		self.default_params = QueryParams({
			'key': self.api_key,
			'token': self.token
		})

	def boards(self, filter_board_name: str | None = None) -> List[Dict]:
		'''
		Get all trello boards that the user is a member of
		'''
		url = f"{self.BASE_API_URL}/members/me/boards?{self.default_params}"
		response = requests.get(url).json()

		if filter_board_name:
			response = list(filter(
				lambda board_json: board_json['name'] == filter_board_name and not board_json['closed'],
				response
			))

			if len(response) == 0:
				return {'message': 'The filter returned no results'}
			
		return response
	
	def one_board(self, board_id: str) -> Dict:
		'''
		Get a single trello board by id or name
		'''
		url = f"{self.BASE_API_URL}/boards/{board_id}?{self.default_params}"
		response = requests.get(url)
		if response.status_code == 200:
			return response.json()
		else:
			# assume board_id is the board name
			response = TrelloGet().boards(filter_board_name=board_id)
			if 'message' in response:
				return {'message': 'Board not found by name or id'}
			return response[0]
	
	def lists(self, board_id: str) -> List[Dict]:
		'''
		Get all lists on a trello board
		'''
		url = f"{self.BASE_API_URL}/boards/{board_id}/lists?{self.default_params}"
		response = requests.get(url).json()
		return response
	
	def one_list(self, list_id: str) -> Dict:
		'''
		Get a single list on a trello board
		'''
		url = f"{self.BASE_API_URL}/lists/{list_id}?{self.default_params}"
		response = requests.get(url).json()
		return response
	
	def cards(self, list_id: str) -> List[Dict]:
		'''
		Get all cards in a trello list
		'''
		url = f"{self.BASE_API_URL}/lists/{list_id}/cards?{self.default_params}"
		response = requests.get(url).json()
		return response
	
	def one_card(self, card_id: str) -> Dict:
		'''
		Get a single card in a trello list
		'''
		url = f"{self.BASE_API_URL}/cards/{card_id}?{self.default_params}"
		response = requests.get(url).json()
		return response
	
	def labels(self, board_id: str) -> List[Dict]:
		'''
		Get all labels on a trello board
		'''
		url = f"{self.BASE_API_URL}/boards/{board_id}/labels?{self.default_params}"
		response = requests.get(url).json()
		return response
	
	def one_label(self, label_id: str) -> Dict:
		'''
		Get a single label on a trello board
		'''
		url = f"{self.BASE_API_URL}/labels/{label_id}?{self.default_params}"
		response = requests.get(url).json()
		return response
	

class TrelloCreate(TrelloAuth):
	'''
	Methods to create new trello boards, lists and cards
	'''
	def __init__(self, api_key: str | None = None, api_token: str | None = None) -> None:
		super().__init__(api_key, api_token)
		self.default_params = QueryParams({
			'key': self.api_key,
			'token': self.token
		})

	def board(self, board_name: str, extra_params: Dict | None = None) -> Dict:
		'''
		Create a new trello board
		'''
		extra_params = {
			'name': board_name,
			'desc': 'A board to track job applications',
			'defaultLists': 'false',
			# TODO: Figure out if we can add a custom background image
			**(extra_params or {})
		}
		url = f"{self.BASE_API_URL}/boards?{self.default_params}&{QueryParams(extra_params)}"
		response = requests.post(url).json()
		return response
	
	def list(self, board_id: str, list_name: str, pos: Literal['top', 'bottom'] = 'top') -> Dict:
		'''
		Create a new list on a trello board
		'''
		url = f"{self.BASE_API_URL}/lists?{self.default_params}&{QueryParams({'name': list_name, 'idBoard': board_id, 'pos': pos})}"
		response = requests.post(url).json()
		return response
	
	def card(self, card_data: CardInputParams) -> Dict:
		'''
		Create a new card in a trello list
		'''
		url = f"{self.BASE_API_URL}/cards?{self.default_params}&{QueryParams(card_data)}"
		response = requests.post(url).json()
		return response
	
	def board_label(self, board_id: str, label_name: Label.name, label_color: Label.color) -> Dict:
		'''
		Create a new label for a trello board
		'''
		url = f"{self.BASE_API_URL}/labels?{self.default_params}&{QueryParams({'name': label_name, 'color': label_color, 'idBoard': board_id})}"
		response = requests.post(url).json()
		return response
	
	def card_label(self, card_id: str, label_id: str) -> Dict:
		'''
		Add a label to a card
		'''
		url = f"{self.BASE_API_URL}/cards/{card_id}/idLabels?{self.default_params}&{QueryParams({'value': label_id})}"
		response = requests.post(url).json()
		return response


class StarterBoard:
	def __init__(
			self,
			board_name: str = 'Charter Job Application Tracker',
			list_names: List[str] = ['Applied', 'Interview', 'Offer', 'Rejected'],
			api_key: str | None = None,
			api_token: str | None = None
		) -> None:
		self.get = TrelloGet(api_key, api_token)
		self.create = TrelloCreate(api_key, api_token)

		self.board_name = board_name
		self.list_names = list_names

		self.starter_board_id = None
		self.starter_lists_ids = None
	
	def is_already_setup(self) -> bool:
		"""
		Check if the starter board has already been setup,
		i.e., if the board exists and has the correct lists.
		"""
		all_boards = self.get.boards()
		
		# Find the most recently active board with the specified name that is not closed
		starter_board = next(
			(
				board 
				for board in sorted(all_boards, key=lambda b: b['dateLastActivity'] or '', reverse=True)
				if board['name'] == self.board_name and not board['closed']
			), None
		)
		
		if not starter_board:
			return False
		
		# Retrieve lists from the starter board
		all_lists = self.get.lists(starter_board['id'])
		starter_lists = [list['name'] for list in all_lists]
		
		# Store the starter board and lists IDs
		self.starter_board_id = {starter_board['name']: starter_board['id']}
		self.starter_lists_ids = {list['name']: list['id'] for list in all_lists} if starter_lists else None
		
		# Check if the retrieved lists match the required list names
		return set(starter_lists) == set(self.list_names)

	
	def one_time_setup(self) -> Dict:
		if self.is_already_setup():
			return {'message': 'Starter board already setup'}

		starter_board = self.create.board(self.board_name)
		starter_lists = [
			self.create.list(starter_board['id'], list_name, 'bottom') 
			for list_name in self.list_names
		]
		card = self.create.card(starter_lists[0]['id'], 'You\'re 1 step closer to landing a job!', 'This is a card to help you get started with your job application tracker. Move this card to the next list as you progress through the job application process.')

		self.starter_board_id = {
			starter_board['name']: starter_board['id']
		} if starter_board else None
		self.starter_lists_ids = {
			list_json['name']: list_json['id'] for list_json in starter_lists
		} if starter_lists else None

		return {'board': starter_board, 'lists': starter_lists, 'card': card}
	
	def display_all_ids(self):
		if not self.is_already_setup():
			self.one_time_setup()

		return json.dumps({
			'board_id': self.starter_board_id,
			'list_ids': self.starter_lists_ids
		}, indent=4)
		

if __name__ == '__main__':
	print(json.dumps(
		# StarterBoard().display_all_ids()
		TrelloCreate().board_label('66aada42ebce138ab1ce192d', 'Big Company', '#eb4034')
	, indent=4))
