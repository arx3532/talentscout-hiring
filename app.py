# app.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from fastapi import FastAPI

# Load environment variables
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    raise ValueError("NVIDIA_API_KEY not set in environment variables.")

# Initialize OpenAI client for NVIDIA NIM
client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

# System prompt for the chatbot
system_prompt = (
    "You are a Hiring Assistant chatbot for TalentScout, a tech recruitment agency. Your task is to:\n"
    "1. Start by greeting the candidate and explaining your purpose, then ask for their full name.\n"
    "2. Collect one piece of information at a time: full name, email, phone number, years of experience, desired position, current location.\n"
    "3. After collecting all info, ask for their tech stack (e.g., languages, frameworks, tools).\n"
    "4. Once the tech stack is provided, generate and ask one technical question at a time (3 total), waiting for a response before asking the next.\n"
    "5. After all questions, thank them and explain next steps.\n"
    "6. If input is unclear, politely ask for clarification.\n"
    "7. End the conversation if the candidate says 'exit' or 'quit'.\n"
    "Ask only one question at a time and wait for the candidate's response before proceeding."
)

def chat_with_nim(user_input, conversation_state):
    """Generate a response from the LLM using the conversation history."""
    if user_input:
        conversation_state["history"].append({"role": "user", "content": user_input})
    
    try:
        completion = client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=conversation_state["history"],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        response = completion.choices[0].message.content
        conversation_state["history"].append({"role": "assistant", "content": response})
        return response, conversation_state
    except Exception as e:
        return f"Sorry, an error occurred: {str(e)}. Please try again.", conversation_state

def update_conversation_state(conversation_state, user_input, chatbot_response):
    """Update the conversation state based on the current step and input."""
    if user_input.lower() in ["exit", "quit"]:
        conversation_state["step"] = "done"
        return conversation_state

    if conversation_state["step"] == "start":
        conversation_state["candidate_info"]["full_name"] = user_input
        conversation_state["step"] = "email"
    elif conversation_state["step"] == "email":
        conversation_state["candidate_info"]["email"] = user_input
        conversation_state["step"] = "phone"
    elif conversation_state["step"] == "phone":
        conversation_state["candidate_info"]["phone"] = user_input
        conversation_state["step"] = "experience"
    elif conversation_state["step"] == "experience":
        conversation_state["candidate_info"]["experience"] = user_input
        conversation_state["step"] = "position"
    elif conversation_state["step"] == "position":
        conversation_state["candidate_info"]["position"] = user_input
        conversation_state["step"] = "location"
    elif conversation_state["step"] == "location":
        conversation_state["candidate_info"]["location"] = user_input
        conversation_state["step"] = "tech_stack"
    elif conversation_state["step"] == "tech_stack":
        conversation_state["candidate_info"]["tech_stack"] = user_input
        conversation_state["step"] = "ask_questions"
        conversation_state["questions_asked"] = 0
    elif conversation_state["step"] == "ask_questions":
        conversation_state["tech_responses"].append(user_input)
        conversation_state["questions_asked"] += 1
        if conversation_state["questions_asked"] >= 3:
            conversation_state["step"] = "done"
    return conversation_state

def chatbot_interface(user_input, conversation_state):
    """Handle the chatbot interaction and update the UI."""
    if not conversation_state["history"]:
        conversation_state["history"] = [{"role": "system", "content": system_prompt}]
        conversation_state["step"] = "start"
        conversation_state["candidate_info"] = {}
        conversation_state["questions_asked"] = 0
        conversation_state["tech_responses"] = []
        chatbot_response, updated_state = chat_with_nim("", conversation_state)
        return [{"role": "assistant", "content": chatbot_response}], updated_state, ""

    chatbot_response, updated_state = chat_with_nim(user_input, conversation_state)
    updated_state = update_conversation_state(updated_state, user_input, chatbot_response)

    convo_history = [{"role": msg["role"], "content": msg["content"]} 
                     for msg in updated_state["history"] if msg["role"] != "system"]

    if updated_state["step"] == "done" and not any("Thank you" in msg["content"] for msg in updated_state["history"]):
        closing_msg = "Thank you for your responses! A TalentScout representative will follow up soon."
        updated_state["history"].append({"role": "assistant", "content": closing_msg})
        convo_history.append({"role": "assistant", "content": closing_msg})

    return convo_history, updated_state, ""

# Custom CSS (unchanged)
custom_css = """
body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    margin: 0;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    color: #e6e6e6;
}
.chat-card {
    background: #121212;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
    width: 100%;
    max-width: 600px;
    padding: 20px;
    overflow: hidden;
}
.header {
    text-align: center;
    padding-bottom: 15px;
    border-bottom: 2px solid #9c27b0;
}
.header h1 {
    font-size: 28px;
    color: #bb86fc;
    margin: 0;
}
.header p {
    font-size: 14px;
    color: #9e9e9e;
    margin: 5px 0 0;
}
.chatbot-container {
    height: 400px;
    overflow-y: auto;
    padding: 10px 0;
}
.gr-chatbot .message {
    padding: 10px 15px;
    margin: 8px 10px;
    border-radius: 15px;
    font-size: 15px;
}
.gr-chatbot .message.user {
    background: #9c27b0;
    color: white;
    margin-left: 20%;
}
.gr-chatbot .message.bot {
    background: #1e1e1e;
    color: #e6e6e6;
    margin-right: 20%;
    border: 1px solid #3a3a3a;
}
.input-area {
    margin-top: 15px;
}
.input-textbox {
    border: 2px solid #9c27b0;
    border-radius: 25px;
    padding: 10px 15px;
    font-size: 14px;
    width: 100%;
    background-color: #1e1e1e;
    color: #e6e6e6;
}
.input-textbox::placeholder {
    color: #9e9e9e;
}
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #1e1e1e;
}
::-webkit-scrollbar-thumb {
    background: #9c27b0;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #bb86fc;
}
"""

# FastAPI setup
app = FastAPI()

# Gradio interface
with gr.Blocks(css=custom_css) as demo:
    with gr.Column(elem_classes="chat-card"):
        gr.Markdown(
            """
            <div class="header">
                <h1>TalentScout Chat</h1>
                <p>Hey there! I'll ask you a few questions to get started. Just answer one at a time and press Enter, or say 'exit' to wrap up!</p>
            </div>
            """
        )
        chatbot = gr.Chatbot(type="messages", elem_classes="chatbot-container")
        with gr.Row(elem_classes="input-area"):
            user_input = gr.Textbox(placeholder="Type here and press Enter...", show_label=False, elem_classes="input-textbox")
    
    conversation_state = gr.State({"history": [], "step": "", "candidate_info": {}, 
                                  "questions_asked": 0, "tech_responses": []})
    
    demo.load(fn=chatbot_interface, inputs=[gr.State(value=""), conversation_state], 
              outputs=[chatbot, conversation_state, user_input])
    user_input.submit(fn=chatbot_interface, inputs=[user_input, conversation_state], 
                      outputs=[chatbot, conversation_state, user_input])

# Mount Gradio app onto FastAPI
app = gr.mount_gradio_app(app, demo, path="/")