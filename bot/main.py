from bot.foodbot import graph

# ✅ Stream chatbot updates
def stream_graph_updates(user_input: str):
    """Streams chatbot responses."""
    messages = [{"role": "system", "content": "Always respond in English. Do not use any other language."}]
    messages.append({"role": "user", "content": user_input})
    
    for event in graph.stream({"messages": messages}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

# # ✅ Start Chatbot
print("\n🤖 Chatbot is ready! Type 'exit', 'quit', or 'bye' to stop.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input)