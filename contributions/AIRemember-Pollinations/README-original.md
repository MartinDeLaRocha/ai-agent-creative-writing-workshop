![4e756570-dc34-438c-a387-8f95f1fa5bf9](https://github.com/user-attachments/assets/0b444e5d-7650-47ca-bea9-365cd39c5b98)

> **New: [AIRemember — Pollinations edition](README-Pollinations.md)** writes the same "Me acuerdo" books with no API key and no local model, using the Pollinations free tier. It adds CLI options, score parsing, deduplication, rate-limit backoff and offline tests. Start there if you do not have Ollama running.


# 🧠📖 AI Remember

**Software de literatura generativa que utiliza modelos LLM locales para producir recuerdos ficticios bajo la forma “Me acuerdo…”.**

AI Remember es un experimento de **literatura generativa**, Python y modelos de lenguaje ejecutados localmente mediante **Ollama**.

El proyecto toma como referencia la estructura de *I Remember* de **Joe Brainard** y *Je me souviens* de **Georges Perec**: una sucesión de fragmentos construidos alrededor de una fórmula repetida.

En AI Remember, quien recuerda es un modelo de lenguaje.

Cada texto surge de la combinación de:

- 🧠 instrucciones de sistema
- 🎲 una o dos palabras seed
- 📚 un ejemplo seleccionado al azar
- 🌡️ parámetros de generación
- 🤖 un LLM generador
- ✍️ un segundo LLM que funciona como editor

Los recuerdos son inventados, pero pueden sugerir una memoria colectiva probable: tecnología, objetos cotidianos, cultura popular, errores, anacronismos y asociaciones inesperadas.

> “Todos esos recuerdos se perderán como lágrimas en la lluvia.”  
> — Roy Batty, *Blade Runner*

---

## ✨ Características

- 🧠 Generación literaria con LLM
- 🏠 Ejecución local con Ollama
- 🐍 Implementado en Python
- 📚 Inspirado en Joe Brainard y Georges Perec
- 🎲 Selección aleatoria de palabras seed
- 🔀 Uso periódico de dos seeds simultáneos
- 📝 Ejemplos literarios como referencia de formato
- 🌡️ Temperatura y `top_p` configurables
- 📏 Ventana de contexto configurable
- ⚡ Generación por streaming
- ✍️ Segundo modelo utilizado como editor
- 🔢 Evaluación de cada fragmento de 1 a 10
- ✅ Validación automática del comienzo `Me acuerdo`
- 📄 Compilación incremental en `airemember.txt`
- 📖 Libro generado incluido en el repositorio
- 🔌 Sin dependencia de APIs cloud
- 📜 Licencia MIT para el software

---

## 🧩 Origen

En 2011 participé del ciclo **Celebración de Perec** en el CCEBA con una performance sobre *No recuerdo*, de Esteban Feune de Colombi, inspirado en *Je me souviens* de Georges Perec, inspirado a su vez en *I Remember* de Joe Brainard.

Desde entonces quedó dando vueltas la idea de desarrollar un software capaz de automatizar una escritura similar.

Años después, una ThinkPad cargada con modelos y librerías de IA fue el punto de partida para AI Remember.

El procedimiento conserva la repetición formal de esas obras, pero reemplaza la memoria humana por una máquina estadística que produce recuerdos que nunca ocurrieron.

---

## 📚 Antecedentes literarios

### Joe Brainard — *I Remember*

Joe Brainard publicó *I Remember* originalmente en 1970.

El libro está compuesto por una sucesión de fragmentos iniciados por:

```text
I remember...
```

La repetición funciona como mecanismo generativo para recuperar recuerdos personales, objetos cotidianos, hábitos, cultura popular y acontecimientos aparentemente insignificantes.

- [The Collected Writings of Joe Brainard — Library of America](https://www.loa.org/books/482-the-collected-writings-of-joe-brainard-paperback/)
- [I Remember Joe Brainard — Library of America](https://rememberjoebrainard.loa.org/)

### Georges Perec — *Je me souviens*

Georges Perec publicó *Je me souviens* en 1978.

La obra reúne 480 entradas que comienzan con:

```text
Je me souviens...
```

o:

```text
Me acuerdo...
```

Perec utiliza esa estructura para construir una memoria simultáneamente personal y colectiva a partir de objetos, canciones, personajes, expresiones y detalles de una época.

- [Je me souviens — Bibliothèque nationale de France](https://catalogue.bnf.fr/ark:/12148/cb34592799z)
- [Me acuerdo — Impedimenta](https://impedimenta.es/producto/me-acuerdo)

---

## 🎛️ Procedimiento generativo

```text
sustantivos.csv
      │
      └──── palabra seed ────────┐
                                 │
meacuerdo.csv                    │
      │                          │
      └──── ejemplo aleatorio ───┤
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  LLM generador  │
                        │     Ollama      │
                        └────────┬────────┘
                                 │
                                 ▼
                           "Me acuerdo..."
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   LLM editor    │
                        │                 │
                        │ puntuación 1-10 │
                        └────────┬────────┘
                                 │
                                 ▼
                            validación
                                 │
                                 ▼
                         airemember.txt
                                 │
                                 ▼
                              📖 libro
```

Cada iteración:

1. selecciona un ejemplo de `meacuerdo.csv`
2. selecciona una palabra de `sustantivos.csv`
3. cada tercera generación intenta utilizar dos palabras diferentes
4. construye el prompt
5. genera un recuerdo mediante Ollama
6. envía el resultado a un segundo modelo
7. obtiene una puntuación de 1 a 10
8. valida el formato
9. agrega el fragmento a `airemember.txt`

---

## 🎲 Palabras seed

Las palabras utilizadas para disparar asociaciones se cargan desde:

```text
sustantivos.csv
```

El archivo debe contener una entrada por línea.

Ejemplo:

```text
fax
módem
robot
discman
terminal
disquete
internet
microchip
satélite
videocasetera
```

El código carga las entradas con:

```python
listaSustantivos = [
    linea.strip()
    for linea in archivo
    if linea.strip()
]
```

Para cada generación selecciona una palabra al azar:

```python
sustantivo1 = random.choice(listaSustantivos)
```

---

## 🔀 Dos seeds

Cada tercera generación, AI Remember intenta combinar dos palabras diferentes:

```python
usarDosSustantivos = (
    contador % 3 == 2
    and len(listaSustantivos) >= 2
)
```

Por ejemplo:

```text
'fax' y 'abuela'
```

La combinación permite provocar asociaciones menos previsibles entre conceptos alejados.

---

## 📚 Ejemplos

El archivo:

```text
meacuerdo.csv
```

contiene ejemplos utilizados como referencia de formato y estilo.

En cada iteración se selecciona uno al azar:

```python
ejemploAleatorio = random.choice(listaEjemplos)
```

La estructura del prompt actual es:

```text
Escribir una oración de 10 a 25 palabras que empiece con: Me acuerdo

Usar 'SEED'.

Ejemplo de estilo: EJEMPLO.
```

Cuando se utilizan dos palabras:

```text
Usar 'SEED_1' y 'SEED_2'.
```

---

## 🤖 Modelo generador

El modelo utilizado para escribir los recuerdos se configura en:

```python
modeloChat = ""
```

El libro incluido en el repositorio fue producido utilizando **Dolphin Llama 3 8B**.

Puede descargarse mediante Ollama:

```bash
ollama pull dolphin-llama3:8b
```

y configurarse con:

```python
modeloChat = "dolphin-llama3:8b"
```

- [Dolphin Llama 3 — Ollama](https://ollama.com/library/dolphin-llama3)

Puede utilizarse otro modelo compatible con Ollama.

---

## 🌡️ Parámetros de generación

El código actual define:

```python
temperatura = 1
topP = 1
tamanioVentanaContexto = 1024
```

y los utiliza en:

```python
options={
    "temperature": temperatura,
    "num_ctx": tamanioVentanaContexto,
    "top_p": topP
}
```

La generación se realiza además mediante streaming:

```python
stream=True
```

por lo que el recuerdo aparece progresivamente en la terminal.

---

## 🧠 Instrucciones de sistema

El comportamiento general del escritor se define en:

```python
sistema = "Sos un escritor..."
```

Allí pueden establecerse criterios como:

- tono
- voz
- registro
- época
- longitud
- temas
- nivel de extrañeza
- referencias culturales
- restricciones
- elementos que deben evitarse

---

## ✍️ Modelo editor

Después de generar cada fragmento, AI Remember lo envía a un segundo LLM.

El modelo se configura en:

```python
modeloEvaluacion = ""
```

El sistema editorial se define en:

```python
sistemaEvaluacion = "Sos un editor que responde puntuando textos del 0 al 10..."
```

El prompt enviado al editor es:

```text
Evalúa la siguiente frase en una escala del 1 al 10.
Retorna solo el número.
```

Para esta etapa se utiliza una temperatura menor:

```python
"temperature": 0.2
```

El modelo generador y el modelo editor pueden ser diferentes.

---

## 📊 Evaluación

La respuesta del editor debe poder convertirse a un entero:

```python
puntajeEvaluacion = int(contenidoEvaluacion)
```

y encontrarse entre:

```text
1 ... 10
```

Cada recuerdo guardado incluye:

- texto generado
- número de generación
- seed o seeds utilizados
- puntuación editorial

Ejemplo:

```text
Me acuerdo de aquel módem que parecía discutir con el teléfono antes de conectarse. | -- 42 (módem) | Puntuación: 8/10
```

La implementación actual registra la puntuación pero no aplica un puntaje mínimo de aceptación.

---

## ✅ Validación

Antes de incorporar un texto al compilado se comprueba:

```python
def validarFrase(frase):
    return frase.startswith("Me acuerdo") and "Nota:" not in frase
```

Se descartan respuestas que:

- no comienzan con `Me acuerdo`
- contienen `Nota:`
- producen un error durante la evaluación

---

## 📄 Compilación

Los recuerdos aceptados se guardan en:

```text
airemember.txt
```

El archivo se abre en modo append:

```python
logging.basicConfig(
    filename=archivoLog,
    level=logging.INFO,
    format="%(message)s",
    encoding="utf-8",
    filemode='a'
)
```

Esto permite que cada ejecución continúe agregando recuerdos al compilado existente.

---

## 📖 Libro

El repositorio incluye:

[`AIRemember.pdf`](AIRemember.pdf)

El libro fue producido en Buenos Aires en abril de 2025 a partir de textos generados con el procedimiento de AI Remember.

Los fragmentos exploran recurrentemente:

- computadoras
- redes
- robots
- terminales
- videojuegos
- fax
- inteligencia artificial
- realidad virtual
- teléfonos
- chips
- memoria
- futuros imaginados

También puede consultarse en:

- [AI Remember — Scribd](https://es.scribd.com/document/851972773/AI-Remember)

---

## 🖼️ Ejemplo

![Ejemplo de AI Remember](https://github.com/user-attachments/assets/2a6a2192-5b2c-4682-8976-8763a23fb34f)

---

## 📁 Estructura del repositorio

```text
AIRemember/
├── AIRemember.pdf
├── LICENSE
├── README.md
└── aiRememberUpload.py
```

### `aiRememberUpload.py`

Programa principal encargado de:

- cargar las palabras seed
- cargar los ejemplos
- seleccionar entradas al azar
- construir prompts
- llamar a Ollama
- generar texto mediante streaming
- evaluar cada fragmento
- validar las respuestas
- compilar el resultado

### `AIRemember.pdf`

Edición del libro producido con el sistema.

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/ronibandini/AIRemember.git
cd AIRemember
```

### 2. Instalar Python

- [Python](https://www.python.org/downloads/)

Comprobar la instalación:

```bash
python3 --version
```

### 3. Instalar Ollama

- [Ollama](https://ollama.com/download)

Comprobar:

```bash
ollama --version
```

### 4. Descargar un modelo

Por ejemplo:

```bash
ollama pull dolphin-llama3:8b
```

### 5. Instalar la librería Python de Ollama

```bash
pip install ollama
```

### 6. Crear `sustantivos.csv`

Ejemplo:

```text
fax
módem
robot
terminal
cassette
internet
disquete
microchip
```

### 7. Crear `meacuerdo.csv`

Una frase por línea.

Ejemplo:

```text
Me acuerdo de las agendas telefónicas junto al teléfono.
Me acuerdo de rebobinar los cassettes con una lapicera.
Me acuerdo de escuchar el módem antes de conectarme a Internet.
```

### 8. Configurar los modelos

En:

```text
aiRememberUpload.py
```

definir:

```python
modeloChat = "dolphin-llama3:8b"
modeloEvaluacion = "dolphin-llama3:8b"
```

También pueden utilizarse dos modelos diferentes.

### 9. Configurar los prompts de sistema

Completar:

```python
sistema = "Sos un escritor..."
```

y:

```python
sistemaEvaluacion = "Sos un editor..."
```

### 10. Ejecutar

```bash
python3 aiRememberUpload.py
```

El programa muestra:

```text
🧠 AI Remember, Roni Bandini, Abril 2025

Cargados ... sustantivos desde 'sustantivos.csv'.
Cargados ... ejemplos desde 'meacuerdo.csv'.
El libro se produce en 'airemember.txt'.
```

Luego comienza la generación continua.

---

## 🛑 Detener el proceso

Presionar:

```text
CTRL+C
```

El contenido generado permanece almacenado en:

```text
airemember.txt
```

---

## 🐞 Depuración

El código incluye:

```python
depurar = 0
```

Para visualizar el seed y el ejemplo seleccionados en cada iteración:

```python
depurar = 1
```

La terminal mostrará información similar a:

```text
Seed: 'fax'
Ejemplo: Me acuerdo de...
```

---

## ⚙️ Configuración principal

| Variable | Función | Valor inicial |
|---|---|---|
| `modeloChat` | LLM generador | `""` |
| `temperatura` | Temperatura de generación | `1` |
| `topP` | Nucleus sampling | `1` |
| `tamanioVentanaContexto` | Ventana de contexto | `1024` |
| `sistema` | Prompt de sistema del escritor | `"Sos un escritor..."` |
| `archivoSustantivos` | Archivo de seeds | `sustantivos.csv` |
| `archivoEjemplos` | Archivo de ejemplos | `meacuerdo.csv` |
| `archivoLog` | Compilación | `airemember.txt` |
| `modeloEvaluacion` | LLM editor | `""` |
| `sistemaEvaluacion` | Criterios editoriales | configurable |
| `depurar` | Mostrar seed y ejemplo | `0` |

---

## 🎲 Variabilidad

El procedimiento contiene varias fuentes de indeterminación:

```text
seed aleatorio
+
ejemplo aleatorio
+
modelo
+
temperatura
+
top_p
+
prompt de sistema
+
muestreo del LLM
```

Dos ejecuciones realizadas con los mismos archivos pueden producir compilaciones completamente diferentes.

---

## 🔬 Ideas para extender el proyecto

1. **📊 Curaduría por puntaje** — incorporar al compilado solamente los textos que superen un umbral editorial configurable.

2. **🧬 Varias generaciones por seed** — generar múltiples recuerdos para una misma combinación y hacer que el modelo editor seleccione uno.

3. **📖 Maquetación automática** — convertir `airemember.txt` directamente en PDF o EPUB.

---

## 📰 Referencias externas

### ✍️ Medium

**AI Remember: un LLM generador de “Me acuerdo”**

[Leer el artículo en Medium](https://bandini.medium.com/ai-remember-un-llm-generador-de-me-acuerdo-938dd863f8c0)

Artículo en español sobre el origen del proyecto, sus antecedentes literarios y el proceso de generación con modelos locales.

### 📖 Scribd

**AI Remember**

[Leer el libro en Scribd](https://es.scribd.com/document/851972773/AI-Remember)

Publicación de la edición generada en abril de 2025.

---

## 🎤 Presentaciones

### 📚 Feria Internacional del Libro de Buenos Aires 2025

AI Remember formó parte del trabajo presentado alrededor de inteligencia artificial, literatura generativa y máquinas literarias durante la **49.ª Feria Internacional del Libro de Buenos Aires**.

El 2 de mayo de 2025, la programación del auditorio Ticmas incluyó:

**Máquinas literarias, IA y contracultura maker**

Un diálogo con Roni Bandini sobre literatura, Inteligencia Artificial y experimentación tecnológica.

[Una jornada de inteligencia artificial en el auditorio de Ticmas en la Feria del Libro — Infobae](https://www.infobae.com/educacion/2025/05/02/una-jornada-de-inteligencia-artificial-en-el-auditorio-de-ticmas-en-la-feria-del-libro/)

---

## 📚 Referencias literarias

- [Joe Brainard — Library of America](https://www.loa.org/books/482-the-collected-writings-of-joe-brainard-paperback/)
- [I Remember Joe Brainard](https://rememberjoebrainard.loa.org/)
- [Je me souviens — Bibliothèque nationale de France](https://catalogue.bnf.fr/ark:/12148/cb34592799z)
- [Me acuerdo — Impedimenta](https://impedimenta.es/producto/me-acuerdo)
- [Georges Perec — Oulipo](https://www.oulipo.net/en/oulipiens/gp)

---

## 🧰 Referencias técnicas

- [Ollama](https://ollama.com/)
- [Dolphin Llama 3](https://ollama.com/library/dolphin-llama3)
- [Python](https://www.python.org/)

---

## 🔗 También te puede interesar

Otros proyectos de **Roni Bandini** relacionados con literatura, IA e interfaces no convencionales.

### 🧸📚 Borges Furby

Un Furby de 1998 transformado en un autómata relacionado con Jorge Luis Borges mediante Arduino y audio digital.

[github.com/ronibandini/furby](https://github.com/ronibandini/furby)

### 📚⌨️ Kindle Typewriter

Un Kindle Paperwhite jailbreakeado convertido en una máquina de escribir conectada a una Raspberry Pi y una impresora térmica.

[github.com/ronibandini/Kindle-Typewriter](https://github.com/ronibandini/Kindle-Typewriter)

### 📚🤖 JailbreakedKindleGPT

ChatGPT ejecutado desde un Kindle Paperwhite jailbreakeado mediante Bash, KTerm y la API de OpenAI.

[github.com/ronibandini/JailbreakedKindleGPT](https://github.com/ronibandini/JailbreakedKindleGPT)

---

## 📜 Licencia

El software de AI Remember se distribuye bajo licencia **MIT**.

Ver [`LICENSE`](LICENSE).

Los textos, ejemplos y obras literarias utilizados como material de referencia conservan sus respectivos derechos.

---

## 👤 Autor

**Roni Bandini**

Maker, desarrollador de IA, artista electrónico y escritor.

- 🐙 GitHub: [@ronibandini](https://github.com/ronibandini)
- 💼 LinkedIn: [Roni Bandini](https://www.linkedin.com/in/ronibandini/)
- 📸 Instagram: [@ronibandini](https://www.instagram.com/ronibandini/)
- 🐦 X: [@RoniBandini](https://x.com/RoniBandini)
- ✍️ Medium: [bandini.medium.com](https://bandini.medium.com/)

Buenos Aires, Argentina.
