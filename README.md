# 🏥 Medical Assistant Chatbot

This is a Streamlit-based interactive medical assistant chatbot designed to assist users with medical queries and analyze medical reports. The chatbot leverages AI-driven responses to provide useful insights while encouraging users to seek professional medical advice when necessary.

---

## ✨ Features
- **🔐 User Authentication**: Secure login and registration system with password hashing.
- **💬 Interactive Medical Consultation**: Engages users in a Q&A format for medical guidance.
- **⚙️ Two Modes of Operation**:
  - **🩺 General Health Query**: Provides AI-generated responses based on medical knowledge.
  - **📄 Medical Report Analysis**: Processes and extracts key insights from uploaded medical reports (PDF/DOCX).
- **📜 Conversation History**: Maintains a record of past interactions for reference.
- **🤖 AI-Powered Responses**: Utilizes **Groclake ModelLake** for generating contextual and accurate medical responses.
- **🔒 Secure Data Handling**: Implements SHA-256 password hashing and stores user data in a local SQLite database.

---

## 🚀 Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repository/medical-assistant-chatbot.git
cd medical-assistant-chatbot
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the project root directory and add the following:
```ini
GROCLAKE_API_KEY=your-api-key-here
GROCLAKE_ACCOUNT_ID=your-account-id-here
```

### 5️⃣ Run the Application
```sh
streamlit run app.py
```

---

## 📂 Project Structure
```
medical-assistant-chatbot/
│── app.py               # Main Streamlit app
│── requirements.txt     # Required dependencies
│── .env                 # API keys (not included in version control)
└── README.md            # Documentation
```

---

## 🛠️ How It Works
1️⃣ **User Login/Registration**: New users can register, while existing users can log in securely.
2️⃣ **Mode Selection**: Users choose between "General Health Query" or "Medical Report Analysis."
3️⃣ **Medical Consultation**:
   - In **General Health Query**, users ask medical-related questions and receive AI-generated responses.
   - In **Medical Report Analysis**, users upload their medical reports, which are processed to extract insights.
4️⃣ **Ongoing Interaction**: The chatbot maintains a history of conversations for better context.

---

## 🔐 Environment & Security Notes
- Ensure you do **not** share your `.env` file or commit it to version control.
- Passwords are securely stored using SHA-256 hashing.
- The chatbot is designed for **informational purposes only** and should **not** replace professional medical advice.

---

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Feel free to submit issues or pull requests to enhance functionality.

## 📧 Contact
For any inquiries, reach out to `your.email@example.com`.

---

🚀 **Happy Coding & Stay Healthy!** 🩺

