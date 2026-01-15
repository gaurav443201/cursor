# 🗳️ VIT-ChainVote: Secure Blockchain Voting System

VIT-ChainVote is a state-of-the-art, cryptographically secured voting platform designed for institutional elections. Built on a private blockchain architecture with Google Gemini AI integration, it ensures that every vote is immutable, transparent, and verified.

![VIT-ChainVote](https://img.shields.io/badge/Blockchain-Secured-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.0-red?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Gemini-purple?style=for-the-badge)

## 🌟 Features

### 🔐 Security
- **Blockchain Technology**: Every vote is recorded on an immutable blockchain
- **Proof-of-Work Mining**: Difficulty-4 PoW consensus ensures block integrity
- **Cryptographic Hashing**: SHA-256 hashing for voter privacy and chain validation
- **One Vote Per Person**: Identity hashing prevents double voting
- **Real-Time OTP**: 6-digit codes via SMTP for secure authentication

### 🤖 AI Integration
- **Manifesto Generation**: Gemini AI creates professional 2-sentence manifestos
- **Election Audit**: AI-powered post-election analysis and insights
- **Candidate Verification**: Automated name validation

### 🎨 Modern UI
- **Dark Theme**: Stunning glassmorphism design with vibrant gradients
- **Responsive**: Works seamlessly on desktop and mobile
- **Real-Time Updates**: Live election status monitoring
- **Smooth Animations**: Premium micro-interactions

## 👥 Administrative Governance (The Shadows)

The system is governed by two primary administrators:
- **Shadow 1:** `shadow70956@gmail.com`
- **Shadow 2:** `navgharegaurav80@gmail.com`

**Admin Privileges:**
- Register and remove candidates
- Start/Stop elections
- Reset blockchain to genesis
- Access AI audit reports

## 📜 Election Rules

1. **Identity Integrity**: Only verified VIT emails (`name.prn@vit.edu`) can vote
2. **One Person, One Vote**: Blockchain prevents duplicate voting
3. **Departmental Enclosure**: Voters only see candidates from their department
4. **Immutable Records**: Mined blocks cannot be altered
5. **Real-Time Verification**: PoW algorithm secures every transaction

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API Key
- Gmail account for SMTP (or use provided credentials)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd "c:\PROGRAMMING\CWH\New folder"
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the root directory:
```env
API_KEY=your_gemini_api_key_here
EMAIL_USER=otakuaniverseofficial@gmail.com
EMAIL_PASS=adxpxirxgwnrcjlo
FLASK_ENV=production
PORT=5000
```

4. **Start the backend server**
```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

5. **Open the frontend**

Open `frontend/index.html` in your web browser, or use a local server:
```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

## 📁 Project Structure

```
VIT-ChainVote/
├── backend/
│   ├── app.py              # Flask REST API server
│   ├── blockchain.py       # Blockchain core (Block, Chain)
│   ├── models.py           # Data models (Candidate, Voter, Election)
│   ├── otp_service.py      # OTP generation and SMTP
│   ├── ai_service.py       # Gemini AI integration
│   └── utils.py            # Utility functions
├── frontend/
│   ├── index.html          # Landing page
│   ├── admin.html          # Shadow dashboard
│   ├── voter.html          # Voting interface
│   ├── results.html        # Results page
│   ├── css/
│   │   └── styles.css      # Modern dark theme
│   └── js/
│       └── app.js          # Frontend logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔄 Workflow

### Phase 1: Preparation (Waiting Room)
1. Admins log in with Shadow credentials
2. Register candidates (AI generates manifestos)
3. Voters logging in are held in waiting room
4. Admin clicks "Start Election"

### Phase 2: Live Voting (The Booth)
1. Voters enter VIT email and department
2. Receive 6-digit OTP via email
3. Verify OTP and access voting booth
4. Vote for candidate (block is mined with PoW)
5. Receive transaction hash (TXID) as proof

### Phase 3: Audit & Results
1. Admin clicks "Stop Election"
2. Results calculated from blockchain
3. AI generates audit report
4. Public results page shows winners

## 🛠️ API Endpoints

### Admin Routes
- `POST /api/admin/login` - Shadow authentication
- `POST /api/admin/candidate/add` - Register candidate
- `DELETE /api/admin/candidate/remove` - Remove candidate
- `GET /api/admin/candidates` - Get all candidates
- `POST /api/admin/election/start` - Start election
- `POST /api/admin/election/stop` - Stop election
- `POST /api/admin/election/reset` - Reset blockchain
- `GET /api/admin/audit` - Get AI audit

### Voter Routes
- `POST /api/voter/login` - Send OTP
- `POST /api/voter/verify-otp` - Verify OTP
- `GET /api/voter/candidates` - Get department candidates
- `POST /api/voter/vote` - Submit vote
- `GET /api/voter/status` - Check if voted

### Public Routes
- `GET /api/election/state` - Current election state
- `GET /api/results` - Election results
- `GET /api/blockchain` - Full blockchain data

## 🎯 Departments

- **CSE** - Computer Science & Engineering
- **IT** - Information Technology
- **ENTC** - Electronics & Telecommunication
- **MECH** - Mechanical Engineering

## 🔒 Security Considerations

- Admin emails are hardcoded (Shadow system)
- Voter emails are hashed with SHA-256 (privacy)
- OTP expires after 5 minutes
- Blockchain validates with PoW (difficulty 4)
- CORS enabled for frontend communication

## 🚢 Deployment (Render)

1. Create a new Web Service on Render
2. Connect your repository
3. Set environment variables:
   - `API_KEY`
   - `EMAIL_USER`
   - `EMAIL_PASS`
   - `FLASK_ENV=production`
4. Build command: `pip install -r requirements.txt`
5. Start command: `python backend/app.py`

## 📊 Technology Stack

**Backend:**
- Flask 3.0 (REST API)
- Python hashlib (SHA-256)
- Google Gemini AI (Manifesto generation)
- SMTP (OTP delivery)

**Frontend:**
- HTML5 / CSS3 / JavaScript
- Glassmorphism design
- Google Fonts (Inter, Orbitron)
- Responsive grid layouts

**Blockchain:**
- Custom implementation
- Proof-of-Work consensus
- SHA-256 hashing
- Difficulty: 4

## 🤝 Contributing

This is a secure voting system. Any modifications should be reviewed by the Shadow administrators.

## 📄 License

VIT-ChainVote © 2026 - Secure Digital Asset

## ⚠️ Disclaimer

VIT-ChainVote is a secure digital asset. Any attempt to modify the ledger without administrative authorization will be flagged by the internal hash-integrity monitor.

---

**Powered by Blockchain Technology | Secured by Proof-of-Work | AI-Enhanced by Google Gemini**
