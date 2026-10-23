from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from agents.chat.agent import ChatAgent
from agents.chat.graph.graph import jarvis_graph
from agents.coding.graph import coding_graph
from apps.desktop.backend.models import CodingRequest

from .models import ChatRequest, ChatResponse, HealthResponse

app = FastAPI(title="JARVIS Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
agent = ChatAgent()


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
    """Receive a user message and return JARVIS's reply via the LangGraph pipeline."""
    try:
        state = jarvis_graph.invoke(
            {
                "user_input": request.message,
                "messages": [],
                "intent": "chat",
                "plan": "",
                "safe_to_run": True,
                "final_reply": "",
            }
        )
        reply = state["final_reply"]
        return ChatResponse(
            reply=reply,
            message_count=len(state.get("messages", [])),
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


@app.post("/coding")
async def coding_endpoint(request: CodingRequest) -> dict:
    initial_state = {
        "user_request": request.message,
        "current_mode": "coding",
        "project_root": request.project_root or ".",
        "relevant_files": [],
        "open_file": request.open_file or "",
        "error_context": request.error_context or "",
        "plan_steps": [],
        "current_step": 0,
        "plan_approved": False,
        "proposed_patch": "",
        "patch_approved": False,
        "action_history": [],
        "test_results": "",
        "lint_results": "",
        "verified": False,
        "pending_permission": "",
        "safety_flags": [],
        "blocked": False,
        "final_reply": "",
        "avatar_mood": "thinking",
    }

    result = coding_graph.invoke(initial_state)
    return {
        "reply": result["final_reply"],
        "avatar_mood": result["avatar_mood"],
        "plan": result["plan_steps"],
        "patch": result["proposed_patch"],
        "verified": result["verified"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
