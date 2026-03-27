# XAI in the Medical Field

## Project Idea
A full-stack web application that integrates Explainable AI (XAI) into medical decision-making, enabling doctors to trust and understand AI-driven predictions.

- Django & React web application for AI-driven medical predictions using Django REST APIs
- Integrated AI models to assist in informed decision-making
- Enhanced trustworthiness with multiple explanation methods
- MLFlow integration for model storing, tracking and performance monitoring

## User Roles

### Technical Expert (Admin):
- Register AI models (any type, any schema)
- Define inputs and outputs dynamically
- Monitor and track models using MLflow
- Manage and update models
### Medical Expert (User)
- Select a medical model (use case)
- Fill in dynamically generated forms
- Receive predictions instantly
- Request explanations (XAI methods)
- Provide feedback and rate results



## Main Structure

### Backend (Django + Django REST Framework)

The XAIbackend contains multiple sub-apps (AIModel, Query, Explanation, etc.) that define the system structure and handle the core business logic.


### Frontend (React + Vite)

The XAIfrontend provides the user interfaces for both the admin and the medical user.



## Setup

### Backend

1. Create and activate venv
2. `pip install -r requirements.txt`
3. `cd XAIbackend`
4. `python manage.py makemigrations`
5. `python manage.py migrate`
6. `python manage.py runserver`

### Frontend

1. `cd XAIfrontend`
2. `npm install`
3. `npm run dev`

## Notes

- Some models may require additional dependencies (work in progress)
- The project structure and views are currently being improved and reorganized
- A demo of the system pipeline is available in the `demo` folder


