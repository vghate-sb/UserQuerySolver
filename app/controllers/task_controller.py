from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.task_service import TaskService
from app.db import SessionLocal

router = APIRouter()

def get_db():
    """
    Returns a database session using the SessionLocal class.
    
    Yields:
        Session: A database session object.
    
    Notes:
        The database session is closed when it goes out of scope.
    """
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/extension/")
def get_position_via_extension(task_description: str,db: Session = Depends(get_db)):
    """
    Handles a POST request to retrieve the best position for a given task description via an external service.

    Args:
        task_description (str): A description of the task.

    Returns:
        dict: A dictionary containing the best position for the task.
    """
    best_position = TaskService.get_best_position_from_extension(task_description,db)
    return {"position": best_position}

@router.post("/database/")
def get_position_via_database(task_description: str, db: Session = Depends(get_db)):
    """
    Retrieves the best position for a given task description from the database.

    Args:
        task_description (str): The description of the task.
        db (Session, optional): The database session. Defaults to the result of the `get_db` function.

    Returns:
        dict: The best position for the task.

    Raises:
        HTTPException: If the position is not found in the database.
    """
    result = TaskService.get_best_position_from_db(db, task_description)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Position not found")
