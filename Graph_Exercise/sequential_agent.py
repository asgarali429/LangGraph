from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    skills: List[str]
    message: str

def first_node(state: AgentState) -> AgentState:
    """This node takes a name as input"""
    state['message'] = f"{state['name']}, Welcome to the System!"
    return state

def second_node(state: AgentState) -> AgentState:
    """This node takes an age as input"""
    state['message'] += f" You are {state['age']} years old!"
    return state

def third_node(state: AgentState) -> AgentState:
    """This node takes a list of skills as input"""
    skills_str = ', '.join(state['skills'])
    state['message'] += f" You have the following skills ---> {skills_str}!"
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node('first', first_node)
    graph.add_node('second', second_node)
    graph.add_node('third', third_node)

    graph.set_entry_point('first')
    graph.add_edge('first', 'second')
    graph.add_edge('second', 'third')
    graph.set_finish_point('third')

    return graph.compile()

if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({'name': 'BOB', 'age': 25, 'skills': ['Python', 'SQL']})
    print(result['message'])
