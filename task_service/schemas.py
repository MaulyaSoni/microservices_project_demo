from pydantic import BaseModel , ConfigDict

# Define the TaskCreate schema
class TaskCreate(BaseModel):
    title: str
    description: str

# Define the Task schema
class Task(BaseModel):
    id: int
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)