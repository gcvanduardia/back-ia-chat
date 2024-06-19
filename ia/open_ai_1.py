from dotenv import load_dotenv
import os
import openai
import time
import json
from datetime import datetime
import tracemalloc
from .functions_openai import get_general_report, report_by_week, report_by_region, report_by_region_and_week, comments_analysis

load_dotenv()
tracemalloc.start()

openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
""" thread_id = os.getenv("THREAD_ID") """
thread = openai.beta.threads.create()
thread_id = thread.id

print('assistant_id: ', assistant_id)
print('thread_id: ', thread_id)

def submit_tool(run, tool, result):
    print("*****Submitting tool outputs.")
    tool_outputs = [{
        "tool_call_id": tool.id,
        "output": str(result)
    }]
    try:
        run_end = openai.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
        print("Tool outputs submitted successfully.")
    except Exception as e:
        print("Failed to submit tool outputs:", e)


def handle_detect_function(run):
    print("*****El asistente ha detectado una función:")
    """ print(run.required_action.submit_tool_outputs.tool_calls) """
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    for tool in tool_calls:
        if tool.type == 'function':
            function_name = tool.function.name
            arguments = json.loads(tool.function.arguments)
            print(f"*****Función: {function_name}")
            print(f"*****Argumentos: {arguments}")
            if function_name == 'get_general_report':
                result = get_general_report()
                result_context = result['add_data']
                print(f"Resultado: {result_context}")
                submit_tool(run, tool, result_context)
                return result
            if function_name == 'report_by_week':
                result = report_by_week(arguments['week'])
                result_context = result['add_data']
                print(f"Resultado: {result_context}")
                submit_tool(run, tool, result_context)
                return result
            if function_name == 'report_by_region':
                result = report_by_region(arguments['region'])
                result_context = result['add_data']
                print(f"Resultado: {result_context}")
                submit_tool(run, tool, result_context)
                return result
            if function_name == 'report_by_region_and_week':
                result = report_by_region_and_week(arguments['region'], arguments['week'])
                result_context = result['add_data']
                submit_tool(run, tool, result_context)
                return result
            if function_name == 'comments_report':
                result = comments_analysis(arguments['region'], arguments['week'], arguments['general'])
                result_context = result['add_data']
                print(f"Resultado: {result_context}")
                submit_tool(run, tool, result_context)
                return result
            if function_name == 'competitor_analysis':
                result = 'competitor_analysis'
                result_context = result
                print(f"Resultado: {result_context}")
                submit_tool(run, tool, result_context)
                return result

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
            elif run.status == 'requires_action':
                return handle_detect_function(run)
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
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        body = {
            "user": "Bot",
            "message": """""",
            "date": str(current_date),
            "add_type": "none",
            "messageEnd": response
        }
        
        return body
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Error: El asistente no pudo procesar la solicitud."