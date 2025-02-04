from openai import OpenAI

def start_conversation(api_key):
    client = OpenAI(api_key=api_key)  # Move this inside the function

    print("Starting conversation with Gym Buddy! Type 'exit' to end.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Ending conversation. Goodbye!")
            break

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful gym assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        assistant_reply = response.choices[0].message.content
        print("Gym Buddy:", assistant_reply)
