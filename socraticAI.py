# importing important modules
import streamlit as st
import google.generativeai as genai
from typing import List, Dict
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Loaded from .env! 

class SocraticChatbot:
    def __init__(self):
        """Initialize the Socratic chatbot with Gemini API."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        
        # Socratic prompting template
        self.system_prompt = """
        You are a Socratic teacher who helps students think deeply through topics.
        Follow these principles:
        1. Don't be rude, behave nicely
        2. if the user greet, greet them nicely/professionally
        3. Ask open-ended questions that promote critical thinking
        4. Guide through gentle questioning rather than direct answers
        5. Help students discover answers themselves through reflection
        6. Acknowledge and build upon student responses
        7. Challenge assumptions respectfully
        8. Maintain focus on the core topic while exploring related ideas
        9. If they answer correctly, Congratulate them
        10. Don't end the conversation until a user does so

        Always respond in this format:
        1. Brief reflection on the student's last response 
        2. or 1-2 probing questions to deepen understanding, if necessary
        3. with Gentle guidance or context if needed
        """
        
    def generate_response(self, user_input: str) -> str:
        """Generate a Socratic response to user input."""
        try:
            full_prompt = (
                f"{self.system_prompt}\n\n"
                f"Current topic: {user_input}\n"
                "Generate a Socratic response:"
            )
            
            response = self.chat.send_message(full_prompt)
            return response.text
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

def initialize_session_state():
    """Initialize session state variables."""
    if 'conversations' not in st.session_state:
        st.session_state.conversations = {}
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0
    if 'current_conversation_id' not in st.session_state:
        create_new_conversation()

def get_current_conversation():
    """Get the current conversation data."""
    return st.session_state.conversations[st.session_state.current_conversation_id]

def create_new_conversation():
    """Create a new conversation."""
    st.session_state.conversation_count += 1
    new_conversation_id = f"conversation_{st.session_state.conversation_count}"
    st.session_state.current_conversation_id = new_conversation_id
    st.session_state.conversations[new_conversation_id] = {
        'messages': [],
        'chatbot': SocraticChatbot()
    }
    st.rerun()

def switch_conversation(conversation_id):
    """Switch to a different conversation."""
    st.session_state.current_conversation_id = conversation_id
    st.rerun()

def get_conversation_title(messages):
    """Get the title for a conversation based on first message."""
    if not messages:
        return "New Conversation"
    first_message = messages[0]['content']
    # Truncate long messages
    return (first_message[:30] + "...") if len(first_message) > 30 else first_message

def main():
    st.set_page_config(
        page_title="Socratic AI Teacher",
        page_icon="🤔",
        layout="wide"
    )
    
    st.title("🤔 Socratic AI Teacher")
    st.markdown("""
    Welcome to your AI-powered Socratic teacher! Share your thoughts or questions, 
    and I'll help you explore topics deeply through thoughtful discussion.
    """)
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar with conversation management and information
    with st.sidebar:
        st.header("Conversations")
        
        # New conversation button
        if st.button("Start New Conversation", key="new_conv"):
            create_new_conversation()
        
        st.markdown("---")
        
        # Previous conversations
        if len(st.session_state.conversations) > 1:
            st.subheader("Previous Conversations")
            
            for conv_id, conv_data in st.session_state.conversations.items():
                # Skip if this is a new conversation with no messages
                if not conv_data['messages']:
                    continue
                    
                # Get conversation title from first message
                title = get_conversation_title(conv_data['messages'])
                
                # Highlight current conversation
                is_current = conv_id == st.session_state.current_conversation_id
                button_label = f"{'🔵 ' if is_current else ''}  {title}"
                
                if st.button(button_label, key=f"conv_{conv_id}", 
                            disabled=is_current,
                            use_container_width=True):
                    switch_conversation(conv_id)
        
        st.markdown("---")
        # About section
        st.header("About this AI Tutor")
        st.markdown("""
        ### How it works
        1. Share any topic or question you'd like to explore
        2. The AI will engage you in Socratic dialogue
        3. Through questions and reflection, discover deeper insights
        
        ### Benefits
        - Develop critical thinking
        - Explore ideas deeply
        - Challenge assumptions
        - Learn through self-discovery
        
        ### Tips for best results
        - Be specific in your responses
        - Explain your reasoning
        - Ask questions when unclear
        - Take time to reflect
        """)
    
    # Main chat interface
    chat_container = st.container()
    
    # Display current conversation
    current_conversation = get_current_conversation()
    
    # Display chat messages
    with chat_container:
        for message in current_conversation['messages']:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Share your thoughts or ask a question...")
    
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        current_conversation['messages'].append({"role": "user", "content": user_input})
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = current_conversation['chatbot'].generate_response(user_input)
                st.write(response)
        current_conversation['messages'].append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
