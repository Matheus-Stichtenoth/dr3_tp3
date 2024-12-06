import streamlit as st
import os

# Agent and LLM
from langchain import LLMChain, OpenAI
from langchain.agents import AgentExecutor, Tool, ConversationalAgent
from langchain_community.chat_models import ChatOpenAI

# Memory
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

# Tools
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.utilities import EventbriteAPIWrapper

st.title('Smart Event Planner')

# Set API Keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")

# Initialize tools
search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
events = EventbriteAPIWrapper(eventbrite_api_key=EVENTBRITE_API_KEY)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to get current, up-to-date answers.",
    ),
    Tool(
        name="Events",
        func=events.run,
        description="Useful for finding events, shows, or activities in a city on a specific date.",
    )
]

# Define Chat Prompt
prefix = """You are a friendly modern-day event planner.
You can help users find events, activities, or shows in a given city 
based on their preferences and the date.
You have access to the following tools:
"""

suffix = """
Chat History:
{chat_history}
Latest Question: {input}
{agent_scratchpad}
"""

prompt = ConversationalAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

# Set Memory
msg = StreamlitChatMessageHistory()

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        messages=msg,
        memory_key="chat_history",
        return_messages=True
    )
    
memory = st.session_state.memory

# Set Agent
llm_chain = LLMChain(
    llm=ChatOpenAI(temperature=0.8, model_name="gpt-4"),
    prompt=prompt,
    verbose=True
)

agent = ConversationalAgent(
    llm_chain=llm_chain,
    memory=memory,
    verbose=True,
    max_interactions=3,
    tools=tools
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Streamlit UI
st.subheader("Ask your event planner!")
user_input = st.text_input("What do you want to plan? (e.g., 'Find concerts in New York on Friday')")

if user_input:
    with st.spinner("Fetching information..."):
        response = agent_executor.run(user_input)
    st.success("Here's what I found:")
    st.write(response)