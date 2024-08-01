from pydantic import BaseModel
from enum import Enum
from typing import List, Literal

class Label(BaseModel):
	name: str

	# class Color(str, Enum):
	# 	YELLOW = 'yellow'
	# 	PURPLE = 'purple'
	# 	BLUE = 'blue'
	# 	RED = 'red'
	# 	GREEN = 'green'
	# 	ORANGE = 'orange'
	# 	BLACK = 'black'
	# 	SKY = 'sky'
	# 	PINK = 'pink'
	# 	LIME = 'lime'
	# 	NULL = 'null'
		
	# color: Color
	

class CardInputParams(BaseModel):
	idList: str
	name: str | None
	desc: str | None
	pos: Literal['top', 'bottom'] | None
	due: str | None
	start: str | None
	dueComplete: bool | None
	idMembers: List[str] | None
	idLabels: List[str] | None
	urlSource: str | None
	fileSource: str | None
	mimeType: str | None
	idCardSource: str | None
	keepFromSource: str | None
	address: str | None
	locationName: str | None
	coordinates: str | None
