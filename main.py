from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from logger.logging import get_logger
from exception.exceptions import TravelPlannerException

load_dotenv()

logger = get_logger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error. Please check logs for details."}
    )

@app.exception_handler(TravelPlannerException)
async def travel_planner_exception_handler(request: Request, exc: TravelPlannerException):
    logger.error(f"Travel Planner exception occurred: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={"error": exc.message}
    )

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        logger.info(f"Received query: {query.question}")
        print(query)
        # Using Google as default provider
        graph = GraphBuilder(model_provider="google")
        react_app = graph()
        #react_app = graph.build_graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        logger.info(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        logger.info("Query processed successfully")
        return {"answer": final_output}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})