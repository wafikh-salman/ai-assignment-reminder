# 🤖 AI Assignment Reminder

<div align="center">

### Turn assignment reminders into an automated AI workflow.

A full-stack application that identifies students who have not submitted an assignment, generates a professional reminder with an LLM, validates the generated tool call on the backend, and sends the email through Resend.

<br/>

<a href="https://github.com/wafikh-salman/ai-assignment-reminder">
  <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repository"/>
</a>
<a href="#-tech-stack">
  <img src="https://img.shields.io/badge/Stack-React%20%2B%20Django%20%2B%20AI-00C896?style=for-the-badge" alt="Tech Stack"/>
</a>

</div>

---

## ✨ What is this?

**AI Assignment Reminder** is an experimental full-stack AI application built around a simple problem:

> Students miss assignment deadlines, and manually writing individual reminder emails is repetitive.

Instead of hard-coding one email template, the application uses an LLM to generate the **subject and message body**, while the backend keeps control over the trusted recipient address and the actual email delivery.

### The core idea

```text
Assignment + Due Date
        ↓
Find students who have not submitted
        ↓
Send context to the LLM
        ↓
LLM generates an email through a tool call
        ↓
Backend validates the tool + arguments
        ↓
Resend sends the email
        ↓
Return execution results
```

---

## 🚀 What the application does

### 👨‍🏫 Assignment reminder workflow

The current application accepts:

- **Assignment name**
- **Due date**

The backend then processes students who are marked as not having submitted.

For every pending student, it:

1. Builds a constrained AI prompt.
2. Requires the LLM to use a `send_email` tool.
3. Reads the generated `subject` and `body`.
4. Validates the tool name and required arguments.
5. Keeps the recipient controlled by the backend.
6. Sends the email through Resend.
7. Retries retryable failures up to **2 additional times**.
8. Returns a structured execution summary.

---

## 🧠 AI Engineering Behind the Project

This project is intentionally more than an LLM API call. It demonstrates a small **AI application pipeline**.

### 01 — Context injection

The model receives only the information required to write the reminder:

```text
Student name
Assignment name
Due date
```

The prompt explicitly instructs the model not to invent deadlines, penalties, marks, or recipient information.

### 02 — Tool calling

The model is required to call:

```text
send_email(subject, body)
```

The AI generates the **message content**, but it does not choose the final recipient.

### 03 — Backend trust boundary

The backend executes the tool itself and passes the trusted student email to the delivery layer.

```text
LLM
 │
 │ subject + body
 ▼
Backend validation
 │
 │ trusted recipient
 ▼
Resend
```

This keeps the model away from direct control of the destination address.

### 04 — Validation + retries

The backend checks:

- expected tool name
- presence of `subject`
- presence of `body`
- string types
- non-empty values
- retryable delivery failures

Invalid tool arguments can be retried before the request is finally marked as failed.

---

## 🏗️ Architecture

<div align="center">

```text
┌──────────────────────┐
│      React UI        │
│   React 19 + Vite    │
└──────────┬───────────┘
           │
           │ POST /api/assignment-reminder/
           ▼
┌──────────────────────┐
│    Django + DRF      │
│   API + Validation   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Reminder Service   │
│  Student Processing  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Groq / LLM       │
│   Tool Call Required │
└──────────┬───────────┘
           │
      subject + body
           │
           ▼
┌──────────────────────┐
│   Tool Validation    │
│  Trusted Recipient   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Resend         │
│    Email Delivery    │
└──────────────────────┘
```

</div>

---

## 🖥️ Frontend

The frontend is a **React 19 + Vite** application.

### Interface includes

- Assignment name input
- Due-date selection
- Client-side validation
- Light / dark theme toggle
- Loading state with skeleton UI
- API error handling
- Execution summary dashboard
- Sent / failed student states
- Retry-attempt display
- Message ID display for successful deliveries
- Empty state when there are no pending students

### Frontend flow

```text
User enters assignment
        +
      due date
        ↓
Client validation
        ↓
POST request
        ↓
Loading / skeleton state
        ↓
API response
        ↓
Results dashboard
```

---

## ⚙️ Backend

The backend is built with **Django 6.1.1** and **Django REST Framework 3.18.1**.

### Main responsibilities

```text
API Endpoint
    ↓
Serializer validation
    ↓
Due-date validation
    ↓
Identify pending students
    ↓
Generate AI reminder
    ↓
Validate tool call
    ↓
Send email
    ↓
Aggregate results
```

### Main backend modules

| File | Responsibility |
|---|---|
| `views.py` | API endpoint and request flow |
| `serializers.py` | Assignment input validation |
| `services.py` | LLM integration, student processing and retry loop |
| `email_services.py` | Tool validation + Resend email delivery |
| `urls.py` | Reminder API routing |

---

## 🔌 API

### Endpoint

```http
POST /api/assignment-reminder/
```

### Request

```json
{
  "assignment_name": "Database Assignment",
  "due_date": "2026-10-15"
}
```

### Successful response shape

```json
{
  "assignment_name": "Database Assignment",
  "due_date": "2026-10-15",
  "results": {
    "total_students": 2,
    "sent": 2,
    "failed": 0,
    "results": [
      {
        "student": "Rahul",
        "status": "sent",
        "attempts": 1,
        "message_id": "..."
      }
    ]
  }
}
```

> The exact result values depend on the current student data and email-provider response.

---

## 📁 Project Structure

```text
ai-assignment-reminder/
│
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── reminder/
│   │   ├── migrations/
│   │   ├── email_services.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests.py
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── requirements.txt
└── .gitignore
```

---

## 🧰 Tech Stack

### Frontend

![React](https://img.shields.io/badge/React-19-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=flat-square&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

### Backend

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1.1-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.18.1-A30000?style=flat-square)

### AI + Email

![Groq](https://img.shields.io/badge/Groq-LLM-111111?style=flat-square)
![Resend](https://img.shields.io/badge/Resend-Email-000000?style=flat-square)

### Supporting tools

![Python Dotenv](https://img.shields.io/badge/python--dotenv-Environment%20Variables-3776AB?style=flat-square)

---

## 🛠️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/wafikh-salman/ai-assignment-reminder.git
cd ai-assignment-reminder
```

### 2. Create a virtual environment

From the repository root:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the backend environment/location used by the Django application:

```env
GROQ_API_KEY=your_groq_api_key
RESEND_API_KEY=your_resend_api_key
```

### 5. Run Django

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

The API is available at:

```text
http://127.0.0.1:8000/
```

### 6. Run the React frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will provide the local frontend URL.

---

## 🔐 Environment & Security Notes

API keys should **never** be committed to Git.

This project uses environment variables for:

- `GROQ_API_KEY`
- `RESEND_API_KEY`

The backend also follows an important design rule:

> **The model generates email content, while the backend controls the recipient.**

That separation is intentional and helps keep model-generated output away from direct control of sensitive delivery parameters.

---

## 📊 Execution Dashboard

After the reminder operation completes, the frontend displays:

```text
┌─────────────────────────────────────────┐
│           EXECUTION SUMMARY             │
├─────────────────────────────────────────┤
│ Total Students     Sent       Failed   │
│       3              2           1     │
├─────────────────────────────────────────┤
│ Rahul              ✓ Sent              │
│ Arjun              ✓ Sent              │
│ Anu                ✕ Failed            │
│                                      │
│ Attempts / Message ID / Error Details │
└─────────────────────────────────────────┘
```

This makes the AI workflow observable instead of hiding everything behind a single success message.

---

## 🧪 Current Project Scope

The repository is currently an **AI workflow prototype** rather than a production-ready academic platform.

### Current implementation

- Fixed in-code student dataset
- Assignment reminder API
- Pending-student filtering
- LLM-generated email content
- Required tool calling
- Backend argument validation
- Retry handling
- Resend email delivery
- React result dashboard

### Not yet implemented

- Persistent student database
- Authentication / authorization
- Teacher dashboard backend
- Assignment CRUD
- Real submission tracking
- Background scheduling
- Production deployment configuration
- Full automated test coverage

---

## 🔭 Future Direction

The architecture leaves room for the application to evolve into a more complete academic automation platform.

Potential next steps:

```text
CURRENT
  │
  ├── Fixed student data
  ├── Manual reminder trigger
  └── Direct request/response processing
       │
       ▼
FUTURE
  │
  ├── PostgreSQL-backed students
  ├── Authentication + roles
  ├── Assignment management
  ├── Submission tracking
  ├── Scheduled reminders
  ├── Background workers
  ├── Reminder history
  └── Production deployment
```

---

## 💡 What I Learned Building This

This project was created to explore practical **AI engineering concepts** rather than just calling an LLM for text generation.

The main concepts explored here are:

- Prompt construction
- Context injection
- LLM tool calling
- Backend-controlled tool execution
- Validation of model-generated arguments
- Retry and failure handling
- LLM + API integration
- AI-powered workflow automation
- Frontend observability of AI execution

---

## 👨‍💻 Author

**Wafikh Salman Saleem**

Backend-focused developer working with Python, Django, REST APIs, PostgreSQL, React and emerging AI/LLM engineering.

[![GitHub](https://img.shields.io/badge/GitHub-wafikh--salman-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wafikh-salman)

---

<div align="center">

### Built to understand AI systems by actually building one.

```text
INPUT → CONTEXT → LLM → TOOL CALL → VALIDATE → DELIVER → OBSERVE
```

⭐ Star the repository if you find the project useful.

</div>
