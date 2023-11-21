from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("your_firebase_key.json")
firebase_admin.initialize_app(cred)
database = firestore.client()
collection = database.collection("textDatabase")

def landing_page(request):
    return render(request, 'landing.html')

def home_page(request):
    return render(request, 'home.html')

def details1_page(request):
    return render(request, 'details1.html')

def final_page(request):
    return render(request, 'final.html')

def error_page(request, context={}):
    return render(request, 'error.html', context)

def submit_form(request):
    if request.method == 'POST':
        context = request.POST.get('context')  # Get the 'context' field value
        if len(context.split()) < 10: return error_page(request, {"error_message": "অনুগ্রহ করে প্রসঙ্গে লিখিত শব্দ সংখ্যা দশ বা তার অধিক আছে কিনা তা নিশ্চিত করুন।"})
        if len(context.split()) > 256: return error_page(request, {"error_message": "অনুগ্রহ করে প্রসঙ্গে লিখিত শব্দ সংখ্যা ২৫৬ এর কম আছে কিনা তা নিশ্চিত করুন।"})
        number = request.POST.get('number')  # Get the 'number' field value

        # Loop through the dynamic question and answer fields
        questions = []
        try:
            for i in range(int(number)):
                question = request.POST.get('question' + str(i + 1))
                if len(question.split()) < 3 : return error_page(request, {"error_message": f"প্রশ্ন {i+1} এ উল্লেখিত শব্দ সংখ্যা ৩ অথবা ৩ এর অধিক হতে হবে"}) 
                if len(question.split()) > 32: return error_page(request, {"error_message": f"প্রশ্ন {i+1} এ উল্লেখিত শব্দ সংখ্যা ৩২ এর কম হতে হবে"}) 
                answer_count = int(request.POST.get('answerCount' + str(i + 1)))
                answers_for_question = []
                if answer_count == 0: error_page(request, {"error_message": f"প্রশ্ন {i+1} এ উত্তর {j+1} এর উল্লেখিত শব্দ সংখ্যা ১ অথবা ১ এর অধিক হতে হবে"})
                for j in range(answer_count):
                    answer = request.POST.get('answer' + str(i + 1) + '_' + str(j + 1))
                    if len(answer.split()) < 1: return error_page(request, {"error_message": f"প্রশ্ন {i+1} এ উত্তর {j+1} এর উল্লেখিত শব্দ সংখ্যা ১ অথবা ১ এর অধিক হতে হবে"})
                    if len(answer.split()) > 32: return error_page(request, {"error_message": f"প্রশ্ন {i+1} এ উত্তর {j+1} এর উল্লেখিত শব্দ সংখ্যা ৩২ এর কম হতে হবে"}) 
                    answers_for_question.append(answer)

                questions.append({'question': question, 'answers': answers_for_question})
        except Exception as e:
            return error_page(request, {"error_message": f"প্রশ্ন {i+1} এ উল্লেখিত শব্দ সংখ্যা ৩ অথবা ৩ এর অধিক হতে হবে"})
        finally:
            collection.document().set({"data":questions})
            return final_page(request)
    else:
        # Handle GET request or other request methods if needed
        return render(request, 'error.html')
