from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.recommender import recommend
from app.llm import parse_preferences

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/recommend", response_class=HTMLResponse)
async def get_recommendation(request: Request, user_input: str = Form(...)):
    try:
        prefs = parse_preferences(user_input)
        results = recommend(prefs, top_n=3)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "results": results,
                "user_input": user_input,
                "prefs": prefs
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(e),
                "user_input": user_input
            }
        )