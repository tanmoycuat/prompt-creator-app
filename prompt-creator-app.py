import streamlit as st
import json
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Prompt Creator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'prompts' not in st.session_state:
    st.session_state.prompts = []
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = {
        "role": "",
        "context": "",
        "instructions": [],
        "constraints": [],
        "output_format": "",
        "verification": [],
        "name": "",
        "created_at": ""
    }
if 'editing_instruction_index' not in st.session_state:
    st.session_state.editing_instruction_index = -1
if 'editing_constraint_index' not in st.session_state:
    st.session_state.editing_constraint_index = -1
if 'editing_verification_index' not in st.session_state:
    st.session_state.editing_verification_index = -1

# Functions for handling prompts
def save_prompt():
    if not st.session_state.current_prompt["name"]:
        st.error("Please give your prompt a name before saving.")
        return
        
    # Add created_at timestamp
    st.session_state.current_prompt["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add to prompts list
    st.session_state.prompts.append(st.session_state.current_prompt.copy())
    
    # Reset current prompt
    st.session_state.current_prompt = {
        "role": "",
        "context": "",
        "instructions": [],
        "constraints": [],
        "output_format": "",
        "verification": [],
        "name": "",
        "created_at": ""
    }
    st.success("Prompt saved successfully!")

def export_prompt():
    prompt_text = f"""<s>
{st.session_state.current_prompt["role"]}
</s>

<Context>
{st.session_state.current_prompt["context"]}
</Context>

<Instructions>
{format_list_items(st.session_state.current_prompt["instructions"])}
</Instructions>

<Verification>
{format_list_items(st.session_state.current_prompt["verification"])}
</Verification>

<Constraints>
{format_list_items(st.session_state.current_prompt["constraints"])}
</Constraints>

<Output Format>
{st.session_state.current_prompt["output_format"]}
</Output Format>
"""
    return prompt_text

def format_list_items(items_list):
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items_list)])

def add_instruction():
    if st.session_state.new_instruction:
        st.session_state.current_prompt["instructions"].append(st.session_state.new_instruction)
        st.session_state.new_instruction = ""

def update_instruction():
    if st.session_state.editing_instruction_index >= 0:
        st.session_state.current_prompt["instructions"][st.session_state.editing_instruction_index] = st.session_state.edited_instruction
        st.session_state.editing_instruction_index = -1
        st.session_state.edited_instruction = ""

def add_constraint():
    if st.session_state.new_constraint:
        st.session_state.current_prompt["constraints"].append(st.session_state.new_constraint)
        st.session_state.new_constraint = ""

def update_constraint():
    if st.session_state.editing_constraint_index >= 0:
        st.session_state.current_prompt["constraints"][st.session_state.editing_constraint_index] = st.session_state.edited_constraint
        st.session_state.editing_constraint_index = -1
        st.session_state.edited_constraint = ""

def add_verification():
    if st.session_state.new_verification:
        st.session_state.current_prompt["verification"].append(st.session_state.new_verification)
        st.session_state.new_verification = ""

def update_verification():
    if st.session_state.editing_verification_index >= 0:
        st.session_state.current_prompt["verification"][st.session_state.editing_verification_index] = st.session_state.edited_verification
        st.session_state.editing_verification_index = -1
        st.session_state.edited_verification = ""

def load_prompt(index):
    st.session_state.current_prompt = st.session_state.prompts[index].copy()

def delete_prompt(index):
    st.session_state.prompts.pop(index)
    st.success("Prompt deleted successfully!")

# Sidebar for navigation
st.sidebar.title("AI Prompt Creator")
st.sidebar.image("https://via.placeholder.com/150x100.png?text=AI+Prompt", use_column_width=True)

menu = st.sidebar.radio("Navigation", ["Create Prompt", "My Prompts", "About"])

# About section
if menu == "About":
    st.title("About AI Prompt Creator")
    
    st.markdown("""
    ## What is AI Prompt Creator?
    
    AI Prompt Creator is a tool designed to help you create well-structured, effective prompts for AI systems.
    Whether you're working with ChatGPT, Claude, or other AI models, this tool will help you craft prompts
    that minimize hallucinations and maximize accurate, helpful responses.
    
    ## How to use this tool
    
    1. **Create a new prompt**: Define the AI's role, context, instructions, constraints, and output format
    2. **Add verification mechanisms**: Include ways for the AI to handle uncertainty or verify information
    3. **Save your prompts**: Store them for future use and reference
    4. **Export prompts**: Copy the formatted prompt for use with your preferred AI system
    
    ## Key components of an effective prompt
    
    - **Role**: Define what the AI should act as
    - **Context**: Provide necessary background information
    - **Instructions**: Clear steps for the AI to follow
    - **Verification**: Methods to ensure accuracy and handle uncertainty
    - **Constraints**: Boundaries to keep the AI on track
    - **Output Format**: How the response should be structured
    """)

# My Prompts section
elif menu == "My Prompts":
    st.title("My Prompts")
    
    if not st.session_state.prompts:
        st.info("You haven't created any prompts yet. Go to 'Create Prompt' to get started.")
    else:
        # Create a pandas DataFrame from the prompts for better display
        prompts_df = pd.DataFrame([{
            "Name": p["name"],
            "Role": p["role"][:30] + "..." if len(p["role"]) > 30 else p["role"],
            "Created": p["created_at"],
            "Instructions": len(p["instructions"]),
            "Constraints": len(p["constraints"])
        } for p in st.session_state.prompts])
        
        st.dataframe(prompts_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_index = st.selectbox("Select a prompt to view or edit:", 
                                       range(len(st.session_state.prompts)),
                                       format_func=lambda i: st.session_state.prompts[i]["name"])
        
        with col2:
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                if st.button("Load for Editing", key="load_btn"):
                    load_prompt(selected_index)
                    st.success(f"Loaded '{st.session_state.prompts[selected_index]['name']}' for editing")
            with col2_2:
                if st.button("Delete", key="delete_btn", type="primary"):
                    delete_prompt(selected_index)
        
        if selected_index is not None:
            with st.expander("Preview Prompt"):
                st.session_state.current_prompt = st.session_state.prompts[selected_index].copy()
                st.code(export_prompt(), language="markdown")

# Create Prompt section
else:  # Create Prompt is the default
    st.title("Create an AI Prompt")
    
    # Prompt Basics
    with st.container():
        st.subheader("Prompt Basics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.current_prompt["name"] = st.text_input(
                "Prompt Name",
                value=st.session_state.current_prompt["name"],
                help="Give your prompt a descriptive name"
            )
        
        # AI System Role
        st.session_state.current_prompt["role"] = st.text_area(
            "AI System Role",
            value=st.session_state.current_prompt["role"],
            height=100,
            help="Define what the AI should act as (e.g., 'You are an Expert Essay Writer specialized in academic content...')",
            placeholder="Example: You are an Expert Data Analyst who excels at interpreting complex datasets..."
        )
        
        # Context
        st.session_state.current_prompt["context"] = st.text_area(
            "Context",
            value=st.session_state.current_prompt["context"],
            height=100,
            help="Provide necessary background information",
            placeholder="Example: The user will provide sales data that needs to be analyzed for trends and insights..."
        )
    
    # Instructions
    with st.container():
        st.subheader("Instructions")
        st.caption("Add step-by-step guidance for the AI to follow")
        
        # Display current instructions
        if st.session_state.current_prompt["instructions"]:
            for i, instruction in enumerate(st.session_state.current_prompt["instructions"]):
                cols = st.columns([0.8, 0.1, 0.1])
                with cols[0]:
                    st.markdown(f"**{i+1}.** {instruction}")
                with cols[1]:
                    if st.button("Edit", key=f"edit_instr_{i}"):
                        st.session_state.editing_instruction_index = i
                        st.session_state.edited_instruction = instruction
                with cols[2]:
                    if st.button("Delete", key=f"del_instr_{i}"):
                        st.session_state.current_prompt["instructions"].pop(i)
                        st.rerun()
        
        # Edit existing instruction
        if st.session_state.editing_instruction_index >= 0:
            st.text_input("Edit instruction", key="edited_instruction", 
                        on_change=update_instruction)
        
        # Add new instruction
        st.text_input("Add a new instruction", key="new_instruction", 
                    on_change=add_instruction,
                    placeholder="Example: Analyze the data to identify top 3 trends...")
    
    # Verification Mechanisms
    with st.container():
        st.subheader("Verification Mechanisms")
        st.caption("Add methods to ensure accuracy and handle uncertainty")
        
        # Display current verification mechanisms
        if st.session_state.current_prompt["verification"]:
            for i, verification in enumerate(st.session_state.current_prompt["verification"]):
                cols = st.columns([0.8, 0.1, 0.1])
                with cols[0]:
                    st.markdown(f"**{i+1}.** {verification}")
                with cols[1]:
                    if st.button("Edit", key=f"edit_ver_{i}"):
                        st.session_state.editing_verification_index = i
                        st.session_state.edited_verification = verification
                with cols[2]:
                    if st.button("Delete", key=f"del_ver_{i}"):
                        st.session_state.current_prompt["verification"].pop(i)
                        st.rerun()
        
        # Edit existing verification
        if st.session_state.editing_verification_index >= 0:
            st.text_input("Edit verification mechanism", key="edited_verification", 
                        on_change=update_verification)
        
        # Add new verification
        st.text_input("Add a new verification mechanism", key="new_verification", 
                    on_change=add_verification,
                    placeholder="Example: If uncertain about a fact, explicitly state the limitation...")
    
    # Constraints
    with st.container():
        st.subheader("Constraints")
        st.caption("Add boundaries to keep the AI on track")
        
        # Display current constraints
        if st.session_state.current_prompt["constraints"]:
            for i, constraint in enumerate(st.session_state.current_prompt["constraints"]):
                cols = st.columns([0.8, 0.1, 0.1])
                with cols[0]:
                    st.markdown(f"**{i+1}.** {constraint}")
                with cols[1]:
                    if st.button("Edit", key=f"edit_con_{i}"):
                        st.session_state.editing_constraint_index = i
                        st.session_state.edited_constraint = constraint
                with cols[2]:
                    if st.button("Delete", key=f"del_con_{i}"):
                        st.session_state.current_prompt["constraints"].pop(i)
                        st.rerun()
        
        # Edit existing constraint
        if st.session_state.editing_constraint_index >= 0:
            st.text_input("Edit constraint", key="edited_constraint", 
                        on_change=update_constraint)
        
        # Add new constraint
        st.text_input("Add a new constraint", key="new_constraint", 
                    on_change=add_constraint,
                    placeholder="Example: Limit response to 3-5 paragraphs...")
    
    # Output Format
    with st.container():
        st.subheader("Output Format")
        st.caption("Define how the AI's response should be structured")
        
        st.session_state.current_prompt["output_format"] = st.text_area(
            "Output Format",
            value=st.session_state.current_prompt["output_format"],
            height=100,
            help="How the response should be structured",
            placeholder="Example:\n1. Summary of Findings\n2. Detailed Analysis\n   a. Trend 1\n   b. Trend 2\n3. Recommendations"
        )
    
    # Preview and save buttons
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Save Prompt", type="primary"):
                save_prompt()
        
        with col2:
            if st.button("Preview Prompt"):
                preview_text = export_prompt()
                st.code(preview_text, language="markdown")
                
                # Add a copy button
                st.text_area("Copy this prompt", value=preview_text, height=100)
                st.caption("Copy the above text to use with your preferred AI system")

# Add a footer
st.sidebar.markdown("---")
st.sidebar.caption("AI Prompt Creator v1.0")
st.sidebar.caption("© 2025 Prompt Engineering Tools")
