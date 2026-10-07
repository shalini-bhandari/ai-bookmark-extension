from llm_service import generate_answer


context = """
A POST request is commonly used to create new data.
GET requests are generally used to retrieve data.
"""

question = "Which HTTP method is used to create new data?"


answer = generate_answer(
    question,
    context
)

print(answer)