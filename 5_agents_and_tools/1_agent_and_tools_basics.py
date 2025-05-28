from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


# Define a very simple tool function that returns the current time
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime  # Import datetime module to get current time

    now = datetime.datetime.now()  # Get current time
    return now.strftime("%I:%M %p")  # Format time in H:MM AM/PM format

# Code to generate a secure password
def generate_secure_password(*args, **kwargs):
    import secrets  # Import secrets for secure random generation
    import string  # Import string for character sets
    """Generates a secure password with the specified length and character set."""

    length=12
    use_special_chars=True

    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")

    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += string.punctuation

    # Ensure password has at least one lowercase, one uppercase, one digit, and one special (if enabled)
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
    ]

    if use_special_chars:
        password.append(secrets.choice(string.punctuation))

    # Fill the rest of the password length
    password += [secrets.choice(characters) for _ in range(length - len(password))]

    # Shuffle the password to make it unpredictable
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

# List of tools available to the agent
tools = [
    Tool(
        name="Time",  # Name of the tool
        func=get_current_time,  # Function that the tool will execute
        # Description of the tool
        description="Useful for when you need to know the current time",
    ),
    Tool(
        name="Secure Password Generator",  # Name of the tool
        func=generate_secure_password,  # Function that the tool will execute
        # Description of the tool
        description="Useful for when you need to generate a secure password",
    ),
]

# Pull the prompt template from the hub
# ReAct = Reason and Action
# https://smith.langchain.com/hub/hwchase17/react
prompt = hub.pull("hwchase17/react")

# Initialize a ChatOpenAI model
llm = ChatOpenAI(
    model="gpt-4o", temperature=0
)

# Create the ReAct agent using the create_react_agent function
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True,
)

# Create an agent executor from the agent and tools
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
)

# Run the agent with a test query
response_date = agent_executor.invoke({"input": "What time is it?"})

# Print the response from the agent
print("response:", response_date)

print("####################################################")

# Run the agent with a test query
response_password = agent_executor.invoke({"input": "Can you generate a secure password for me."})

# Print the response from the agent
print("response:", response_password["output"])
# The agent will respond with the generated secure password
# Note: The agent will use the tools defined above to answer the queries.