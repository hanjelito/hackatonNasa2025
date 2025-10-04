from google import genai
from app.config.settings import settings


class VertexAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VertexAIClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.api_key = settings.API_KEY_VERTEXAI
        self.client = genai.Client(api_key=self.api_key, vertexai=True)
        self._initialized = True
