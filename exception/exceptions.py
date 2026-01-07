class TravelPlannerException(Exception):
    """Base exception for the Travel Planner application"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class APIConnectionError(TravelPlannerException):
    """Raised when external API connection fails"""
    pass

class ToolExecutionError(TravelPlannerException):
    """Raised when a tool fails to execute"""
    pass

class LLMGenerationError(TravelPlannerException):
    """Raised when LLM fails to generate a response"""
    pass
