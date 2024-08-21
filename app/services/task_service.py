from sqlalchemy.orm import Session
from app.models.task_model import Task
import openai
import time,os
from dotenv import load_dotenv

load_dotenv()
class TaskService:
    @staticmethod
    def get_best_position_from_extension(task_description: str) -> str:
        Assistant_ID = os.getenv('ASSISTANT_ID')
        client = openai.OpenAI()
        chat = client.beta.threads.create(
        messages=[
                {
                'role':'user',
                'content':f'{task_description}'
                }
            ]
        )
        run = client.beta.threads.runs.create(thread_id=chat.id,assistant_id=Assistant_ID)
        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(thread_id=chat.id,run_id = run.id)
            time.sleep(0.5)

        message = client.beta.threads.messages.list(thread_id=chat.id)

        first_message = message.data[0]
        first_text = first_message.content[0].text.value
        return first_text

    @staticmethod
    def get_best_position_from_db(db: Session, task_description: str) -> dict:
        """
        Retrieves the best job position from the database based on a given task description.
        
        Args:
            db (Session): The database session to query.
            task_description (str): A description of the task to find the best position for.
        
        Returns:
            dict: A dictionary containing the best job position and its corresponding room ID.
                  If no matching position is found, returns "Not found" as the position and None as the room ID.
        """
        # Fetch all positions from the database
        all_positions = db.query(Task.position).all()
        positions_list = [position[0] for position in all_positions]  # Extract positions from the query result

        # Create a prompt for the OpenAI API
        prompt = (
            f"Given the task description: '{task_description}', "
            "choose the most suitable job position from the following list:\n"
            f"{', '.join(positions_list)}."
        )
        
        response = openai.OpenAI().chat.completions.create(
        # response = openai.Completion.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=50,
            temperature=0.5
        )
        best_position = response.choices[0].message.content

        # Validate the best position is in the list
        if best_position in positions_list:
            # Retrieve the room_id for the best position
            best_task = db.query(Task).filter(Task.position == best_position).first()
            if best_task:
                return {"position": best_task.position, "room_id": best_task.room_id}
            else:
                print(f"Best position not found in database: {best_position}")  # Log if position is not found in DB

        return {"position": "Not found", "room_id": None, "prompt": prompt}  # Return default response and log the prompt used
    
    