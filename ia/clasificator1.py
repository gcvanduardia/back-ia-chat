""" Varilux ,Eyezen ,Transition ,crizal ,Stellest ,Attitude ,Panoramax ,Vx ,Tr ,shamir ,kodak ,alcon ,autograph ,intouch ,Mp ,Marca propia ,futurex ,Easy ,clarity ,ovation ,poli ,antireflejo ,luz azul ,Vision sencilla ,Terminados ,Tallados ,AR ,Doble estilo ,fulljob ,NOW ,toricos ,stock ,LC ,promo ,promocion ,CAMPAÑA ,garantia ,cortesia ,pedido ,agencia ,cartera ,transferencia ,Hoya ,zeiss ,Labocosta ,Visionlab ,Megalens ,Restrepo ,paciente ,medidas ,formula ,precio ,politica ,LP """
from transformers import pipeline

pipe = pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2")

question = "¿Cuál de las siguientes palabras es mencionada: Varilux ,Eyezen ,Transition ,crizal ,Stellest ,Attitude ,Panoramax ,Vx ,Tr ,shamir ,kodak ,alcon ,autograph ,intouch ,Mp ,Marca propia ,futurex ,Easy ,clarity ,ovation ,poli ,antireflejo ,luz azul?"
context = "Vendedor: CLAUDIA EDITH OLAVE PINZON. Asunto: Visita comercial. Comentarios: Se refuerza portafolio essilor en progresivos dando a conocer las carcajadas más relevantes y beneficios de cada producto dando tips de venta para la rotación de promociones y se recuerda los lentes para niños digitales se ayudar con trabajo de panoramax del 10 para cierre de venta. Resultado: traer los progresivos con kit de herramientas incluir cliente de realizar capacitación de Stellest"
response =  pipe(question = question, context = context)

print('Response: ', response)