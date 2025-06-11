
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import random

class AgentState(TypedDict):
    player_name: str
    target_number: int
    guesses: List[int]
    attempts: int
    hint: str
    lower_bond: int
    higher_bond: int

def setup_node(state: AgentState) -> AgentState:
    """Initial setup for the game."""
    state['player_name'] = f"Hi, {state['player_name']}! Welcome to the guessing game."
    state['target_number'] = random.randint(state['lower_bond'], state['higher_bond'])
    state['guesses'] = []
    state['attempts'] = 0
    state['hint'] = "Game has started! Guess the number."
    state['lower_bond'] = 1
    state['higher_bond'] = 20
    print(f"{state['player_name']} The game has begun. I'm thinking of a number between 1 and 20.")
    return state

def guess_node(state: AgentState) -> AgentState:
    """Simulates a guess from the agent."""
    possible_guess = [i for i in range(state['lower_bond'], state['higher_bond']+1) if i not in state['guesses']]
    if possible_guess:
        guess = random.choice(possible_guess)
    else:
        guess = random.randint(state['lower_bond'], state['higher_bond'])
    
    state['guesses'].append(guess)
    state['attempts'] += 1

    print(f"Attempt {state['attempts']}: Guessing {guess} (Current range: {state['lower_bond']}-{state['higher_bond']})")
    return state

def hint_node(state: AgentState) -> AgentState:
    """Provides hints based on the guess."""
    current_guess = state['guesses'][-1]
    if current_guess < state['target_number']:
        state['hint'] = "Hint: The number is higher."
        state['lower_bond'] = current_guess + 1
        print(state['hint'])
    elif current_guess > state['target_number']:
        state['hint'] = "Hint: The number is lower."
        state['higher_bond'] = current_guess - 1
        print(state['hint'])
    else:
        state['hint'] = f"Correct! You found the number {state['target_number']} in {state['attempts']} attempts."
        print(f"Success! {state['hint']}")
    return state

def should_continue(state: AgentState) -> str:
    """Determines if the game should continue."""
    latest_guess = state['guesses'][-1]
    if latest_guess == state['target_number']:
        print("GAME OVER: Number found!")
        return "end"
    elif state['attempts'] >= 7:
        print(f"GAME OVER: Maximum attempts reached! The number was {state['target_number']}")
        return "end"
    else:
        print(f"CONTINUING: {state['attempts']}/7 attempts used")
        return "continue"

graph = StateGraph(AgentState)

graph.add_node("setup", setup_node)
graph.add_node("guess", guess_node)
graph.add_node("hint_", hint_node)

graph.add_edge("setup", "guess")
graph.add_edge("guess", "hint_")

graph.add_conditional_edges(
    "hint_",
    should_continue,
    {
        "continue": "guess",
        "end": END
    }
)

graph.set_entry_point("setup")

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({
        "player_name": "Student",
        "guesses": [],
        "attempts": 0,
        "lower_bond": 1,
        "higher_bond": 20
    })
