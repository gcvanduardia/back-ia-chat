import openai
import time

openai.api_key = ''

assistant = openai.beta.assistants.create(
    name="Cristof",
    instructions="tu eres un analista de datos de la empresa Essilor. Essilor es una compañía francesa que produce lentes oftálmicas además de equipamiento óptico. Está situada en París, Francia, y cotiza en la Bolsa Euronext de París.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-0125-preview"
)

thread = openai.beta.threads.create()

message = openai.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="quiero que me des un resumen de los comentarios de los vendedores, identifica topicos relevantes" + "Asunto: Visita comercial. Comentarios: Se revisa caso y cambios se refuerza en toma de medidas.. Resultado: Se hace visita al punto de venta se habla con asesora este mes no ha vendido nada de servi las ventas estan bajas no hay agendas llenas. Tuvo inconveniente con pte de BI FF Asunto: Visita comercial. Comentarios: Se revisa inconveniente con NOW. pedidos estaban saleindo a cod de SURA. Revisamos plataforma el codigo esta OK. Se escala caso a Agencia.. Resultado: Visita rn pubto de venta se habla con asesores refurrzo en ventas se informa fin de promo trans term y tallado Asunto: TFV. Comentarios: REALIZAR TRABAJO DE OFICINA Asunto: Visita comercial. Comentarios: Subieron los lentes desde la primer semana de Enero. Quedaron muy altos el VPhysio esta igual al VXR en precio.. Resultado: Se habla con Dra lina sobrr porducto linea Varilux refuerzo en Varilux XR Asunto: Visita comercial. Comentarios: La Dra comenzo hoy las ventas estan bajas no han salido ptes para lentes. Resultado: Visita a asesora informacion de promos trans NOW que finalizan Asunto: Visita comercial. Comentarios: Refuerzo producto y formulación de producto Shammir. Cobro de cartera hay una fact de mas de 1 mes respobde que ya pago se solicita me envie soporte. Resultado: Visita a Dr Jurado Asunto: Visita comercial. Comentarios: SE REALIZA VISITA COMERCIAL ENTREGA DE MATERIAL POP Y REFUERZO DE PROMOCIONES. Resultado: SE REALIZA VISITA COMERCIAL ENTREGA DE MATERIAL POP Y REFUERZO DE PROMOCIONES Asunto: Visita comercial. Comentarios: Se revisa caso de paciente de Jardin se debe cambiar altura. Resultado: Se habla con Dra karen se hace refuerzo en Varilux y formulacion Asunto: Visita comercial. Comentarios: Me presenta con la nueva administradora. Se habla con Nataly se entrega LP actual la nueva sale en 2 meses. Se presenta portafolio. Esta recien llegando quiere nueva cita para organizar agenda de capacitaciones. Resultado: Visita a punto de venta el Dr esta ocupado Asunto: Visita comercial. Comentarios: SE REALIZA VISITA COMERCIAL ENTREGA DE MATERIAL POP Y REFUERZO DE PROMOCIONES. Resultado: SE REALIZA VISITA COMERCIAL ENTREGA DE MATERIAL POP Y REFUERZO DE PROMOCIONES Asunto: Visita comercial. Comentarios: SE REALIZA VISITA COMERCIAL ENTREGA DE MATERIAL POP Y REFUERZO DE PROMOCIONES. Resultado: SE REALIZA VISITA COMERCIAL ENTREGA DE MATERIAL POP Y REFUERZO DE PROMOCIONES"
)

run = openai.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Diríjase al usuario como David. El usuario es un gerente regional."
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

for message in messages.data:
    role = message.role.capitalize()
    content = message.content[0].text.value  
    created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message.created_at))
    print(f"Rol: {role}\nFecha: {created_at}\nMensaje: {content}\n{'-'*60}")