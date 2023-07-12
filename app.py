# Import the FastAPI and Request modules
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import json


async def jfy(data):
    if len(data[0][1].split()) < 10: return "অনুগ্রহ করে প্রসঙ্গে লিখিত শব্দ সংখ্যা দশ বা তার অধিক আছে কিনা তা নিশ্চিত করুন।"
    if len(data[0][1].split()) > 256: return "অনুগ্রহ করে প্রসঙ্গে লিখিত শব্দ সংখ্যা ২৫৬ এর কম আছে কিনা তা নিশ্চিত করুন।"

    this = {
        "context": "",
        "qas": [
            {
                "id": "",
                "is_impossible": "",
                "question": "",
                "answers": [
                    {
                        "text": "",
                        "answer_start": "",
                    }
                ],
            }
        ],
    }
    result = []
    current_question = ""
    current_answers = []

    for key, value in data:
        if key.startswith('question'):
            if current_question != "":
                result.append({
                    "id": "",
                    "is_impossible": "",
                    "question": current_question,
                    "answers": current_answers
                })
            current_question = value
            current_answers = []
        elif not key.startswith('answerC'):
            current_answers.append({
                "text": value,
                "answer_start": ""
            })

    result.append({
        "id": "",
        "is_impossible": "",
        "question": current_question,
        "answers": current_answers
    })
    this["context"] = data[0][1]
    this["qas"] = result
    pos = 3
    try: ans = int(data[3][1])
    except IndexError: return f"প্রশ্ন {1} এ উল্লেখিত শব্দ সংখ্যা ৩ অথবা ৩ এর অধিক হতে হবে"
    for i in range(int(data[1][1])):
        if len(this["qas"][i]["question"].split()) < 3: return f"প্রশ্ন {i+1} এ উল্লেখিত শব্দ সংখ্যা ৩ অথবা ৩ এর অধিক হতে হবে"
        if len(this["qas"][i]["question"].split()) > 32: return f"প্রশ্ন {i+1} এ উল্লেখিত শব্দ সংখ্যা ৩২ এর কম হতে হবে"
        for j in range(int(data[pos][1])):
            if len(this["qas"][i]["answers"][j]["text"].split()) < 1: return f"প্রশ্ন {i+1} এ উত্তর {j+1} এর উল্লেখিত শব্দ সংখ্যা ১ অথবা ১ এর অধিক হতে হবে"
            if len(this["qas"][i]["answers"][j]["text"].split()) > 32: return f"রশ্ন {i+1} এ উত্তর {j+1} এর উল্লেখিত শব্দ সংখ্যা ৩২ এর কম হতে হবে"
        
        pos += int(data[pos][1]) + 2
    with open("data.json", "a") as f:
        f.write(json.dumps(this)+',')
    
    


# Create an instance of the FastAPI class
app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# Create an instance of the Jinja2Templates class
templates = Jinja2Templates(directory="templates")

@app.get("/image_l")
def get_image():
    return FileResponse("templates/OIG.jpg")

@app.get("/image_h")
def get_image():
    return FileResponse("templates/OIG_.jpg")

@app.get("/logo")
def get_image():
    return FileResponse("templates/logo.jpg")

@app.get("/det1")
def get_image():
    return FileResponse("templates/det_1.jpg")

@app.get("/fnl")
def get_image():
    return FileResponse("templates/pt.jpg")

# Define a route for the home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/detl1", response_class=HTMLResponse)
def home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("details1.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("home.html", {"request": request})

# Define a route for the form submission
@app.post("/submit")
async def submit(request: Request):
    # Get the form data from the request
    
    form_data = await request.form()
    r = await jfy(list(zip(form_data.keys(), form_data.values())))
    if r is None: return templates.TemplateResponse("final.html", {"request": request})
    else: return templates.TemplateResponse("error.html", {"request": request, "error_message": r})
