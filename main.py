import re
import time
from langchain_ollama import ChatOllama

MODEL = ChatOllama(model="qwen3:8b", temperature=0)


def ask(system: str, user: str) -> str:
    """Run one LLM call with a system prompt and user input."""
    response = MODEL.invoke([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ])
    return re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL).strip()

def run_agent(name:str,system:str,user:str) -> str:
    """ Helper that logs how long each agent takes.."""
    print(f"calling agent {name}...")
    start = time.time()
    result  = ask(system,user)
    print(f"finished {name} in {time.time() - start :.1f}s")
    return result

# Agent 1 : Create a short outline 
def planner_agent(topic : str)-> str:
    return run_agent("planer_agent","Break this topic into 3 short study sections.",topic)

# Agent 2 : Turn  the outline into the notes
def teacher_agent(topic:str,outline:str) -> str:
    return run_agent("teacher_agent","Write short beginer-friendly notes using the outline", f"Topic: {topic}\n\nOutline:\n{outline}",)

# Agent 3 :Write and review question from the notes
def quiz_agent(topic:str,notes:str)->str:
    return run_agent("quizz_agent","Write 3 short review question based on the notes.",f"Topic: {topic}\n\nNotes:{notes}",)

def conclusion_agent(topic: str, notes: str) -> str:
    return run_agent(
        "conclusion_agent",
        "Write 3 short concluding takeaways based on the notes.",
        f"Topic: {topic}\n\nNotes:\n{notes}",
    )



def build_study_guide(topic:str) -> str:
    """ Run all these agents in the sequance and combine their output"""
    outline = planner_agent(topic)
    notes = teacher_agent(topic,outline)
    quiz = quiz_agent(topic, notes)
    conculsion = conclusion_agent(topic,notes)
    return(
        f"##Study Guide: {topic}\n\n"
        f"## Outline\n{outline}\n\n"
        f"## Review Question\n{quiz}\n\n"
        f"##Conculsion\n{conculsion}\n\n"
    )


if __name__ =="__main__":
    print("Warming the model...")
    MODEL.invoke("Say Ready...")
    print("Model is ready for you....\n")

    topic = input("Enter the study Topic:").strip()
    print(f"\n{build_study_guide(topic)}")
