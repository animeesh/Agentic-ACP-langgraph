from typing import TypedDict, Annotated
from operator import add
from langgraph.prebuilt.chat_agent_executor import AgentState #MessagesState #
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from acp_sdk.client import Client
import asyncio
from colorama import Fore 
from langgraph.checkpoint.memory import InMemorySaver

class CalculatorState(AgentState):
    result: Annotated[str, add] # Example of an additional state variable

model = ChatOpenAI(model="gpt-4o")
checkpointer = InMemorySaver()

@tool
async def addCalulator(task: str):  
    """
    This tool can be used for adding two numbers
    args:
    task: str - user's query which contains the numbers to be added
    """      
    async with Client(base_url="http://127.0.0.1:8001") as client:
            run = await client.run_sync(      
                agent="add_agent_service", input=task
            )
            print("RUN = ", run)
            print(Fore.RED + run.output[0].parts[0].content + Fore.RESET)
            return run.output[0].parts[0].content 
                
    
@tool
async def substractCalulator(task): 
    """
    This tool can be used for substracting two numbers
    args:
    task: str - user's query which contains the numbers to be substracted
    """             
    async with Client(base_url="http://127.0.0.1:8002") as client:
            run = await client.run_sync(      
                agent="subtract_agent_service", input=task
            )
            print("RUN = ", run)
            print(Fore.GREEN + run.output[0].parts[0].content + Fore.RESET) 
            return run.output[0].parts[0].content  

@tool
async def multiplyCalulator(task): 
    """
    This tool can be used for multiplying two numbers
    args:
    task: str - user's query which contains the numbers to be substracted
    """             
    async with Client(base_url="http://127.0.0.1:8003") as client:
            run = await client.run_sync(      
                agent="multiply_agent_service", input=task
            )
            print("RUN = ", run)
            print(Fore.MAGENTA + run.output[0].parts[0].content + Fore.RESET) 
            return run.output[0].parts[0].content 

@tool
async def divideCalulator(task): 
    """
    This tool can be used for dividing two numbers
    args:
    task: str - user's query which contains the numbers to be substracted
    """             
    async with Client(base_url="http://127.0.0.1:8004") as client:
            run = await client.run_sync(      
                agent="division_agent_service", input=task
            )
            print("RUN = ", run)
            print(Fore.MAGENTA + run.output[0].parts[0].content + Fore.RESET) 
            return run.output[0].parts[0].content 

async def execute(task):   
    agent = create_react_agent(
    model=model,
    tools=[addCalulator,substractCalulator,multiplyCalulator,divideCalulator],
    checkpointer=checkpointer,
    state_schema=CalculatorState,
    prompt="""
                You are a helpful assistant. 
                User will provide query for doing maths calculations. 
                First analyze the task and break down the query into individual tasks and for each task do calculation separately 
                using given tools.
                There may situations where result of one task may be input to the next task. 
                In that case extract the value from the result field of the previous step and pass it to next task.
                Only Result of one task should be passed to next task
                Based on the query use appropriate tools provided to do the calculations.
                Use only given tools for calculation. Do not do anything without using tools.
                Stop calculation as soon as result is calculated.
            """
    )
    config = {"configurable": {"thread_id": "vin-calc-1"}}
    # Invoke the agent with a user query
    input_message = {"messages": [{"role": "user", "content": task}]}
    result = await agent.ainvoke(input_message,config)
    print("#### RESULT IN CLASS $$$$$$$$$")
    # Print the final output
    print(result["messages"][-1].content)
    
if __name__ == "__main__":
    import asyncio
   
    task2 = """
    I bought 10 mangoes from shop. 
    I Ate 2 mangoes.
    From the remaining mangoes I gave 2 mangoes to my freind.
    Then I bought some more mangoes so that total mangoes got 25.
    How many mangoes did i bought? how much should bought mangoes multiply by 5?    
    """
    
    
    result = asyncio.run(execute(task2))