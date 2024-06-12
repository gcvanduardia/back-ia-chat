from dotenv import load_dotenv
import os
import openai
import time

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
thread_id = os.getenv("THREAD_ID")
""" thread = openai.beta.threads.create()
thread_id = thread.id """

print('assistant_id: ', assistant_id)
print('thread_id: ', thread_id)

def get_openai_response(content):
    
    print('***** openai input: ')
    print(content)

    try:
        message = openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        max_retries = 5
        retries = 0

        while True:
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            print(run.status)
            
            if run.status == 'completed':
                break
            elif run.status == 'failed':
                retries += 1
                if retries >= max_retries:
                    raise Exception("El proceso ha fallado repetidamente y no responde.")
                time.sleep(1)
                run = openai.beta.threads.runs.create(
                    thread_id=thread_id,
                    assistant_id=assistant_id
                )
            else:
                time.sleep(1)

        messages = openai.beta.threads.messages.list(
            thread_id=thread_id
        )

        last_message = messages.data[0]
        role = last_message.role.capitalize()
        content = last_message.content[0].text.value  
        created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_message.created_at))

        response = content

        print('***** openai response: ')
        print(response)
        
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Error: El asistente no pudo procesar la solicitud."