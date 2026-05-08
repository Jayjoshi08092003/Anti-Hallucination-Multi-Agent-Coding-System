import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

# --- THE TOOLS ---
async def read_target_file() -> str:
    """Reads the local file context to ground the agents in reality."""
    try:
        with open("target_code.py", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "ERROR: 'target_code.py' does not exist. Ground truth is missing."

async def run_agent_workflow(user_task: str):
    # 1. FIXED: Setup the Model Client with mandatory model_info
    model_client = OpenAIChatCompletionClient(
        model="llama-3.1-8b-instant",
        api_key="", 
        base_url="https://api.groq.com/openai/v1",
        temperature=0.0,
        model_info={
            "vision": False,
            "function_calling": True, # CRITICAL for your tools to work
            "json_output": True,
            "family": "llama"
        }
    )

    # 2. THE CODER
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        tools=[FunctionTool(read_target_file, description="Access local source code")],
        system_message=(
            "You are a Senior Dev. You do not assume; you check. "
            "Always use the read_target_file tool to verify existing code "
            "before suggesting any change. If a variable is missing, report it."
        )
    )

    # 3. THE JUDGE (LLM-as-a-Judge)
    judge = AssistantAgent(
        name="Judge",
        model_client=model_client,
        tools=[FunctionTool(read_target_file, description="Verify facts")],
        system_message=(
            "You are the Anti-Hallucination Guard. Your only job is to prove "
            "the Coder wrong. Read the file. If the Coder's suggestion contains "
            "logic, variables, or functions NOT present in the file, "
            "issue a 'REJECTED' verdict immediately. Otherwise, 'VERIFIED'."
        )
    )

    # 4. Orchestration
    team = RoundRobinGroupChat(participants=[coder, judge], max_turns=4)
    
    # 5. Execute
    return await team.run(task=user_task)