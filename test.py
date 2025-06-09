import os
import json
import re
from typing import List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
import gradio as gr

# Load environment variables
load_dotenv()
key = os.getenv("GROQ_API_KEY")
if key is None:
    raise ValueError("GROQ_API_KEY environment variable not set")
os.environ['GROQ_API_KEY'] = key

# Load MCP servers config and create system prompt
config_file = "configure_mcp.json"

system_message_content = f"""
{config_file}
Always use available MCP servers to fetch real data for user requests. Never guess or fabricate answers—return only actual results from the servers.
If data or tables are missing, state this honestly. Keep responses brief, relevant, and based solely on MCP server outputs. 
If unsure which server applies, ask the user or use your best judgment. Your role is to call MCP servers and deliver accurate answers.
"""


# LLM and agent setup
llm = ChatGroq(model="qwen-qwq-32b")
client = MCPClient.from_config_file(config_file)
agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=15,
    memory_enabled=True,
)

# Function to clean up LLM responses
def remove_think_tag(response_text: str) -> str:
    cleaned_response = re.sub(r'<think>.*?</think>\n?', '', response_text, flags=re.DOTALL)
    return cleaned_response.strip()

# Chat handler for Gradio
async def gradio_chat(user_input, history):
    if user_input.strip().lower() == "clear":
        agent.clear_conversation_history()
        return "Conversation history cleared."
    if user_input.strip().lower() in ["exit", "quit"]:
        return "Session ended. Refresh to start again."

    # Build LLM messages with full history and system prompt
    # messages = [SystemMessage(content=system_message_content)]
    messages: List[BaseMessage] = [SystemMessage(content=system_message_content)]
    for msg in history:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg.get("role") == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=user_input))

    try:
        response_obj = await llm.ainvoke(messages)
        # Extract and clean string response
        result = response_obj.content if hasattr(response_obj, "content") else str(response_obj)
        result_str = str(result)
        response = remove_think_tag(result_str)
        return response
    except Exception as e:
        print(f"Exception during LLM invocation: {e}")
        return f"Error: {e}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🤖 MCP Chat Assistant</h1>")
    chat = gr.ChatInterface(
        gradio_chat,
        chatbot=gr.Chatbot(height=500, type="messages"),
        theme="soft"
    )

if __name__ == "__main__":
    demo.queue().launch()
