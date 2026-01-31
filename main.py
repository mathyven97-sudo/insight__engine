from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import endpoints
import os

app = FastAPI(title=settings.PROJECT_NAME) # instead of js node

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
# Ensure the directory exists
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
templates = Jinja2Templates(directory=templates_dir)

# API Router
app.include_router(endpoints.router, prefix=settings.API_V1_STR)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": settings.PROJECT_NAME,
        "active_page": "overview"
    })

@app.get("/insights")
async def read_insights(request: Request):
    return templates.TemplateResponse("llm_insights.html", {
        "request": request, 
        "title": "LLM Insights - " + settings.PROJECT_NAME,
        "active_page": "insights"
    })

@app.get("/search")
async def read_search(request: Request):
    return templates.TemplateResponse("deep_search.html", {
        "request": request, 
        "title": "Deep Search - " + settings.PROJECT_NAME,
        "active_page": "search"
    })

@app.get("/settings")
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {
        "request": request, 
        "title": "Settings - " + settings.PROJECT_NAME,
        "active_page": "settings"
    })
