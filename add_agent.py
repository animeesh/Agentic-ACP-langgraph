from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYieldResume, RunYield,Server

import warnings
warnings.filterwarnings('ignore')

import nest_asyncio
nest_asyncio.apply()
from base_cal import BaseCalculationAgent

server = Server()

class AddAgent(BaseCalculationAgent):
    def __init__(self):
        sys_msg = """
            You are a specialist in Maths calculations.
            From the given query identify the 2 numbers that need to be added and output first_mumber and second_number.
            return output in JSON format
            """
        super().__init__(sys_msg)
        self.workflow = super().buildGraph(self.calcuation_node)
        
    
    def calcuation_node(self, state):
        a = state["first_no"]
        b = state["second_no"]
        print("*************** ADD NODE", a+b)
        return {"result": a+b}

@server.agent()
async def add_agent_service(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:    
       
        workflow = AddAgent().workflow
    
        task = input[0].parts[0].content
        #task = "Add numbers 7 and 50"
        print("########### INPUT TO GRAPH $$$$$$$$$$$")
        
        task_dict = {"task":task}
        result = workflow.invoke(task_dict)
        
        #print(result)
        yield Message(parts=[MessagePart(content=str(result))])

       
        
if __name__ == "__main__":
    server.run(port=8001)
