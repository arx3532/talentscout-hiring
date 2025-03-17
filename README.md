# TalentScout Hiring

TalentScout Hiring is an AI-powered recruitment chatbot designed to streamline the initial candidate screening process. The application uses NVIDIA NIM API with Meta's llama-3.1-405b-instruct to create an interactive conversation flow that collects candidate information and conducts preliminary technical assessments.

## 🌟 Live Demo
[TalentScout Hiring App](https://talentscout-hiring.onrender.com/)

## 🚀 Features

- **Interactive Chat Interface**: Stylish black and purple themed chatbot with a user-friendly interface
- **Structured Candidate Screening**: Step-by-step information collection process
- **Technical Assessment**: Automated technical questions based on the candidate's tech stack
- **Conversation Management**: Tracks conversation state and candidate information
- **Responsive Design**: Works on both desktop and mobile devices

## 📋 Requirements

- Python 3.10+
- Gradio
- OpenAI Python client library (for NVIDIA NIM API integration)
- python-dotenv
- NVIDIA NIM API key

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/arx3532/talentscout-hiring.git
cd talentscout-hiring
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your NVIDIA API key:
```
NVIDIA_API_KEY=your_nvidia_api_key_here
```

## 🚀 Usage

1. Start the application:
```bash
python hiring_assistant.py
```

2. Open your browser and navigate to the port configured in your environment.

3. The chatbot will automatically start the conversation and guide candidates through the screening process.

## 🤖 Chatbot Workflow

The chatbot follows a structured conversation flow:

1. **Introduction**: Greets the candidate and explains the purpose of the chat
2. **Information Collection**: Collects one piece of information at a time:
   - Full name
   - Email address
   - Phone number
   - Years of experience
   - Desired position
   - Current location
   - Tech stack (programming languages, frameworks, tools)
3. **Technical Assessment**: Asks 3-5 technical questions based on the candidate's tech stack
4. **Conclusion**: Thanks the candidate and explains the next steps in the recruitment process

## 💻 Technical Implementation

- **NVIDIA NIM API**: Uses Meta's llama-3.1-405b-instruct model through NVIDIA's API for natural language processing
- **Gradio Framework**: Provides the interactive chat interface with custom CSS styling
- **Conversation State Management**: Tracks conversation progress and candidate information throughout the chat
- **Custom CSS**: Features a modern black and purple theme with responsive design elements

## 🔒 Security and Privacy

- The application uses environment variables for API key management
- Candidate information is stored in memory only for the duration of the session
- No persistent storage of candidate data is implemented in this version

## 🚀 Deployment

The application is configured to run on Render with automatic port detection:

```python
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  
    demo.launch(server_name="0.0.0.0", server_port=port)
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NVIDIA for providing the NIM API
- Meta for the llama-3.1-405b-instruct
- Gradio for the interactive UI framework
