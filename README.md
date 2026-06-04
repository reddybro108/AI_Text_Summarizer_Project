# AI Meeting Intelligence Assistant

[![CI and Docker Publish](https://github.com/reddybro108/AI_Text_Summarizer_Project/actions/workflows/main.yml/badge.svg)](https://github.com/reddybro108/AI_Text_Summarizer_Project/actions/workflows/main.yml)

## Overview

AI Meeting Intelligence Assistant is an NLP and GenAI-powered application designed to analyze meeting transcripts and automatically generate structured insights.

The system helps teams reduce manual note-taking by extracting meeting summaries, action items, key decisions, owners, and deadlines from meeting discussions.

Long meeting transcripts are automatically chunked with overlap so the summarizers can handle inputs of about 2000 words more reliably while preserving context across chunk boundaries.

Built using FastAPI, Hugging Face Transformers, SpaCy, and Streamlit, the application provides both API-based and interactive UI-driven meeting analysis.

The project also includes Docker support and a GitHub Actions workflow that can run tests and publish the image to Docker Hub.

---

## Features

### Meeting Summarization

Generate concise summaries from lengthy meeting transcripts.

### Action Item Extraction

Identify actionable tasks discussed during meetings.

### Owner Detection

Detect responsible individuals assigned to tasks.

### Deadline Detection

Extract deadlines and due dates from meeting conversations.

### Key Decision Extraction

Identify important decisions and approvals made during meetings.

### Processing Metrics

Track processing time for meeting analysis.

### Interactive Dashboard

Analyze meeting transcripts through a user-friendly Streamlit interface.

---

## Architecture

Meeting Transcript

↓

FastAPI Backend

↓

NLP Processing Pipeline

↓

Transformer-Based Summarization

↓

Entity & Information Extraction

↓

Structured JSON Response

↓

Streamlit Dashboard

---

## Tech Stack

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* Pydantic

### NLP & GenAI

* Hugging Face Transformers
* BART / DistilBART
* SpaCy
* Regex-based Information Extraction

### Frontend

* Streamlit

### Utilities

* Requests
* Logging
* Docker
* GitHub Actions

---

## Project Structure

```text
AI_Text_Summarizer_Project/
│
├── .github/
│   └── workflows/
│       └── main.yml
│
├── app/
│   ├── pipeline/
│   │   ├── summarizer.py
│   │   ├── extractor.py
│   │   ├── meeting_service.py
│   │   ├── prediction.py
│   │   ├── meeting_summarizer.py
│   │   └── llm_meeting_analyzer.py
│   │
│   ├── schemas/
│   │   ├── request_schema.py
│   │   └── response_schema.py
│   │
│   └── utils/
│
├── tests/
│   ├── test_api.py
│   ├── test_extractor.py
│   └── test_summarizer.py
│
├── main.py
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd AI_Text_Summarizer_Project
```

### Create Virtual Environment

```bash
py -3.11 -m venv atsenv
```

### Activate Environment

```bash
atsenv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download SpaCy Model

```bash
python -m spacy download en_core_web_sm
```

---

## Docker Hub

The application image is published to Docker Hub as:

```text
reddybro108/meeting-intelligence:latest
```

### Pull the Image

```bash
docker pull reddybro108/meeting-intelligence:latest
```

### Run the Container

```bash
docker run --rm -p 8000:8000 reddybro108/meeting-intelligence:latest
```

### Build Locally

```bash
docker build -t meeting-intelligence .
```

### Push to Docker Hub Manually

```bash
docker login -u reddybro108
docker tag meeting-intelligence:latest reddybro108/meeting-intelligence:latest
docker push reddybro108/meeting-intelligence:latest
```

---

## GitHub Actions

The repository includes a GitHub Actions workflow in [.github/workflows/main.yml](./.github/workflows/main.yml) that:

* installs dependencies
* runs the unit test suite
* builds and pushes the Docker image to Docker Hub on `push` events to `main` or `master`

To enable Docker Hub publishing from GitHub Actions, add these repository secrets in GitHub:

* `DOCKERHUB_USERNAME`
* `DOCKERHUB_TOKEN`

The published image name is `reddybro108/meeting-intelligence:latest`.

---

## Running FastAPI Application

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Running Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

## API Endpoints

### Health Check

```http
GET /health
```

### Text Summarization

```http
POST /summarize
```

Request:

```json
{
  "text": "Your text here"
}
```

### Meeting Analysis

```http
POST /summarize-meeting
```

Request:

```json
{
  "transcript": "Your meeting transcript here"
}
```

---

## Sample Output

```json
{
  "meeting_summary": "The team discussed deployment timelines and approved the production architecture.",
  "action_items": [
    {
      "owner": "Siva",
      "task": "Deploy model",
      "deadline": "Friday"
    }
  ],
  "key_decisions": [
    "FastAPI will be used in production"
  ],
  "processing_time_seconds": 2.1
}
```

---

## Future Enhancements

* PDF Upload Support
* DOCX Upload Support
* Executive Summary Generation
* Risk Detection
* Next Steps Extraction
* Local LLM Integration (Llama 3 / Phi-3)
* RAG-Based Meeting Search
* Release Tag-Based Docker Publishing
* AWS Deployment
* Meeting Report PDF Generation
* Multi-Meeting Analytics Dashboard

---

## Business Use Cases

* Engineering Standups
* Sprint Planning Meetings
* Client Discussions
* Project Status Reviews
* Product Requirement Meetings
* Executive Leadership Meetings

---

## Skills Demonstrated

* NLP
* Generative AI
* FastAPI Development
* Information Extraction
* Transformer Models
* API Design
* Streamlit Development
* Backend Engineering
* Prompt Engineering Concepts
* Enterprise AI Application Design

---

## Author

Amol Chilame

Associate Data Scientist

Specializations:
Machine Learning | NLP | Generative AI | RAG Systems | FastAPI | LangChain
