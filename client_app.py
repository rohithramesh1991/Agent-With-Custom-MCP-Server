import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import gradio as gr

load_dotenv()
key = os.getenv("GROQ_API_KEY")
if key is None:
    raise ValueError("GROQ_API_KEY environment variable not set")
os.environ['GROQ_API_KEY'] = key


config_file = "configure_mcp.json"

client = MCPClient.from_config_file(config_file)
llm = ChatGroq(model="qwen-qwq-32b")
agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=15,
    memory_enabled=True,
)

async def gradio_chat(user_input, history):
    if user_input.strip().lower() == "clear":
        agent.clear_conversation_history()
        return "Conversation history cleared."
    if user_input.strip().lower() in ["exit", "quit"]:
        return "Session ended. Refresh to start again."
    try:
        response = await agent.run(user_input)
        return response
    except Exception as e:
        return f"Error: {e}"

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🤖 MCP Chat Assistant</h1>")
    chat = gr.ChatInterface(
        gradio_chat,
        theme="soft",
        chatbot=gr.Chatbot(height=500, type="messages"),
    )

if __name__ == "__main__":
    demo.queue().launch()
