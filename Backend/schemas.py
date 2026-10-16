from pydantic import BaseModel, ConfigDict, Field


class createTask(BaseModel):
    
    name:str = Field(description="name of the task to be done")
    description:str = Field(description="description of task to be done")
    is_completed:bool = Field(description="check if given Task is completed or not")

class Task(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id:int
    name:str = Field(description="name of the task to be done")
    description:str = Field(description="description of task to be done")
    is_completed:bool = Field(description="check if given Task is completed or not")
