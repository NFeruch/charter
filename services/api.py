# clear && uvicorn backend.api:app --reload
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .integrations.trello import get_auth_url, get_boards, get_single_board, get_lists, create_job_card
import os

app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

def get_token():
    token_path = 'token.txt'
    if not os.path.isfile(token_path):
        return RedirectResponse(url='/authorize')

    with open(token_path, 'r') as f:
        lines = f.readlines()
        if len(lines) != 1 or not lines[0].strip():
            return RedirectResponse(url='/authorize')

    return lines[0].strip()

@app.get('/')
async def home():
    return {'Hello': 'World'}

@app.get('/authorize')
async def authorize():
    return RedirectResponse(get_auth_url())

@app.get('/save_token')
async def save_token(token: str):
    with open('token.txt', 'w') as f:
        f.write(token)
    return RedirectResponse(url='/static/success.html')

@app.get('/get_boards')
async def get_boards_route(token: str = Depends(get_token)):
    if isinstance(token, RedirectResponse):
        return token
    
    return get_boards(token)

@app.get('/get_boards_clean')

@app.get('/get_board/{board_id}')
async def get_board_route(board_id: str, token: str = Depends(get_token)):
	if isinstance(token, RedirectResponse):
		return token
	board = get_single_board(board_id, token)
	return board

@app.get('/get_lists/{board_id}')
async def get_lists_route(board_id: str, token: str = Depends(get_token)):
	if isinstance(token, RedirectResponse):
		return token
	lists = get_lists(board_id, token)
	return lists

@app.get('/create_job_card')
async def create_job_card_route(list_id: str, title: str, desc: str, token: str = Depends(get_token)):
    if isinstance(token, RedirectResponse):
        return token
    card = create_job_card(list_id, title, desc, token)
    return card

@app.get('/extract_job_info')
async def extract_job_info_route():
	pass