import openai

#Call GPT AI
def Query_OAPI(prompt):

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        # max_tokens = ,
        messages = [{"role": "user", "content": (prompt)}]
        )

        return (completion.choices[0]['message']['content'])