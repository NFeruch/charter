# clear && uvicorn services.api:app --reload
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .integrations.trello import get_auth_url, get_boards, get_single_board, get_lists, create_job_card
from .ai import get_ai_completions
import os
from markdownify import markdownify

app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins as needed
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods, including POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

def get_token():
    token_path = 'token.txt'
    if not os.path.isfile(token_path):
        return HTTPException(status_code=404, detail='Token file not found')

    with open(token_path, 'r') as f:
        lines = f.readlines()
        if len(lines) != 1 or not lines[0].strip():
            return HTTPException(status_code=404, detail='Token file is empty')

    return lines[0].strip()

@app.get('/')
async def home():
    return {'Hello': 'World'}

@app.get('/is_authenticated')
async def user_is_authenticated():
    token_path = 'token.txt'

    if not os.path.isfile(token_path):
        raise HTTPException(status_code=404, detail='Token file not found')

    if os.stat(token_path).st_size == 0:
        raise HTTPException(status_code=404, detail='Token file is empty')

    return {'is_authenticated': True}

@app.get('/authorize')
async def authorize():
    return RedirectResponse(get_auth_url())

@app.get('/save_token')
async def save_token(token: str):
    with open('token.txt', 'w') as f:
        f.write(token)
    return {'message': 'Token saved successfully'}

@app.post('/job-description-html-to-markdown')
async def html(request: Request):
    html = await request.body()
    return markdownify(html)

@app.get('/get_boards')
async def get_boards_route(token: str = Depends(get_token)):
    if isinstance(token, RedirectResponse):
        return token
    
    return get_boards(token)

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