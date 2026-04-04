from app.database import SessionLocal, Rating, init_db
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.recommender import recommend
from app.llm import parse_preferences

app = FastAPI()
init_db()

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
@app.post("/rate", response_class=HTMLResponse)
async def rate_coffee(
    request: Request,
    coffee_name: str = Form(...),
    user_input: str = Form(...),
    stars: int = Form(...)
):
    db = SessionLocal()
    try:
        rating = Rating(
            coffee_name=coffee_name,
            user_input=user_input,
            stars=stars
        )
        db.add(rating)
        db.commit()
    finally:
        db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"rated": coffee_name, "stars": stars}
    )    