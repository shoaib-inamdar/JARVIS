from agents.chat.agent import ChatAgent
from rich.console import Console
from rich.panel import Panel,text
from rich.text import Text
console = Console()

def main()->None:
    console.print(Panel(
        Text(
            "JARVIS V0.1.0- Chat Mode\n\n"
            "Type 'exit' to quit |Type 'clear' to reset coversation" 

        )
    ))
    agent = ChatAgent()
    console.print("JARVIS is ready. Say something!")
    while True:
        user_input =input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            console.print("JARVIS: Goodbye! Shutting down... 👋")
            break
        if user_input.lower()== "clear":
            agent.clear_history()
            print("JARVIS: Memory cleared! Fresh start.")
            continue
        reply = agent.chat(user_input)
        print( f"JARVIS: {reply}")






if __name__ == "__main__":
    main()
