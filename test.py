from Tools.Gmail_sending_tool import send_email


result = send_email.invoke({
    "to": "charifisaad123@gmail.com",
    "subject": "Test Gmail Tool",
    "body": "Hello, this is a test from my Agentic AI system.",
})

print(result)