from graph import graph


state = {
    "messages": [
    "I dropped out after Class 10."
],
    "status": "",
    "student_class": "",
    "country": "",
    "interests": [],
    "stream": "",
    "response": ""
}

result = graph.invoke(state)

print("\n===== FINAL STATE =====\n")

for key, value in result.items():
    print(f"{key}: {value}")