import streamlit as st
import sqlite3
import hashlib
import os
from groclake.modellake import ModelLake
from groclake.vectorlake import VectorLake
import docx
import PyPDF2

# Initialize Groclake
os.environ['GROCLAKE_API_KEY'] = '013d407166ec4fa56eb1e1f8cbe183b9'
os.environ['GROCLAKE_ACCOUNT_ID'] = '3838e00de26b4f0c6e8e84d7ea89e566'
modellake = ModelLake()
vectorlake = VectorLake()

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'medical_text' not in st.session_state:
    st.session_state.medical_text = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def is_healthcare_question(query: str) -> bool:
    """Quick, naive check for health-related keywords."""
    keywords = [
        "health", "doctor", "symptom", "pain", "disease", "illness", 
        "medical", "treatment", "medication", "stomach", "vomit", "nausea"
    ]
    q_lower = query.lower()
    return any(kw in q_lower for kw in keywords)

def handle_query_and_response(query, mode, medical_text=None):
    """Handle query processing and response generation."""
    try:
        # Improved system prompt for interactive diagnosis
        system_content = """You are a skilled medical assistant conducting an interactive diagnosis session.
        Your goals are to:
        1. Ask specific, focused questions to understand the patient's condition better
        2. Build on previous responses to narrow down potential causes
        3. Guide the conversation towards a clear understanding of symptoms
        4. Provide clear, actionable insights while reminding to consult healthcare professionals
        5. Keep responses concise but informative
        """

        # Determine which response function to call
        if mode == "General Health Query":
            response = get_general_health_response(query, system_content)
        else:
            if not medical_text:
                st.error("Please upload a medical report first")
                return
            response = get_report_analysis_response(query, medical_text, system_content)
        
        # Store conversation
        st.session_state.conversation_history.extend([
            {"type": "question", "content": query},
            {"type": "answer", "content": response['answer']}
        ])
        
        return response['answer']

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT NOT NULL,
                  name TEXT NOT NULL)''')
    conn.commit()
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = init_db()
    c = conn.cursor()
    hashed_pw = hash_password(password)
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_pw))
    result = c.fetchone() is not None
    conn.close()
    return result

def register_user(username, password, name):
    conn = init_db()
    try:
        c = conn.cursor()
        hashed_pw = hash_password(password)
        c.execute('INSERT INTO users VALUES (?, ?, ?)', (username, hashed_pw, name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def process_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")
    return text

def get_general_health_response(query, system_content):
    conversation_messages = [
        {
            "role": "system",
            "content": """You are an empathetic medical assistant conducting an interactive diagnosis.
            Your approach should be:
            1. Start with a positive, professional tone (avoid starting with "I'm sorry")
            2. Ask ONE specific follow-up question at a time
            3. Structure your responses clearly:
               - Acknowledge the concern professionally
               - Ask a focused follow-up question
               - Explain why this information helps
               - If sufficient info, provide analysis
               - Add any relevant precautions
            4. Keep responses complete (never cut off mid-sentence)
            5. Maintain a constructive, solution-focused tone
            6. Include clear action items when appropriate
            
            Example format:
            "Thank you for sharing these symptoms. Let's work together to understand your situation better.
            [Brief acknowledgment of current symptoms]
            [One specific follow-up question]
            [Brief explanation of why this information helps]
            [If applicable: potential causes and next steps]"
            """
        }
    ]
    
    # Add conversation history
    for msg in st.session_state.conversation_history:
        conversation_messages.append({
            "role": "user" if msg["type"] == "question" else "assistant",
            "content": msg["content"]
        })
    
    conversation_messages.append({"role": "user", "content": query})
    return modellake.chat_complete({
        "groc_account_id": os.environ['GROCLAKE_ACCOUNT_ID'],
        "messages": conversation_messages
    })

def get_report_analysis_response(query, medical_text, system_content):
    conversation_messages = [
        {
            "role": "system",
            "content": system_content
        }
    ]
    
    # Add conversation history
    for msg in st.session_state.conversation_history:
        conversation_messages.append({
            "role": "user" if msg["type"] == "question" else "assistant",
            "content": msg["content"]
        })
    
    # Add current query with medical context
    conversation_messages.append({
        "role": "user",
        "content": f"Context: {medical_text}\nPrevious discussion summary: {summarize_conversation()}\nQuestion: {query}"
    })
    
    return modellake.chat_complete({
        "groc_account_id": os.environ['GROCLAKE_ACCOUNT_ID'],
        "messages": conversation_messages
    })

def summarize_conversation():
    if not st.session_state.conversation_history:
        return "No previous discussion"
    return " | ".join([f"Q: {msg['content']}" if msg['type'] == 'question' else f"A: {msg['content'][:100]}..."
                      for msg in st.session_state.conversation_history[-3:]])  # Last 3 exchanges

def create_chat_ui():
    """Create a modern chat UI with proper message bubbles"""
    st.markdown("""
        <style>
        /* Containers */
        .main-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            height: calc(100vh - 100px);
        }
        
        .chat-container {
            flex-grow: 1;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 80px;
        }
        
        /* Message bubbles */
        .message {
            display: flex;
            margin: 8px 0;
            animation: fadeIn 0.3s ease-in;
        }
        
        .message-content {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 12px;
            line-height: 1.4;
            white-space: pre-wrap;
        }
        
        /* User message */
        .user-message {
            justify-content: flex-end;
        }
        
        .user-message .message-content {
            background: var(--primary-color, #2b6cb0);
            color: white;
            border-bottom-right-radius: 4px;
            margin-left: auto;
        }
        
        /* Assistant message */
        .assistant-message {
            justify-content: flex-start;
        }
        
        .assistant-message .message-content {
            background: var(--chat-bubble-bg, #f0f2f5);
            color: var(--text-color, #1a1a1a);
            border-bottom-left-radius: 4px;
        }
        
        /* Input area */
        .input-area {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--background-color, white);
            padding: 16px 24px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            z-index: 100;
        }
        
        .input-container {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 10px;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .message-content {
                max-width: 85%;
            }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .assistant-message .message-content {
                background: #2d3748;
                color: #e2e8f0;
            }
            
            .input-area {
                background: #1a202c;
                border-top: 1px solid #2d3748;
            }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

def render_message(msg):
    """Render a single chat message"""
    if msg["type"] == "question":
        return f"""
        <div class="message user-message">
            <div class="message-content">
                {msg["content"]}
            </div>
        </div>
        """
    else:
        return f"""
        <div class="message assistant-message">
            <div class="message-content">
                {msg["content"]}
            </div>
        </div>
        """

# Main application flow
def main():
    st.set_page_config(page_title="Medical Assistant", layout="wide")

    # Display current step
    steps = ["Login/Register", "Choose Mode", "Ask Questions", "View Results"]
    st.progress((st.session_state.step - 1) / len(steps))
    st.write(f"Step {st.session_state.step}: {steps[st.session_state.step - 1]}")

    # Step 1: Authentication
    if not st.session_state.logged_in:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        with col2:
            st.subheader("Register")
            new_username = st.text_input("Username", key="reg_username")
            new_password = st.text_input("Password", type="password", key="reg_password")
            new_name = st.text_input("Full Name")
            if st.button("Register"):
                if register_user(new_username, new_password, new_name):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")

    # Step 2: Mode Selection
    elif st.session_state.step == 2:
        st.subheader("Choose Mode")
        mode = st.radio("Select mode:", ["General Health Query", "Medical Report Analysis"])
        if st.button("Continue"):
            st.session_state.mode = mode
            st.session_state.step = 3
            st.rerun()

    # Step 3: Query Interface
    elif st.session_state.step == 3:
        st.subheader("Medical Consultation")
        create_chat_ui()
        
        # Main container
        main_container = st.container()
        
        with main_container:
            # File upload area
            if st.session_state.mode == "Medical Report Analysis":
                if not st.session_state.medical_text:
                    uploaded_file = st.file_uploader("Upload Medical Report", type=['pdf', 'docx'])
                    if uploaded_file:
                        try:
                            text = process_uploaded_file(uploaded_file)
                            st.session_state.medical_text = text
                            st.success("Report processed successfully!")
                        except Exception as e:
                            st.error(f"Error processing file: {str(e)}")
            
            # Chat messages area
            st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
            for msg in st.session_state.conversation_history:
                if msg["type"] == "question":
                    st.markdown(f'<div class="user-message">🤔 You: {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message">👩‍⚕️ Assistant: {msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Fixed input area at bottom
        input_container = st.container()
        with input_container:
            st.markdown('<div class="input-area">', unsafe_allow_html=True)
            cols = st.columns([6, 1])
            with cols[0]:
                query = st.text_input(
                    "",
                    placeholder="Ask about your medical concerns...",
                    key=f"chat_input_{len(st.session_state.conversation_history)}",
                    label_visibility="collapsed"
                )
            with cols[1]:
                send_button = st.button("💬", use_container_width=True)
            st.markdown(f'<p style="color: gray; font-size: 12px;">Mode: {st.session_state.mode}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle query submission
        if (send_button or query.endswith('\n')) and query:
            response = handle_query_and_response(
                query,
                st.session_state.mode,
                st.session_state.medical_text if st.session_state.mode == "Medical Report Analysis" else None
            )
            if response:
                st.rerun()

    # Logout button in sidebar
    if st.session_state.logged_in:
        with st.sidebar:
            st.write(f"Logged in as: {st.session_state.username}")
            if st.button("Logout"):
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()

