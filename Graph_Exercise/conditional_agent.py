from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    number1: int
    operation1: str
    number2: int
    number3: int
    number4: int
    operation2: str
    final_number_1: int
    final_number_2: int

def add_node1(state: AgentState) -> AgentState:
    """Adds number1 and number2"""
    state['final_number_1'] = state['number1'] + state['number2']
    return state

def add_node2(state: AgentState) -> AgentState:
    """Adds number3 and number4"""
    state['final_number_2'] = state['number3'] + state['number4']
    return state

def subtract_node1(state: AgentState) -> AgentState:
    """Subtracts number2 from number1"""
    state['final_number_1'] = state['number1'] - state['number2']
    return state

def subtract_node2(state: AgentState) -> AgentState:
    """Subtracts number4 from number3"""
    state['final_number_2'] = state['number3'] - state['number4']
    return state

def decide_next_node1(state: AgentState) -> str:
    """Router for the first operation"""
    if state['operation1'] == '+':
        return "addition_operation1"
    elif state['operation1'] == '-':
        return "subtraction_operation1"
    else:
        return "invalid_operation1"

def decide_next_node2(state: AgentState) -> str:
    """Router for the second operation"""
    if state['operation2'] == '+':
        return "addition_operation2"
    elif state['operation2'] == '-':
        return "subtraction_operation2"
    else:
        return "invalid_operation2"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("add_node1", add_node1)
    graph.add_node("add_node2", add_node2)
    graph.add_node("router1", lambda state: state)
    graph.add_node("subtract_node1", subtract_node1)
    graph.add_node("subtract_node2", subtract_node2)
    graph.add_node("router2", lambda state: state)

    graph.add_edge(START, "router1")

    graph.add_conditional_edges(
        "router1",
        decide_next_node1,
        {
            "addition_operation1": "add_node1",
            "subtraction_operation1": "subtract_node1"
        }
    )

    graph.add_edge("add_node1", "router2")
    graph.add_edge("subtract_node1", "router2")

    graph.add_conditional_edges(
        "router2",
        decide_next_node2,
        {
            "addition_operation2": "add_node2",
            "subtraction_operation2": "subtract_node2"
        }
    )

    graph.add_edge("add_node2", END)
    graph.add_edge("subtract_node2", END)

    return graph.compile()

if __name__ == "__main__":
    app = build_graph()

    initial_state = AgentState(
        number1=10,
        operation1="-",
        number2=5,
        number3=7,
        number4=2,
        operation2="+",
        final_number_1=0,
        final_number_2=0
    )

    result = app.invoke(initial_state)
    print(result)
