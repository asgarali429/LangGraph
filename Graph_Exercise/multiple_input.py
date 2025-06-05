from typing import TypedDict, List
from langgraph.graph import StateGraph
import math

class AgentState(TypedDict):
    values: List[int]
    name: str
    operation: str
    message: str

def operation_node(state: AgentState) -> AgentState:
    """This function performs addition or multiplication based on user input."""
    result = None

    if state['operation'] == '+':
        result = sum(state['values'])
    elif state['operation'] == '*':
        result = math.prod(state['values'])
    else:
        print('Enter the operation + or *')

    # Print the message as intended
    if result is not None:
        state['message'] = (
            f"Hi {state['name']}, the result of {state['operation']} of {state['values']} is {result}"
        )

    return state

graph = StateGraph(AgentState)

graph.add_node('perform', operation_node)

graph.set_entry_point('perform')

graph.set_finish_point('perform')

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({'values': [1, 2, 3, 4], "name": 'BOB', "operation": '*', "message": ""})
    print(result['message'])
