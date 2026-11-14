from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class File(BaseModel):
    path: str = Field(description="the file path to be created or modified")
    purpose: str = Field(description="the purpose of the file eg:'Main Application logic'")

class Plan(BaseModel):
    name: str = Field(description="the name of the app to be built")
    description: str = Field(description="the description of the app to be built")
    techstack:str = Field(description="the techstack app to be built eg:'python','javascript','react','flask'")
    features:str = Field(description="the features app to be built eg:'user authentication','data visualization'")
    files:list[File] = Field(description="the files to be built, each with path and purpose")


class ImplementationTask(BaseModel):
    filepath: str = Field(description="The path to the file to be modified")
    task_description: str = Field(
        description="A detailed description of the task to be performed on the file, e.g. 'add user authentication', 'implement data processing logic', etc.")


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(
        description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow")



class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(None, description="The content of the file currently being edited or created")

