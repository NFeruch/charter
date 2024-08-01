import os
from typing import Dict, List, Literal
import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Column(BaseModel):
	name: str
	type: str
	description: str | None
	options: Dict[str, str] | None


class TableSchema(BaseModel):
	name: str
	description: str | None
	fields: List[Column]


class AirtableAuth:
	BASE_API_URL = 'https://api.airtable.com/v0'

	def __init__(self, access_token: str) -> None:
		self.access_token = access_token or os.getenv('AIRTABLE_ACCESS_TOKEN')


class AirtableGet(AirtableAuth):
	def __init__(self, access_token: str | None = None) -> None:
		super().__init__(access_token)

	def base(self, base_name: str) -> None:
		pass

	def table(self, table_name: str) -> None:
		pass


class AirtableCreate(AirtableAuth):
	def __init__(self, access_token: str | None = None) -> None:
		super().__init__(access_token)

	def base(self, base_name: str, table_schemas: Dict | None = None) -> None:
		url = "https://api.airtable.com/v0/meta/bases"
		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
		}
		data = {
			"name": "Apartment Hunting",
			"tables": [
				{
					"description": "A to-do list of places to visit",
					"fields": [
						{
							"description": "Name of the apartment",
							"name": "Name",
							"type": "singleLineText"
						},
						{
							"name": "Address",
							"type": "singleLineText"
						},
						{
							"name": "Visited",
							"options": {
								"color": "greenBright",
								"icon": "check"
							},
							"type": "checkbox"
						}
					],
					"name": "Apartments"
				}
			],
			"workspaceId": "wsptqNGXeruu5OQj5?"
		}

		response = requests.post(url, headers=headers, json=data)
		print(response.text)
		return response.json()

	def table(self, base_name: str, table_schema: TableSchema) -> None:
		url = f"{self.BASE_API_URL}/meta/bases/{base_name}/tables"
		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}

		response = requests.post(url, headers=headers, json=table_schema)
		response.raise_for_status()
		return response.json()


class StarterTable:
	default_table_schema = [
		{
			"name": "Charter Job Application Tracker",
			"description": "A table to track job applications",
			"workspaceId": "wsptqNGXeruu5OQj5?",
			"fields": [
				{
					"name": "Position",
					"type": "singleLineText"
				},
				{
					"name": "Company",
					"type": "singleLineText"
				},
				{
					"name": "Location",
					"type": "singleLineText"
				},
				{
					"name": "Status",
					"type": "singleSelect",
					"options": [
						{
							"name": "Applied"
						},
						{
							"name": "Interviewing"
						},
						{
							"name": "Offered"
						},
						{
							"name": "Rejected"
						}
					]
				},
				{
					"name": "Notes",
					"type": "longText"
				}
			]
		}
	]

	def __init__(
			self,
			base_name: str = 'Charter Job Base',
			table_name: str = 'Charter Job Application Tracker',
			access_token: str | None = None
		) -> None:
		self.get = AirtableGet(access_token)
		self.create = AirtableCreate(access_token)

		self.base_name = base_name
		self.table_name = table_name

	def is_already_setup(self) -> bool:
		pass

	def one_time_setup(self) -> None:
		self.create.base(self.base_name, self.default_table_schema)

	def display_all_ids(self) -> None:
		pass


if __name__ == '__main__':
	print(
		StarterTable().one_time_setup()
	)
