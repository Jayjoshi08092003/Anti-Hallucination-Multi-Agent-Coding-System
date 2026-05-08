import streamlit as st
import asyncio
from train import run_agent_workflow

st.set_page_config(page_title="Agent Dashboard", layout="wide")

# --- HEADER ---
st.title("🛡️ Anti-Hallucination Multi-Agent System")
st.info("The Coder proposes. The Judge verifies. Only the Truth survives.")

# --- SIDEBAR (Context Management) ---
with st.sidebar:
    st.header("⚙️ Environment")
    if st.button("🔧 Initialize target_code.py"):
        with open("target_code.py", "w") as f:
            f.write("def calculate_total(price, tax):\n    return price + tax")
        st.success("File initialized!")

# --- CELL 1: INPUT BOX ---
st.subheader("📥 Cell 1: User Command")
with st.container(border=True):
    user_input = st.text_input("Enter task for agents:", "Add a 10% discount logic to the calculate_total function.")
    run_clicked = st.button("🚀 Execute Workflow")

st.divider()

# --- CELL 2: THE OUTPUT TERMINAL ---
st.subheader("🖥️ Cell 2: Agent Output Console")
output_area = st.container(border=True)

if run_clicked:
    with output_area:
        with st.status("Agents are debating... (Round Robin Orchestration)", expanded=True) as status:
            # Setup the async loop for Streamlit
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Backend Execution
                result = loop.run_until_complete(run_agent_workflow(user_input))
                
                # Render results in the console
                for msg in result.messages:
                    with st.chat_message(msg.source):
                        st.markdown(f"**{msg.source}**")
                        # Use code block if content looks like Python
                        if "def " in msg.content or "import " in msg.content:
                            st.code(msg.content, language="python")
                        else:
                            st.write(msg.content)
                
                status.update(label="Workflow Complete!", state="complete")
            
            except Exception as e:
                status.update(label="Process Halted", state="error")
                st.error(f"Error: {e}")
else:
    output_area.write("Terminal idle. Enter a command above to begin.")