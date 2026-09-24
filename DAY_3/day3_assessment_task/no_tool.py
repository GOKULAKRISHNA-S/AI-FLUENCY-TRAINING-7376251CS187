from config import client, MODEL


question = input("Enter your travel question: ")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful travel assistant."
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

print("\nLLM Answer:")
print(response.choices[0].message.content)