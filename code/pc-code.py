from dotenv import load_dotenv
import os

load_dotenv('private.env')
api_key = os.getenv("API_KEY")