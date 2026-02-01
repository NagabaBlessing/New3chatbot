from django.shortcuts import render
from .services.LLMClient import LLMClient

def chatbot_view(request):
    response_text = None
    error = None
    user_input = ""

    if request.method == "POST":
        user_input = request.POST.get("user_input")

        try:
            client = LLMClient()
            response_text = client.generate_reply(user_input)
        except Exception as e:
            error = str(e)

    return render(
        request,
        "chatbot.html",
        {
            "bot_reply": response_text,
            "user_input": user_input,
            "error": error,
        }
    )
