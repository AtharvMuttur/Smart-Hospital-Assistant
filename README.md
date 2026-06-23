# Intelligent Hospital Appointment Assistant

## PROJECT OVERVIEW

Build an AI-powered conversational chatbot for a hospital that can:

1. Book appointments
2. Cancel appointments
3. Reschedule appointments
4. Check doctor availability
5. Answer hospital FAQs
6. Maintain conversational context
7. Retrieve information from a database
8. Optionally use RAG for document-based question answering

The goal is to learn:

- Intent Classification
- Entity Extraction
- Conversational AI
- Dialogue Management
- API Integration
- Database Operations
- RAG Systems
- LLM Integration

This is an intermediate-level AI + Full Stack project.

---

## MAIN USE CASES

### 1. Appointment Booking

**User:** "I want to book an appointment with Dr. Rao tomorrow at 3 PM"

**Flow:**
- Detect booking intent
- Extract doctor name
- Extract date
- Extract time
- Check slot availability
- Save appointment
- Return confirmation

### 2. Appointment Cancellation

**User:** "Cancel my appointment with Dr. Rao"

**Flow:**
- Retrieve appointment
- Confirm cancellation
- Update database

### 3. Appointment Rescheduling

**User:** "Move my appointment to Friday at 11 AM"

**Flow:**
- Find existing appointment
- Check new slot availability
- Update booking

### 4. Doctor Availability

**User:** "Is Dr. Rao available tomorrow?"

**Flow:**
- Query doctor schedule
- Return available slots

### 5. FAQ Queries

**User:** "What are the hospital visiting hours?"

**Flow:**
- Retrieve answer from FAQ database
- Return answer

### 6. Insurance Queries

**User:** "Do you accept Star Health Insurance?"

**Flow:**
- Search hospital documents
- Return answer

---

## TECH STACK

### Frontend
- **React**
  - Login
  - Registration
  - Chat Interface
  - Appointment History
  - Appointment Management

### Backend
- **FastAPI**
  - API layer
  - Authentication
  - Database access
  - Rasa integration

Example APIs:
- `POST /book`
- `POST /cancel`
- `POST /reschedule`
- `GET /appointments`
- `GET /doctors`

### Conversational AI Layer
- **Rasa**
  - Intent Classification
  - Entity Extraction
  - Slot Filling
  - Dialogue Management
  - Story Management

### Database
- **Recommended:** PostgreSQL
- **Alternative:** MongoDB

### Optional RAG Layer

**Components:**
- LangChain
- ChromaDB
- FAISS
- Sentence Transformers
- Gemini/OpenAI

**Used for:**
- FAQ retrieval
- Insurance policies
- Hospital documentation

---

## SYSTEM ARCHITECTURE

```
User
 |
 v
React Frontend
 |
 v
FastAPI Backend
 |
 +----------------------+
 |                      |
 v                      v
Rasa                 Database
 |
 v
Custom Actions
 |
 +-------------------+
 |                   |
 v                   v
Database          RAG Service
                      |
                      v
                ChromaDB/FAISS
                      |
                      v
                 Documents
```

---

## RASA DESIGN

### INTENTS

- `book_appointment`
- `cancel_appointment`
- `reschedule_appointment`
- `doctor_availability`
- `view_appointments`
- `faq`
- `greet`
- `goodbye`
- `affirm`
- `deny`

### ENTITIES

- `doctor_name`
- `date`
- `time`
- `specialization`
- `appointment_id`
- `insurance_provider`

**Example:**

User: "Book appointment with Dr. Rao tomorrow at 3 PM"

Entities:
```json
{
  "doctor_name": "Dr. Rao",
  "date": "tomorrow",
  "time": "3 PM"
}
```

### SLOTS

Slots store conversation state.

**Example:**

- `doctor_name`
- `date`
- `time`
- `appointment_id`

**Conversation:**

```
User: Book appointment

Bot: Which doctor?

User: Dr Rao

Store: doctor_name = "Dr Rao"

Bot: Which date?

User: Tomorrow

Store: date = "tomorrow"

Continue until all required information is collected.
```

### STORIES

Example Conversation:

```
User: Book appointment

Bot: Which doctor?

User: Dr Rao

Bot: Which date?

User: Tomorrow

Bot: Which time?

User: 3 PM

Bot: Appointment booked
```

---

## CUSTOM ACTIONS

### action_book_appointment

**Responsibilities:**
- Validate doctor
- Check slot
- Save appointment
- Return confirmation

### action_cancel_appointment

**Responsibilities:**
- Locate appointment
- Cancel appointment
- Update database

### action_reschedule_appointment

**Responsibilities:**
- Locate appointment
- Check new slot
- Update booking

### action_check_availability

**Responsibilities:**
- Retrieve doctor schedule
- Return available slots

### action_answer_faq

**Responsibilities:**
- Retrieve FAQ answer
- Return response

---

## DATABASE SCHEMA

### USERS TABLE

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);
```

### DOCTORS TABLE

```sql
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100)
);
```

### APPOINTMENTS TABLE

```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    user_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    status VARCHAR(50)
);
```

**Possible Status Values:**
- `Booked`
- `Cancelled`
- `Completed`
- `Rescheduled`

---

## API DESIGN

### BOOK APPOINTMENT

**Endpoint:** `POST /book`

**Request:**
```json
{
  "user_id": 1,
  "doctor_id": 2,
  "date": "2026-06-25",
  "time": "15:00"
}
```

### CANCEL APPOINTMENT

**Endpoint:** `POST /cancel`

**Request:**
```json
{
  "appointment_id": 15
}
```

### DOCTOR AVAILABILITY

**Endpoint:** `GET /doctor/{doctor_id}/availability`

---

## RAG LAYER (PHASE 2)

**Hospital Documents:**
- `hospital_policies.pdf`
- `insurance_guide.pdf`
- `visiting_rules.pdf`
- `doctor_directory.pdf`

**Pipeline:**

```
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
LLM
   ↓
Answer
```

**Tools:**
- LangChain
- ChromaDB
- Sentence Transformers
- Gemini API

---

## FRONTEND FEATURES

### LOGIN PAGE

**Fields:**
- Email
- Password

### REGISTER PAGE

**Fields:**
- Name
- Email
- Phone
- Password

### CHAT PAGE

**Features:**
- Conversation window
- Input box
- Send button

### APPOINTMENT DASHBOARD

**Display:**
- Appointment ID
- Doctor
- Date
- Time
- Status

**Actions:**
- Cancel
- Reschedule

---

## DEVELOPMENT ROADMAP

### PHASE 1 (Backend Foundation)

- [ ] Setup FastAPI
- [ ] Setup PostgreSQL
- [ ] Create database schema
- [ ] Create CRUD APIs
- [ ] Test APIs using Postman

### PHASE 2 (Rasa)

- [ ] Install Rasa
- [ ] Create intents
- [ ] Create entities
- [ ] Create stories
- [ ] Create slots
- [ ] Train model

### PHASE 3 (Business Logic)

- [ ] Create custom actions
- [ ] Connect Rasa with FastAPI
- [ ] Connect FastAPI with PostgreSQL

### PHASE 4 (Frontend)

- [ ] Build React frontend
- [ ] Create login/register pages
- [ ] Create chat interface
- [ ] Create appointment dashboard
- [ ] Connect frontend with backend

### PHASE 5 (FAQ System)

- [ ] Create FAQ dataset
- [ ] Add FAQ retrieval
- [ ] Integrate with chatbot

### PHASE 6 (RAG)

- [ ] Add document ingestion
- [ ] Chunk documents
- [ ] Generate embeddings
- [ ] Store in ChromaDB/FAISS
- [ ] Build retriever

### PHASE 7 (LLM Integration)

- [ ] Connect Gemini/OpenAI
- [ ] Use retrieved context
- [ ] Generate natural language answers

### PHASE 8 (Deployment)

**Frontend:**
- Vercel

**Backend:**
- Render

**Database:**
- PostgreSQL / Supabase / MongoDB Atlas

---

## FINAL ARCHITECTURE

```
React Frontend
      |
      v
FastAPI Backend
      |
      +---- PostgreSQL
      |
      +---- Rasa
      |
      +---- Custom Actions
      |
      +---- ChromaDB
      |
      +---- Gemini/OpenAI
```

---

## LEARNING OUTCOMES

By completing this project, you will learn:

- NLP Fundamentals
- Intent Classification
- Entity Extraction
- Conversational AI
- Dialogue Management
- REST APIs
- FastAPI
- PostgreSQL
- Rasa
- Vector Databases
- Embeddings
- RAG Architecture
- LLM Integration
- React Frontend Development
- Full Stack AI Application Development

---

## RESUME DESCRIPTION

Developed an Intelligent Hospital Appointment Assistant using React, FastAPI, PostgreSQL, Rasa, and ChromaDB. Implemented intent classification, entity extraction, slot-filling dialogue management, appointment booking workflows, FAQ retrieval, and RAG-based document question answering. Designed REST APIs, integrated database-backed appointment management, and built an end-to-end conversational AI system capable of handling healthcare support operations.
