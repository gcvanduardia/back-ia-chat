import openai
import time

def get_openai_response(content):

    print('***** openai input: ')
    print(content)

    openai.api_key = ''

    assistant = openai.beta.assistants.create(
        name="botIA",
        instructions="tu eres un analista de comentarios de las diferentes campañas en redes sociales del banco Davivienda.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-0125-preview"
    )

    thread = openai.beta.threads.create()

    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

    run = openai.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions="Diríjase al usuario como Juan. El usuario es un gerente regional."
    )
    while True:
        run = openai.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
        )
        print(run.status)
        if run.status == 'completed':
            break
        time.sleep(1)

    messages = openai.beta.threads.messages.list(
      thread_id=thread.id
    )

    last_message = messages.data[0]
    role = last_message.role.capitalize()
    content = last_message.content[0].text.value  
    created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_message.created_at))

    response = content

    print('***** openai response: ')
    print(response)
    
    return response
