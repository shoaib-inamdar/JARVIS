from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from agents.graph.graph import jarvis_graph
from agents.chat.agent import ChatAgent

from .models import ChatRequest, ChatResponse, HealthResponse

app = FastAPI(title="JARVIS Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
agent = ChatAgent()
initial_state = {
    "user_input":request.message,
    "messages":[],
    "intent":"chat",
    "plan":"",
    "safe_to_run":True,
    "final_reply":"",
}

result = jarvis_graph.invoke(initial_state)
reply = result["final_reply"]


@app.on_event("startup")
async def startup_event() -> None:
    print("JARVIS backend starting up...")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    print("JARVIS backend shutting down...")



@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Confirm JARVIS backend is alive. Used by the front-end to check connection."""
    return HealthResponse(
        status="ok",
        version="0.1.0",
        agent_ready=True,
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Receive a user message and return JARVIS's reply."""
    try:
        reply = agent.chat(request.message)
        return ChatResponse(
            reply=reply,
            message_count=agent.get_message_count(),
            status="ok",
        )
    except Exception:
        return ChatResponse(
            reply="Internal error. Please try again.",
            message_count=0,
            status="error",
        )


@app.delete("/chat/history")
def clear_history() -> dict:
    """Clear JARVIS's conversation memory — start fresh."""
    agent.clear_history()
    return {"message": "Conversation history cleared."}



@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket) -> None:
    """Real-time two-way connection for streaming responses (used from Phase 4 onward)."""
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            reply = agent.chat(data)
            await websocket.send_text(reply)
        except WebSocketDisconnect:
            break  



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
