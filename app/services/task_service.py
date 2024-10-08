from sqlalchemy.orm import Session
from app.models.task_model import Task
import openai
import time,os, json,re
from dotenv import load_dotenv
from typing import Union

load_dotenv()
class TaskService:
    @staticmethod
    def get_best_position_from_extension(task_description: str,db: Session) -> str:
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
            print("Running")

        message = client.beta.threads.messages.list(thread_id=chat.id)
        print(message)

        first_message = message.data[0]
        first_text = json.loads(backtick_filter(first_message.content[0].text.value))
        
        print(first_text)
        
        position = best_position_respond(db,first_text,task_description)
        
        return position
        # return first_text
    
    

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
            f"You are an AI assistant designed to help users identify the most suitable job role for given task description from a provided list of job roles" +
            f"Given the task description: '{task_description}', " +
            "choose the most suitable job position from the following list:\n" +
            f"{', '.join(positions_list)}. \nJust give the job position only minimum 1 and max 3, no self metion or any other message, give me in following format where take room_id and role form given data"+""" {"positions" : [{"id": 1,"position":"Role","room_id":"123"},{"id": 2,"position":"Role","room_id":"124"}]}"""
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
        
        best_position = json.loads(response.choices[0].message.content)
        
        print(best_position)

        # Validate the best position is in the list
        position = best_position_respond(db,best_position,task_description)
        
        
        
        return position

        # return {"position": "Not found", "room_id": None, "prompt": prompt}  # Return default response and log the prompt used
    

def best_position_respond(db: Session, position_or_json: Union[str, dict], query: str) -> dict:
    if isinstance(position_or_json, str):
        position = position_or_json
    elif isinstance(position_or_json, dict):
        # Assuming the JSON format you mentioned
        # position = position_or_json.get("positions", [{}])[0].get("position")
        #[{'id': 1, 'position': 'Mobile Repair Technician', 'room_id': '123'}]
        print(position_or_json)
        print(type(position_or_json))
        ans_positions = {}
        try:
            ans_positions = {}
            try:
                for i in position_or_json['positions']:
                    position = i.get('position')
                    room_id = i.get("room_id", None)
                    answer = f"Your query '{query}' will be answered by role '{position}' and its room id '{room_id}'"
                    ans_positions[position] = {"position": position, "room_id": room_id, "answer": answer}
            except:
                position = position_or_json[0]['position']
                room_id = position_or_json[0].get("room_id", None)
                answer = f"Your query '{query}' will be answered by role '{position}' and its room id '{room_id}'"
                ans_positions[position] = {"position": position, "room_id": room_id, "answer": answer}
            return ans_positions
        except:
            room_id = None
    else:
        raise ValueError("Invalid input type. Must be a string or a JSON-like dictionary.")

    all_positions = db.query(Task.position).all()
    positions_list = [position[0] for position in all_positions] 

    if position in positions_list:
        best_task = db.query(Task).filter(Task.position == position).first()
        if best_task:
            answer = f"Your query '{query}' will be answered by role '{best_task.position}' and its room id '{best_task.room_id}'"
            return {"position": best_task.position, "room_id": best_task.room_id, "answer": answer}
    else:
        print(f"Best position not found in database: {position}")  # Log if position is not found in DB
        answer = f"Your query '{query}' will be answered by role '{position}' and it doesn't have any room id"
        return {"position": None, "room_id": None, "answer": answer}


def backtick_filter(data):
    pattern = r'{.*\}'
    match = re.search(pattern, data)
    return match.group()
# def best_position_respond(db: Session,position:str,query:str) -> dict:
#     all_positions = db.query(Task.position).all()
#     positions_list = [position[0] for position in all_positions] 
    
    
#     if position in positions_list:
#             best_task = db.query(Task).filter(Task.position == position).first()
#             answer = f"Your query '{query}' will be answered by role '{best_task.position}' and its room id '{best_task.room_id}'"
#             if best_task:
#                 return {"position": best_task.position, "room_id": best_task.room_id,"answer":answer}
#     else:
#         print(f"Best position not found in database: {position}")  # Log if position is not found in DB
#         answer = f"Your query '{query}' will be answered by role '{position}' and it haven't any room id"
#         return {"position": None, "room_id": None,"answer":answer}
    
    
    