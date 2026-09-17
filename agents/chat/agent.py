from urllib import response
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

from core.config.settings import GEMINI_API_KEY, AI_MODEL


genai.configure(api_key=GEMINI_API_KEY)

JARVIS_SYSTEM_PROMPT =""" You are JARVIS (Just A Rather Very Intelligent System),

   an intelligent AI desktop companion with an anime-style avatar.
   You are helpful, friendly, and slightly witty — like a knowledgeable
   friend who happens to know everything about computers and technology.
   
   You have three modes:
   - Chat Mode: have a helpful conversation
   - Guide Mode: walk the user through tasks step by step on their real screen
   - JARVIS Mode: take autonomous actions with the user's explicit permission
    Right now you are in Chat Mode.
   
   Always be concise, clear, and encouraging. If the user seems confused,
   ask a simple question to help them — don't overwhelm them.
   
   You are aware that you will later be able to see the user's screen,
   control their desktop, and connect to their phone — but only with permission.
"""

class ChatAgent:
    def __init__(self)->None:
        self.model= genai.GenerativeModel(
            model_name = AI_MODEL,
            system_instruction= JARVIS_SYSTEM_PROMPT
            
        )
        self.chat_session = self.model.start_chat(history=[])
        self.message_count=0
        print("🤖 JARVIS ChatAgent initialised. Ready to chat!")
    

    def chat(self,user_message:str)->str:
        if not user_message.strip():
            return "I didn't catch that — could you say it again"
        self.message_count +=1
        try:
            response= self.chat_session.send_message(user_message)
            return response.text.strip()
        except Exception as error:
             print(f"⚠️ Gemini error: {error}")
             return "Sorry, I'm having trouble thinking right now. Please try again!"


    def clear_history(self)-> None:
        """Reset the conversation — start fresh."""
        self.model.start_chat(history=[])
        self.message_count=0
        print("🔄 Conversation history cleared.")

    def get_message_count(self)->int:
        """How many messages have been sent this session?"""
        return self.message_count  

