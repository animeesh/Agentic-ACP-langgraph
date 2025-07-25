from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import START,END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json

import warnings
warnings.filterwarnings('ignore')

import nest_asyncio
nest_asyncio.apply()

from abc import abstractmethod

class CalcState(TypedDict):
    task: str
    first_no: int
    second_no: int
    result: int
    
class BaseCalculationAgent:
    def __init__(self,prompt):
        self.llm = ChatOpenAI(model="gpt-4o")
        self.prompt = prompt
        #self.workflow = self.buildGraph()
        
    
    def getTaskDetails(self,state:CalcState):
        sys_msg = """
            You are a specialist in Maths calculations.
            From the given query identify the 2 numbers that need to be added.
            Identify only the numbers, not the operators.
            Output first_mumber and second_number.
            return output in JSON format
            """
        usr_msg = state["task"]
        
        messages = [
            SystemMessage(content=sys_msg),
            HumanMessage(content=usr_msg)
        ]
        
        result = self.llm.invoke(messages)           
        
        formatted = result.content
        formatted = formatted.replace("json","")
        formatted = formatted.replace("```","")
        print("RESULT from getTaskDetails === ",formatted)
        d = json.loads(formatted)
        
        a = d["first_number"]
        b = d["second_number"]
    
        print(" a and b values ", a,"---",b)
        return {"first_no":a,"second_no":b}
    
    @abstractmethod
    def calcuation_node(self,state:CalcState):
        pass
    
    def buildGraph(self,calc_node):
        graph = StateGraph(CalcState)
        graph.add_node("TaskDetails",self.getTaskDetails)
        graph.add_node("CalcNode",calc_node)
        graph.add_edge(START,"TaskDetails")
        graph.add_edge("TaskDetails","CalcNode")
        graph.add_edge("CalcNode",END)
        workflow = graph.compile()
        return workflow