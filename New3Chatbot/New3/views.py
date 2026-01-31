from django.http import JsonResponse
from django.shortcuts import render
from .services import LLMClient

def chatbot_view(request):
    # 1️⃣ Show the chat UI
    if request.method == "GET":
        return render(request, "chatbot.html")

    # 2️⃣ Handle chat messages
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        client = LLMClient()
        ai_reply = client.generate_reply(user_message)

        return JsonResponse({"reply": ai_reply})
import os
print("GROQ KEY:", os.getenv("GROQ_API_KEY"))