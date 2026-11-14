def planner_prompt(user_prompt:str)->str:
    # For Using user prompt
    # user_prompt = "create a simple calculator web application"

        PLANNER_PROMPT = f"""
    You are the PLANNER AGENT.convert the user prompt into a Complete Engineering Plan
    User Request: {user_prompt}
    """
        return PLANNER_PROMPT


def architect_prompt(plan:str)->str:
    ARCHITECT_PROMPT = f"""
    You are the ARCHITECT AGENT.Given this project plan,break it down into explicit engineering tasks
    
    RULES:
    -For each FILE in the plan. create one or more implementation tasks
    -In each task description
        *Specify exactly what to implement
        *Name the variables,functions,classes and components to be defined
        *Mention how this task task depends on or will be used by preious tasks
        * Include integration details: imports,expected functions signaturs,data flow
        
    -Order tasks so that dependencies are implemented first 
    -Each step must be self contaminates but also carry forward the elevant context
    
    Project Plan:
    
    {plan}
    """
    return ARCHITECT_PROMPT


def coder_system_prompt()->str:
    CODER_SYSTEM_PROMPT = """
        You are the coder agent.you re implementing a specific enginerring tasks
        you are given a task description below, write complete code for it
        you have access to tool to read and write files
        
        Always:
        Review all exsisting files to maintain compatability
        - Review all existing files to maintain compatibility.
- Implement the FULL file content, integrating with other modules.
- Maintain consistent naming of variables, functions, and imports.
- When a module is imported from another file, ensure it exists and is implemented as described.
    
    """
    return CODER_SYSTEM_PROMPT