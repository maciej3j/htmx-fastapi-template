import io
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

storage = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(excel_file: UploadFile = File(...), pdf_file: UploadFile = File(...)):
    file_id = "przykładowe-id"

    return f"""
    <div class="w-full animate-in fade-in zoom-in duration-300">
        <div class="bg-custom-powder border-l-4 border-custom-red p-6 rounded-r-xl shadow-md">
            <div class="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h3 class="text-custom-blue font-bold text-lg">Analiza zakończona!</h3>
                    <p class="text-custom-red text-sm font-medium">Gotowy PDF czeka na pobranie.</p>
                </div>
                <div class="flex gap-3">
                    <a href="/download/{file_id}" 
                       class="btn-default !bg-custom-red hover:!bg-custom-blue shadow-md transition-colors">
                       Pobierz plik
                    </a>
                    <button hx-get="/" hx-target="body" 
                            class="text-custom-blue-light hover:text-custom-blue font-semibold text-sm underline underline-offset-4">
                       Zacznij od nowa
                    </button>
                </div>
            </div>
        </div>
    </div>
    """


@app.get("/download/{file_id}")
async def download(file_id: str):
    file_data = storage.get(file_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="Plik wygasł lub nie istnieje")

    return StreamingResponse(
        io.BytesIO(file_data["content"]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={file_data['filename']}"
        },
    )
