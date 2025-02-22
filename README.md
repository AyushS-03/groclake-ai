# Medical Assistant AI

A comprehensive medical assistance platform powered by AI that offers two main functionalities:
1. General Health Query - Interactive health consultation
2. Medical Report Analysis - AI-powered medical report interpretation

## Features

- **General Health Query**
  - Symptom analysis
  - Dynamic questionnaire generation
  - Structured medical recommendations
  - Conversation history tracking

- **Medical Report Analysis**
  - PDF and DOCX report upload
  - Key findings extraction
  - Medical terminology explanation
  - Follow-up question handling

- **Other Features**
  - User authentication
  - Secure data handling
  - Responsive design
  - Cross-platform compatibility

## Tech Stack

- **Frontend**
  - React.js
  - Styled Components
  - Axios for API calls
  - React Router

- **Backend**
  - Flask (Python)
  - Groclake AI API
  - SQLite for user management
  - PyPDF2 & python-docx for file processing

## Project Structure
### [README.md](file:///d%3A/ma/README.md)

```markdown
# Medical Assistant AI

A comprehensive medical assistance platform powered by AI that offers two main functionalities:
1. General Health Query - Interactive health consultation
2. Medical Report Analysis - AI-powered medical report interpretation

## Features

- **General Health Query**
  - Symptom analysis
  - Dynamic questionnaire generation
  - Structured medical recommendations
  - Conversation history tracking

- **Medical Report Analysis**
  - PDF and DOCX report upload
  - Key findings extraction
  - Medical terminology explanation
  - Follow-up question handling

- **Other Features**
  - User authentication
  - Secure data handling
  - Responsive design
  - Cross-platform compatibility

## Tech Stack

- **Frontend**
  - React.js
  - Styled Components
  - Axios for API calls
  - React Router

- **Backend**
  - Flask (Python)
  - Groclake AI API
  - SQLite for user management
  - PyPDF2 & python-docx for file processing

## Project Structure

```
ma/
├── backend/
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── temp_uploads/        # Temporary file storage
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── AuthPage.js
│   │   │   ├── GeneralQueryPage.js
│   │   │   ├── LandingPage.js
│   │   │   ├── ModeSelectionPage.js
│   │   │   └── ReportAnalysisPage.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## Setup Instructions

1. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

3. **Environment Variables**
- Create `.env` in frontend directory:
```
REACT_APP_API_URL=http://localhost:5000
```

4. **Database**
- SQLite database will be automatically created on first run
- Default location: `backend/users.db`

## API Endpoints

- `POST /login` - User authentication
- `POST /register` - New user registration
- `POST /query` - Handle both general queries and report analysis
- `POST /process_file` - File upload and processing

## Usage

1. Start with user registration/login
2. Choose between General Query or Report Analysis
3. For General Query:
   - Enter your health-related question
   - Fill out the dynamic questionnaire
   - Review the structured response
4. For Report Analysis:
   - Upload medical report (PDF/DOCX)
   - Review the AI analysis
   - Ask follow-up questions

## Security Notes

- Password hashing implemented
- File upload size limits enforced
- Temporary file cleanup
- CORS configured for development

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Contact

For support or queries, please open an issue in the repository.
```