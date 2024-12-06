import streamlit as st
import os

# Agent and LLM
from langchain import LLMChain
from langchain_community.llms import OpenAI

# Memory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory

# Tools
from langchain_community.utilities import GoogleSerperAPIWrapper
# Certifique-se de que o EventbriteAPIWrapper está disponível em outra biblioteca ou crie sua própria integração.

from langchain.agents import AgentExecutor, Tool, ConversationalAgent

st.title('Smart Event Planner')

# Set API Keys
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")
EVENTBRITE_API_KEY = os.environ["EVENTBRITE_API_KEY"]
OPENAI_KEY = os.environ['OPENAI_KEY']

# Initialize tools
search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)

# Verificar existência do Eventbrite API Wrapper
try:
    from langchain_community.utilities import EventbriteAPIWrapper
    events = EventbriteAPIWrapper(eventbrite_api_key=EVENTBRITE_API_KEY)
except ImportError:
    events = None

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to get current, up-to-date answers.",
    ),
]

if events:
    tools.append(
        Tool(
            name="Events",
            func=events.run,
            description="Useful for finding events, shows, or activities in a city on a specific date.",
        )
    )

# Define Chat Prompt
prefix = """You are a friendly modern-day event planner.
You can help users find events, activities, or shows in a given city 
based on their preferences and the date.
If the user dont ask something near to a questions involve this cases, return for him somenthing like 'I am not programmed to do this, lets try talk about events?'
You have access to the following tools:
"""

suffix = """
Chat History:
{chat_history}
Latest Question: {input}
{agent_scratchpad}
"""

from langchain.agents import ConversationalAgent

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
from langchain_community.chat_models import ChatOpenAI

llm_chain = LLMChain(
    llm=ChatOpenAI(temperature=0.8, model_name="gpt-4",api_key=OPENAI_KEY),
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

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Streamlit UI
st.subheader("Ask your event planner!")
user_input = st.text_input("What do you want to plan? (e.g., 'Find shows in Porto Alegre tomorrow')")

if user_input:
    with st.spinner("Fetching information..."):
        try:
            response = agent_executor.run(user_input)
            st.write("DEBUG: Response received", response)
        except Exception as e:
            st.error(f"Erro ao executar o agente: {e}")
            response = None
    if response:
        st.success("Here's what I found:")
        st.write(response)
    else:
        st.warning("O agente não retornou nenhum dado. Tente outra consulta.")