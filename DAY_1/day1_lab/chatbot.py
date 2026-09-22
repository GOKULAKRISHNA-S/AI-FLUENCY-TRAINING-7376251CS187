from config import client, MODEL, QUESTIONS, banner
 
def chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful college assistant."},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
 
if __name__ == "__main__":
    banner("SYSTEM 1: CHATBOT")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", chatbot(question))
        print("-" * 70)
