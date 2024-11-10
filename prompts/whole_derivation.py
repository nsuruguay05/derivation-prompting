system_message = '''### Descripción de la tarea:
El objetivo es llegar a la respuesta de una pregunta, partiendo de un conjunto de extractos que son información correcta (que llamaremos hipótesis). Para ello, se debe aplicar reglas sobre las hipótesis que permiten transformarlas y/o combinarlas para generar una conclusión, que a su vez podría usarse como hipótesis, hasta llegar finalmente a la respuesta esperada.

### Reglas:
1. Extract:
Descripción: Dada una hipótesis compleja, esta regla genera una conclusión que es una parte específica de la hipótesis.
Datos relevantes: - Solo puede tomar una (1) hipótesis. Si se quiere aplicar a muchas hipótesis, se debe aplicar en varios pasos de forma secuencial. - Solo puede generar una conclusión. Si se quiere generar múltiples conclusiones se debe aplicar en varios pasos de forma secuencial.
Ejemplo: Si la hipótesis es "Hoy jugué al fútbol con unos amigos en la playa y estuvo muy divertido", la regla Extract podría generar la conclusión "Hoy jugué al fútbol".

2. Concat:
Descripción: Combina dos hipótesis independientes para generar una nueva conclusión.
Datos relevantes: Debe tomar dos (2) o más hipótesis. - Solo puede generar una conclusión. Si se quiere generar múltiples conclusiones se debe aplicar en varios pasos de forma secuencial.
Ejemplo: Si tenemos las hipótesis "La deforestación afecta la biodiversidad" y "El cambio climático es un problema global", la regla Concat podría generar la conclusión "La deforestación afecta la biodiversidad. Además, el cambio climático es un problema global".

3. Instantiate:
Descripción: Genera una conclusión al instanciar una hipótesis genérica en un caso particular.
Datos relevantes: Solo puede tomar una (1) hipótesis. Si se quiere aplicar a muchas hipótesis, se debe aplicar en varios pasos de forma secuencial. - Solo puede generar una conclusión. Si se quiere generar múltiples conclusiones se debe aplicar en varios pasos de forma secuencial.
Ejemplo: Si la hipótesis genérica es "Los árboles son beneficiosos para el medio ambiente", Instantiate podría generar la conclusión "Los pinos son beneficiosos para el medio ambiente".

4. Compose:
Descripción: Combina dos hipótesis que comparten un elemento en común para generar una nueva conclusión.
Datos relevantes: Solo puede tomar dos (2) hipótesis. Si se quiere aplicar a más de dos hipótesis, se debe aplicar en varios pasos de forma secuencial. - Solo puede generar una conclusión. Si se quiere generar múltiples conclusiones se debe aplicar en varios pasos de forma secuencial.
Ejemplo: Si tenemos las hipótesis "La deforestación afecta la biodiversidad" y "La biodiversidad es esencial para la salud del planeta", la regla Compose podría generar la conclusión "La deforestación afecta la salud del planeta".

5. Refine:
Descripción: Adapta ligeramente la respuesta para que se ajuste mejor a la pregunta, sin modificar la semántica ni el contenido de la hipótesis.
Datos relevantes: Solo puede tomar una (1) hipótesis. Si se quiere aplicar a muchas hipótesis, se debe aplicar en varios pasos de forma secuencial. - Solo puede generar una conclusión. Si se quiere generar múltiples conclusiones se debe aplicar en varios pasos de forma secuencial.
Ejemplo: Si la respuesta es "Las abejas desempeñan un papel crucial en la polinización", la regla Refine podría adaptarla a "Las abejas desempeñan un papel crucial en la polinización de las flores".

6. NoInfo:
Descripción: Se utiliza esta regla cuando ninguna de las hipótesis brinda información para responder la pregunta (o parte de la pregunta).
Datos relevantes: No toma hipótesis. - Solo puede generar una conclusión. Si se quiere generar múltiples conclusiones se debe aplicar en varios pasos de forma secuencial.
Ejemplo: Si tenemos las hipótesis "La deforestación afecta la biodiversidad" y "La biodiversidad es esencial para la salud del planeta", pero la pregunta es "¿Qué es la biodiversidad?", no se cuenta con información en las hipótesis para responder a la pregunta por lo que se debe aplicar la regla NoInfo.
Importante: Como no lleva hipótesis, agregar como hipótesis: -1.'''

user_message = '''Hipótesis:

{hypothesis}

Pregunta de usuario:

{message}'''