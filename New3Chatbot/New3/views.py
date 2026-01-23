from django.shortcuts import render
from .services import ask_wit_ai
# Create your views here.
def chatbot_view(request):
    response = None
    
    if request.method =="POST":
        user_input = request.POST.get('user_input')
        response = ask_wit_ai(user_input)
    return render(request, 'chatbot.html',{'response': response})    





from django.views.decorators.http import require_http_methods

from .services import ask_wit_ai


@require_http_methods(["GET", "POST"])
def chatbot_view(request):
    response = None
    error = None

    if request.method == "POST":
        user_input = request.POST.get("user_input", "").strip()
        if not user_input:
            error = "Please enter a message."
        else:
            try:
                # ask_wit_ai returns the raw JSON response from Wit.ai
                response = ask_wit_ai(user_input)
            except Exception as exc:
                # Keep the message simple for users; log fuller details if needed
                error = f"Failed to contact Wit.ai: {exc}"

    return render(request, "chatbot.html", {"response": response, "error": error})