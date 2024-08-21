# Project documentation


## Structure
```bash
fastapi_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── task_routes.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── task_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task_model.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py
│   └── db.py
│
├── .env
└── requirements.txt
```

# FastAPI Project Setup and Running

## Setup

1. **Clone the Repository**

   Clone the repository to your local machine if you haven't already:

   ```bash
   git clone <repository-url>
   cd fastapi_project

```bash
    python -m venv venv
```

2.  **Install Requirements**
    ```
        pip install -r requirements.txt
    ```

3. **Start Server**
    ```bash
        uvicorn app.main:app --reload
    ```


.env file
```bash
    OPENAI_API_KEY=your-openai-api-key
```

## Files Information
task_routes.py: Defines API endpoints.
task_controller.py: Handles request logic and responses.
task_model.py: Defines the database schema.
task_service.py: Contains business logic and external system interactions.

fastapi_project copy\app\models