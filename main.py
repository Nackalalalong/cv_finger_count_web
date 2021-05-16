from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

image_pairs = [
    
]

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request, 'image_pairs': image_pairs})

def is_args_valid(req):
    if 'data' not in req:
        return False
    if type(req['data']) is not list:
        return False
    for pair in req['data']:
        if len(pair) != 3:
            return False
    return True

@app.post('/add_images', status_code=200)
async def add_images(request: Request):
    global image_pairs
    res = await request.json()
    if not is_args_valid(res):
        return HTTPException(status_code=400, detail='invalid data')
    data = res['data']
    image_pairs = data + image_pairs

    return {'status': 'success'}

@app.post('/edit_image', status_code=200)
async def edit_image(request: Request):
    global image_pairs
    res = await request.json()
    if 'data' not in res or len(res['data']) != 3:
        return HTTPException(status_code=400, detail='invalid data')
    try:
        id = int(res['data'][2])
    except:
        return HTTPException(status_code=400, detail='invalid data')
    for index,(_,_,image_id) in enumerate(image_pairs):
        if image_id == id:
            image_pairs[index] = res['data']
            break
    return {'status': 'success'}

@app.post('/delete_image/{id}', status_code=200)
async def delete_image(request: Request, id: int):
    global image_pairs
    for index,(_,_,image_id) in enumerate(image_pairs):
        if image_id == id:
            image_pairs = image_pairs[:index] + image_pairs[index+1:]
            break
    return {'status': 'success'}