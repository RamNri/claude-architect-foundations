import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv(override=True)

from calculator import calculator


client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")


tools = [
    {
        "type": "function",
        "name": "calculator",
        "description": "Performs basic arithmetic operations.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "The arithmetic operation to perform.",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ]
                },
                "a": {
                    "type": "number",
                    "description": "The first number."
                },
                "b": {
                    "type": "number",
                    "description": "The second number."
                }
            },
            "required": [
                "operation",
                "a",
                "b"
            ]
        }
    }
]

def execute_tool(tool_call):
   if tool_call.name != "calculator":
      raise ValueError(f"Unknown tool: {tool_call.name}")

   arguments = json.loads(tool_call.arguments)
   result = calculator(**arguments)
   return result


def run_agent(user_message):

   response = client.responses.create(
      model=MODEL,
      tools=tools,
      input=user_message
   )

   while True:
      tool_calls = [ item for item in response.output if item.type == "function_call"]

      if not tool_calls:
         return response.output_text

      tool_outputs = []

      for tool_call in tool_calls:
        result = execute_tool(tool_call)

        print("Tool:", tool_call.name)
        print("Arguments:", tool_call.arguments)
        print("Result:", result)

        tool_outputs.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(result)
         })

        response = client.responses.create(
           model=MODEL,
           tools=tools,
           previous_response_id=response.id,
           input=tool_outputs 
        )


if __name__ == "__main__":
    answer = run_agent("What is 125 * 37 + 890?")
    print(f"\n Final answer: {answer}")