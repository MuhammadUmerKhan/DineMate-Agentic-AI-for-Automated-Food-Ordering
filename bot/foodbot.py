import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langchain.tools import Tool
from tools.agent_tools import *
from config import GROK_API_KEY

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize the LLM
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=GROK_API_KEY,
    model_name="qwen-2.5-32b"
)

# ✅ Define a TypedDict to store chat messages
class State(TypedDict):
    messages: Annotated[list, add_messages]


tools = [
    Tool(
        name="Greet",
        func=lambda _: "👋 Hello! Welcome to our restaurant! 🍽️ How can I assist you today? Would you like to see the menu?",
        description="Warmly greet the user and offer assistance."
    ),
    Tool(
        name="Goodbye",
        func=lambda _: "👋 Goodbye! Thank you for visiting! Hope to serve you again soon. 🍽️ Have a great day!",
        description="Politely say goodbye to the user."
    ),
    Tool(
        name="Show Menu", 
        func=show_menu, 
        description="Fetch and display the menu items."
    ),
    Tool(
        name="Take Order",
        func=take_order,
        description="Add items to your order. Use this JSON format only: {'item': quantity}."
    ),
    Tool(
        name="Remove Item", 
        func=remove_item, 
        description="Remove an item from your order."
    ),
    Tool(
        name="Update Item Quantity", 
        func=update_item, 
        description="Update the quantity of an existing item in your order. Use JSON format: `{'item': quantity}`."
    ),
    Tool(
        name="Total Price",
        func=total_price, 
        description="Calculate the total price of ordered items."
    ),
    Tool(
        name="Check Order Items", 
        func=check_order_items, 
        description="View all items currently in your order."
    ),
    Tool(
        name="Track Order",
        func=check_order_status,
        description="Check your order status and estimated delivery time."
        ),
    Tool(
        name="Confirm Order", 
        func=confirm_order, 
        description="Confirm or Place or Deliver your order for processing."
    ),
    Tool(
        name="Cancel Order before confirmation",
        func=cancel_order_before_confirmation,
        description="Cancel the current order and clear all items. Cancel order before placing order"
    ),
    Tool(
        name="Replace Item",
        func=replace_item,
        description="Replace an item in the order while keeping the same quantity and updating the total price. "
                    "Use structured format: [(old_item, new_item), (old_item, new_item), ...]"
    ),
    Tool(
        name="Cancel Order after confirmation",
        func=cancel_order_after_confirmation,
        description="Cancel an order after confirmation using an Order ID. This is only possible within 20 minutes of order placement."
    ),
    Tool(
        name="Estimated Delivery Time",
        func=estimated_delivery_time,
        description="Check the estimated delivery time of your order based on when it was placed using order ID."
    ),
    Tool(
        name="Modify Order after confirmation",
        func=modify_order_after_confirmation,
        description="Modify an order after confirmation using an Order ID. This is only possible before food preparation starts."
                    "Use JSON: {'order_id': 1, 'updated_items': {'item': quantity}}"
    ),
]

# ✅ Define Tool Execution Class
class ToolExecutor:
    """✅ Handles tool execution when called by the LLM."""
    
    def __init__(self, tools: list):
        self.tools_by_name = {tool.name: tool for tool in tools}
    
    def __call__(self, state: State):
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message or not hasattr(last_message, "tool_calls"):
            return {"messages": messages}
        
        tool_results = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name in self.tools_by_name:
                tool_result = self.tools_by_name[tool_name].invoke(tool_args)
                tool_results.append(ToolMessage(
                    content=json.dumps(tool_result),
                    tool=tool_name,
                    tool_call_id=tool_call["id"]
                ))
        
        return {"messages": messages + tool_results}

# ✅ Define Routing Function
def route_tools(state: State):
    """✅ Routes the flow based on whether tools are required."""
    messages = state.get("messages", [])
    
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    
    return END

# ✅ Build the LangGraph Chatbot Flow
graph_builder = StateGraph(State)
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    """✅ Handles AI response and tool calling."""
    ai_response = llm_with_tools.invoke(state["messages"])
    return {"messages": [ai_response]}

# ✅ Add nodes to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolExecutor(tools))

# ✅ Define edges (flow)
graph_builder.add_conditional_edges("chatbot", route_tools, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "chatbot")  # ✅ Return to chatbot after tool execution
graph_builder.add_edge(START, "chatbot")

# ✅ Compile the graph
graph = graph_builder.compile()