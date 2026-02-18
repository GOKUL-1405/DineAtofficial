import json
import logging
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini API
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    model = None

# Project Description for Context
PROJECT_INFO = """
Project Name: DineAt Premium Restaurant Management System

Description:
DineAt is a comprehensive restaurant management system built with Django (backend) and MySQL (database). It facilitates seamless interaction between customers, kitchen staff, and administrators.

Core Technologies:
- Backend: Django (Python)
- Database: MySQL
- Frontend: HTML, CSS (Vanilla), JavaScript

User Roles & Features:

1. Customer:
   - Account Management: Sign up, Login, Logout, Profile update.
   - Ordering: Browse menu, Select tables, Add items to cart, Place orders.
   - History: View past order history and status.
   - Authentication: Customer login, Sign up routes available.

2. Kitchen Staff:
   - Dashboard: Real-time view of incoming orders.
   - Order Management: Update status of order items (e.g., Pending -> Preparing -> Ready -> Served).
   - Notifications: Alerted when new orders arrive.

3. Administrator:
   - Dashboard: Overview of total orders, revenue, and active users.
   - Management: Add/Edit/Delete menu items, manage users, configure system settings.

Key Functionalities:
- Real-time order updates for the kitchen.
- Secure role-based authentication.
- Responsive design for mobile and desktop users.

Scope of this bot:
- Answer technical questions about the DineAt project architecture.
- Explain features available to different user roles.
- Provide details on the technology stack used.
"""

@csrf_exempt
@require_http_methods(["POST"])
def chat_view(request):
    """
    API Endpoint for the Chatbot.
    Accepts JSON: {"message": "user question"}
    Returns JSON: {"reply": "bot response"}
    """
    if not model:
        return JsonResponse({"error": "Chatbot service is currently unavailable."}, status=503)

    try:
        # Parse Request Body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({"error": "Message field is required."}, status=400)

        # Construct Prompt
        prompt = f"""You are a chatbot for a specific software project.

Project details:
{PROJECT_INFO}

Rules:
* Answer only from project details
* Do not use external knowledge
* If unrelated question, reply exactly: "This question is outside the project scope."
* Keep answers concise and helpful.

User question:
{user_message}"""

        # Generate Response
        response = model.generate_content(prompt)
        
        # Extract Text
        bot_reply = response.text.strip()

        return JsonResponse({"reply": bot_reply})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return JsonResponse({"error": f"An internal error occurred: {str(e)}"}, status=500)
