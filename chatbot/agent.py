from typing import Annotated,List,TypedDict
from langchain_core.messages import AIMessage,HumanMessage,BaseMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from pydantic import BaseModel,Field
from langchain_mcp_adapters.client import MultiServerMCPClient


class is_query_task(BaseModel):
    """To check wether the user is asking to query the task or not"""
    is_query:bool = Field(description="Is the query about the task or not")


class task_state(TypedDict):
    """State for the task management agent"""
    messages:Annotated[List[BaseMessage], add_messages]

llm = ChatOllama(model="gemma4:e2b",reasoning=False,temperature=1)
llm_query_check = llm.with_structured_output(is_query_task)


async def build_task_graph():

    ## initialize client and get the tools
    client = MultiServerMCPClient({
        "task_manager_mcp_client":{
            "url":"http://localhost:8000/mcp",
            "transport":"sse"
        }
    })

    tools = await client.get_tools()
    llm_withtools = llm.bind_tools(tools)

    ## Function to check if query is about the task
    def check_query(state:task_state):
        response = llm_query_check.invoke(
            [
                SystemMessage(content="Determine if the request is about managing, viewing, creating, updating, or deleting tasks."),
                HumanMessage(content=state["messages"][-1].content)
            ]
        )
        print(f"The response is : {response.is_query}")
        if response.is_query:
            return "f_task_agent"
        else:
            return "f_fallback"

    
    ## Function to check if should have tool call or not

    def tool_call_required(state:task_state):
        last_msg = state["messages"][-1]

        if last_msg.tool_calls:
            return "tools"

        return END


    ## node to create f_task_agent

    def f_task_agent(state:task_state):
        response = llm_withtools.invoke(state["messages"])
        return {"messages":[response]}

    ## node to create f_fallback
    def f_fallback(state:task_state):
        response = AIMessage(content="I am a dedicated Task Assistant. I can only assist you with task-related queries such as viewing, creating, updating, or deleting tasks.")
        return {"messages":[response]}

    ## node to tool calls
    f_tool_node = ToolNode(tools)

    ## build graph
    graph_builder = StateGraph(task_state)

    ## add nodes
    graph_builder.add_node("n_task_agent",f_task_agent)
    graph_builder.add_node("n_fallback",f_fallback)
    graph_builder.add_node("tools",f_tool_node)

    ## add edges
    graph_builder.add_conditional_edges(
        START,
        check_query,
        {
            "f_task_agent":"n_task_agent",
            "f_fallback":"n_fallback"
        }
    )

    graph_builder.add_conditional_edges(
        "n_task_agent",
        tool_call_required,
        ["tools",END]
    )

    graph_builder.add_edge("tools","n_task_agent")
    graph_builder.add_edge("n_fallback",END)
    checkpointer = InMemorySaver()
    return graph_builder.compile(checkpointer=checkpointer)

    




