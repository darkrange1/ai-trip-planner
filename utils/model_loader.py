import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_google_genai import ChatGoogleGenerativeAI
from logger.logging import get_logger

logger = get_logger(__name__)

class ConfigLoader:
    def __init__(self):
        logger.info(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["google"] = "google"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        logger.info("LLM loading...")
        logger.info(f"Loading model from provider: {self.model_provider}")
        
        if self.model_provider == "google":
            logger.info("Loading LLM from Google..............")
            google_api_key = os.getenv("GOOGLE_API_KEY", "").strip().strip('"').strip("'")
            if not google_api_key:
                logger.error("GOOGLE_API_KEY not found in environment variables")
                raise ValueError("GOOGLE_API_KEY not found")
                
            model_name = self.config["llm"]["google"]["model_name"]
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=google_api_key)
        
        return llm
    