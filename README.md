Socratic AI Chatbot
Overview
The Socratic AI Chatbot is an interactive AI-powered chatbot that engages users in Socratic dialogue. By using the power of Google’s Gemini API, this chatbot guides users to think deeply about various topics through open-ended, probing questions, promoting critical thinking and self-discovery.

Whether you're exploring a new concept or simply want to engage in thoughtful conversation, the Socratic AI Chatbot helps you uncover deeper insights by asking the right questions.

Features
Engage in a Socratic-style dialogue to explore topics deeply.
Provides gentle guidance to help users discover answers themselves.
Built using Streamlit for an easy-to-use web interface.
Utilizes Google Gemini AI for generating conversational responses.
Requirements
Before running the project, make sure you have the following installed:

Python 3.x
Streamlit
google-generativeai Python package

Installation
Clone this repository:

bash
Copy code
git clone https://github.com/riya-Xx/SocraticAI-Tutor.git
Navigate to the project folder:

bash
Copy code
cd SocraticAI-Tutor
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Add your Gemini API key in a .env file (make sure the .env file is not shared publicly):

bash
Copy code
GEMINI_API_KEY=your_api_key_here
Usage
Run the chatbot locally:

bash
Copy code
streamlit run socraticAI.py
Open your browser and navigate to http://localhost:8501 to interact with the chatbot.

Contributing
Contributions are welcome! If you find any bugs or have feature suggestions, feel free to open an issue or submit a pull request.

License
This project is open source and available under the MIT License.
