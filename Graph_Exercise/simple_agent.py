from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str

def Compliment_Agent(state: AgentState) -> AgentState:
    """This function compliments the user for learning"""
    state['name'] = f"{state['name']}, you are doing an amazing job learning LangChain"
    return state

graph = StateGraph(AgentState)

graph.add_node('compliment', Compliment_Agent)

graph.set_entry_point('compliment')
graph.set_finish_point('compliment')

app = graph.compile()

result = app.invoke({'name': 'BOB'})
print(result['name'])
