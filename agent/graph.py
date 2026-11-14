from dotenv import load_dotenv
from langgraph.graph import StateGraph, state
from langchain_groq import ChatGroq
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

from prompts import *
from states import *
from tools import *

# from pydantic import BaseModel,Field

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")



user_prompt = "create a simple calculator web application"


def planner_agent(state : dict) -> dict:
    users_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    return {"plan": resp}

def architect_agent(state : dict) -> dict:
     plan:Plan = state["plan"]
#      previous state has plan so we get for architect purpose
     resp = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))

     if resp is None:
         raise ValueError("Architect did not return a valid response")
     # made resp as task plan defined in states schema so resp allow any variable resp.asdf

     return {"task_plan": resp}

def coder_agent(state : dict) -> dict:
    steps = state['task_plan'].implementation_steps
    current_step_idx = 0
    current_task = steps[current_step_idx]
    existing_content = read_file.run(current_task.filepath)
    user_prompt = (
        f"Task:{current_task.task_description}\n"
        f"File:{current_task.filepath}\n"
        f"Exsisting content:\n{existing_content}\n"
        "use write_file(path,content) to save your changes"
    )
    system_prompt = coder_system_prompt()
    # resp = llm.invoke(system_prompt + user_prompt)
    coder_tools = [read_file,write_file,list_files,get_current_directory]
    # react_agent = create_react_agent(llm,coder_tools)
    react_agent = create_agent(llm, coder_tools)

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})
    # react_agent.invoke({"messages":[{"role":"system","content":"system_prompt"},{"role":"user","content":"user_prompt"}]})

    # return {"code":resp.content}
    return {}
# state = {"user_prompt":user_prom
# pt,plan:state}

graph = StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.add_node("architect",architect_agent)
graph.add_node("coder",coder_agent)
graph.add_edge("planner","architect")
graph.add_edge("architect","coder")


graph.set_entry_point("planner")

agent = graph.compile()

result = agent.invoke({"user_prompt":user_prompt})
print(result)

# state - > planner -< after - state has both agnet and planner

# resp = llm.invoke("Who invented zero,answer in 1 sentence")
# print(resp.content)

# For Structured output define schema(class)
# class Schema(BaseModel):
#     price: float
#     eps: float
#
# resp = llm.with_structured_output(Schema).invoke("Extract Price and EPS from this report: NVIDIA reported Quarterly EPS of 2.3 and their current price is $100")
#
# print(resp)

# For Using user prompt
# prompt = planner_prompt(user_prompt)
#
# resp = llm.with_structured_output(Plan).invoke(prompt)
# print(resp)




