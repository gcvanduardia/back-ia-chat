import openai
import time

# Configura la clave de la API y crea el asistente una vez
openai.api_key = ''
assistant = openai.beta.assistants.create(
    name="botIA NOW",
    instructions='tu eres un analista de comentarios de las diferentes campañas en redes sociales del banco Davivienda. Los comentarios en redes sociales son: [{ "Date": "2024-02-01 02:24:26", "Likes": 21, "titulovideo": "banco de bogota", "Comment": "yo pagué un libre inversion de una ...uno encima de otro antes de tiempo. Pensé que me darian otro, y salió Negado!", "Concatenado": "Likes: 21.0. Video: banco de bogota. Comentario: yo pagué un libre inversion de una ...uno encima de otro antes de tiempo. Pensé que me darian otro, y salió Negado!", "label": "negative", "score": 0.463238388299942 }, { "Date": "2024-02-01 02:25:33", "Likes": 6, "titulovideo": "banco de bogota", "Comment": "los intereses son demasiados altos", "Concatenado": "Likes: 6.0. Video: banco de bogota. Comentario: los intereses son demasiados altos", "label": "positive", "score": 0.5316643118858337 }, { "Date": "2024-02-01 04:02:10", "Likes": 2, "titulovideo": "banco de bogota", "Comment": "cule hueso de credito un encarte", "Concatenado": "Likes: 2.0. Video: banco de bogota. Comentario: cule hueso de credito un encarte", "label": "positive", "score": 0.5693753957748413 }, { "Date": "2024-02-01 04:20:00", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "Que lindooooo 💕", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: Que lindooooo 💕", "label": "positive", "score": 0.6735376119613647 }, { "Date": "2024-02-01 04:24:58", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "😂😂😂😂 si son. los toderos", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: 😂😂😂😂 si son. los toderos", "label": "positive", "score": 0.5060659050941467 }, { "Date": "2024-02-01 04:32:13", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "😁😁😁", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: 😁😁😁", "label": "none", "score": 0 }, { "Date": "2024-02-01 17:04:54", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "yo saqué uno de 2400 lo pagué antes de tiempo y fuy a sacar otro más alto me lo negaron quede 🫤🫤", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: yo saqué uno de 2400 lo pagué antes de tiempo y fuy a sacar otro más alto me lo negaron quede 🫤🫤", "label": "negative", "score": 0.4506146013736725 }, { "Date": "2024-02-01 18:17:30", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "busque otro muy alta las tasas", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: busque otro muy alta las tasas", "label": "positive", "score": 0.5770710706710815 }, { "Date": "2024-02-01 18:26:17", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "yo tengo un crédito actualmente con ustedes , puedo adquirir otro de menor valor ?", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: yo tengo un crédito actualmente con ustedes , puedo adquirir otro de menor valor ?", "label": "positive", "score": 0.5156042575836182 }, { "Date": "2024-02-02 02:47:58", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "Se verda", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: Se verda", "label": "positive", "score": 0.5861639976501465 }, { "Date": "2024-02-02 21:37:06", "Likes": 9, "titulovideo": "banco de bogota", "Comment": "Creo que a todos nos pasó igual que pagamos para que nos prestaran más y nada 😅😅😅", "Concatenado": "Likes: 9.0. Video: banco de bogota. Comentario: Creo que a todos nos pasó igual que pagamos para que nos prestaran más y nada 😅😅😅", "label": "positive", "score": 0.3593667149543762 }, { "Date": "2024-02-03 02:36:26", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "🥰😌", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: 🥰😌", "label": "none", "score": 0 }, { "Date": "2024-02-04 01:03:42", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "solicito libre inversión", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: solicito libre inversión", "label": "positive", "score": 0.6450059413909912 }, { "Date": "2024-02-07 11:19:27", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "eso no es tan fácil", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: eso no es tan fácil", "label": "negative", "score": 0.5120848417282104 }, { "Date": "2024-02-10 19:24:09", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "De lo peorsito es tener cuenta en este banco...", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: De lo peorsito es tener cuenta en este banco...", "label": "negative", "score": 0.6209278702735901 }, { "Date": "2024-02-12 02:49:15", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "🥰🥰", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: 🥰🥰", "label": "none", "score": 0 }, { "Date": "2024-02-12 14:09:12", "Likes": 21, "titulovideo": "banco de bogota", "Comment": "Son muy altos los intereses, adicional sí o sí debes ir a una oficina física para el desembolso.", "Concatenado": "Likes: 21.0. Video: banco de bogota. Comentario: Son muy altos los intereses, adicional sí o sí debes ir a una oficina física para el desembolso.", "label": "positive", "score": 0.6193567514419556 }, { "Date": "2024-02-13 18:59:16", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "astetik", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: astetik", "label": "positive", "score": 0.5887712836265564 }, { "Date": "2024-02-13 20:36:28", "Likes": 39, "titulovideo": "banco de bogota", "Comment": "pa que si me lo van a negar", "Concatenado": "Likes: 39.0. Video: banco de bogota. Comentario: pa que si me lo van a negar", "label": "positive", "score": 0.4436931312084198 }, { "Date": "2024-02-15 14:41:34", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "me lo negaron ☠️", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: me lo negaron ☠️", "label": "negative", "score": 0.4506908655166626 }, { "Date": "2024-02-17 22:21:59", "Likes": 19, "titulovideo": "banco de bogota", "Comment": "Yo lo pedí y con eso me fui del país, gracias algún día me regresaré a pagar", "Concatenado": "Likes: 19.0. Video: banco de bogota. Comentario: Yo lo pedí y con eso me fui del país, gracias algún día me regresaré a pagar", "label": "negative", "score": 0.7099689841270447 }, { "Date": "2024-02-19 14:34:53", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "uiii no ... mala experiencia con el banco de Bogotá 😔", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: uiii no ... mala experiencia con el banco de Bogotá 😔", "label": "negative", "score": 0.5879213213920593 }, { "Date": "2024-02-19 19:42:17", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "Extraño a hange", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: Extraño a hange", "label": "positive", "score": 0.5790324807167053 }, { "Date": "2024-02-20 13:19:53", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "yo quiero", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: yo quiero", "label": "positive", "score": 0.605292558670044 }, { "Date": "2024-02-20 17:07:19", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "siempre lo niegan ajjaja", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: siempre lo niegan ajjaja", "label": "positive", "score": 0.4850721061229706 }, { "Date": "2024-02-20 22:41:59", "Likes": 2, "titulovideo": "banco de bogota", "Comment": "yo pagué 8 millones x 5 y media", "Concatenado": "Likes: 2.0. Video: banco de bogota. Comentario: yo pagué 8 millones x 5 y media", "label": "positive", "score": 0.5905088186264038 }, { "Date": "2024-02-20 22:46:54", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "fui y me mo le negaron 😅", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: fui y me mo le negaron 😅", "label": "positive", "score": 0.478059858083725 }, { "Date": "2024-02-21 02:40:18", "Likes": 11, "titulovideo": "banco de bogota", "Comment": "😂😂 no le vendan el alma, hoy pague uno que saqué hace 5 meses, pedi 3 millones, me desembolsaron 2.8, la deuda quedo en 3.600 y en 5 meses pague 3.900", "Concatenado": "Likes: 11.0. Video: banco de bogota. Comentario: 😂😂 no le vendan el alma, hoy pague uno que saqué hace 5 meses, pedi 3 millones, me desembolsaron 2.8, la deuda quedo en 3.600 y en 5 meses pague 3.900", "label": "negative", "score": 0.627281129360199 }, { "Date": "2024-02-21 04:26:43", "Likes": 1, "titulovideo": "banco de bogota", "Comment": "Ami por 17 millones pago 32 millones no es justo no lo coji", "Concatenado": "Likes: 1.0. Video: banco de bogota. Comentario: Ami por 17 millones pago 32 millones no es justo no lo coji", "label": "positive", "score": 0.5041801929473877 }, { "Date": "2024-02-21 20:50:38", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "Niegan todo crédito, exigen muchas garantías y si aprueban algo es un chiste lo que aprueban", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: Niegan todo crédito, exigen muchas garantías y si aprueban algo es un chiste lo que aprueban", "label": "positive", "score": 0.3865340650081635 }, { "Date": "2024-02-22 00:31:32", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "(\\_\/)(•_•)\/> 🍏", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: (\\_\/)(•_•)\/> 🍏", "label": "positive", "score": 0.5722740888595581 }, { "Date": "2024-02-22 00:57:11", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "🥰🥰🥰🥰", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: 🥰🥰🥰🥰", "label": "positive", "score": 0.6483306288719177 }, { "Date": "2024-02-22 02:48:35", "Likes": 0, "titulovideo": "banco de bogota", "Comment": "pura bulla y trámite para salir con q no lo van a dar 😡😡😡", "Concatenado": "Likes: 0.0. Video: banco de bogota. Comentario: pura bulla y trámite para salir con q no lo van a dar 😡😡😡", "label": "negative", "score": 0.5936237573623657 }]',
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o"
)

# Crea un hilo una vez
thread = openai.beta.threads.create()

def get_openai_response(content):
    print('***** openai input: ')
    print(content)

    # Crea un mensaje en el hilo existente
    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

    # Crea una ejecución en el hilo existente
    run = openai.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id
    )

    # Espera a que la ejecución se complete
    while True:
        run = openai.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
        )
        print(run.status)
        if run.status == 'completed':
            break
        time.sleep(1)

    # Recupera los mensajes del hilo
    messages = openai.beta.threads.messages.list(
      thread_id=thread.id
    )

    # Obtiene el último mensaje
    last_message = messages.data[0]
    role = last_message.role.capitalize()
    content = last_message.content[0].text.value  
    created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_message.created_at))

    response = content

    print('***** openai response: ')
    print(response)
    
    return response