import os
import json
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq

from tools import list_files, read_file, search_file


# Loading the API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found.")


# Creating the Groq client
client = Groq(api_key=api_key)


MODEL = "openai/gpt-oss-20b"


# Limiting how long the agent can continue using tools
MAX_STEPS = 10

# Locating the folder used for saving run results
RESULTS_FOLDER = Path(__file__).parent / "results"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files available in the movie workspace.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the complete contents of one file in the movie workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read."
                    }
                },
                "required": ["filename"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_file",
            "description": "Search one movie workspace file for lines containing a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to search."
                    },
                    "query": {
                        "type": "string",
                        "description": "The text to search for."
                    }
                },
                "required": ["filename", "query"]
            }
        }
    }
]


def execute_tool(tool_name, arguments):
    """Executing the tool selected by the agent."""

    if tool_name == "list_files":
        return list_files()

    if tool_name == "read_file":
        return read_file(arguments["filename"])

    if tool_name == "search_file":
        return search_file(
            arguments["filename"],
            arguments["query"]
        )

    return f"ERROR: UNKNOWN_TOOL: {tool_name}"


def save_run(run_data):
    """Saving one baseline run as a JSON file."""

    # Creating a unique timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"baseline_{timestamp}.json"

    file_path = RESULTS_FOLDER / filename

    # Saving the complete run in readable JSON format
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            run_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nRun saved to: {file_path}")

    return file_path


def run_agent(task):
    """Running the baseline tool-using agent."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a movie information agent operating inside a "
                "controlled file workspace. "
                "Answer the user's task using only information obtained "
                "from the available tools. "
                "Do not use outside knowledge. "
                "If information cannot be found in the available files, "
                "say that it is not available. "
                "You may use multiple tools when necessary."
            )
        },
        {
            "role": "user",
            "content": task
        }
    ]

    trajectory = []

    print("\n========================================")
    print("BASELINE AGENT")
    print("========================================")
    print(f"Task: {task}")

    for step in range(1, MAX_STEPS + 1):

        print(f"\n--- Step {step} ---")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Checking whether the agent wants to use tools
        if message.tool_calls:

            messages.append(message)

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"Tool selected: {tool_name}")
                print(f"Arguments: {arguments}")

                # Executing exactly what the agent requested
                result = execute_tool(tool_name, arguments)

                print(f"Observation: {result}")

                # Recording what happened
                trajectory.append(
                    {
                        "step": step,
                        "tool": tool_name,
                        "arguments": arguments,
                        "observation": result
                    }
                )

                # Returning the observation to the model
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    }
                )

        else:

            final_answer = message.content

            print("\n========================================")
            print("FINAL ANSWER")
            print("========================================")
            print(final_answer)

            run_data = {
                "timestamp": datetime.now().isoformat(),
                "system": "baseline",
                "model": MODEL,
                "max_steps": MAX_STEPS,
                "task": task,
                "trajectory": trajectory,
                "tool_calls": len(trajectory),
                "final_answer": final_answer,
                "status": "completed"
            }

            save_run(run_data)

            return run_data
        
    print("\n========================================")
    print("MAXIMUM STEPS REACHED")
    print("========================================")

    run_data = {
    "timestamp": datetime.now().isoformat(),
    "system": "baseline",
    "model": MODEL,
    "max_steps": MAX_STEPS,
    "task": task,
    "trajectory": trajectory,
    "tool_calls": len(trajectory),
    "final_answer": None,
    "status": "max_steps_reached"
    }

    save_run(run_data)

    return run_data

if __name__ == "__main__":

    task = (
    "According to the available files, find the benchmark rating "
    "of Robert Pattinson's upcoming Batman movie."

    )

    run_agent(task)