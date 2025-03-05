from bot.agent import graph

# ✅ Stream chatbot updates
# def stream_graph_updates(user_input: str):
#     """Streams chatbot responses."""
#     messages = [{"role": "system", "content": "Always respond in English. Do not use any other language."}]
#     messages.append({"role": "user", "content": user_input})
    
#     for event in graph.stream({"messages": messages}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)



def stream_graph_updates(user_input: str) -> str:
    """Streams chatbot responses and returns the final response."""
    messages = [{"role": "system", "content": "Always respond in English. Do not use any other language."}]
    messages.append({"role": "user", "content": user_input})

    final_response = ""  # Initialize empty response string

    for event in graph.stream({"messages": messages}):
        for value in event.values():
            assistant_message = value["messages"][-1].content  # Extract the latest assistant message
            print("Assistant:", assistant_message)  # Debugging print statement

            # Append to the final response
            final_response += assistant_message + " "

    return assistant_message.strip()  # Return cleaned response to display in Streamlit


# # ✅ Start Chatbot
# print("\n🤖 Chatbot is ready! Type 'exit', 'quit', or 'bye' to stop.\n")
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         break
#     stream_graph_updates(user_input)