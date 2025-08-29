import gradio as gr
from chatbot import Chatbot

bot = Chatbot()

def chat_fn(user_input, history):
    if not user_input.strip():
        return history + [[user_input, "Por favor escribe una pregunta."]]
    
    response = bot.get_response(user_input)
    history = history + [[user_input, response]]
    return history

def suggest_fn():
    # Devuelve 3 preguntas distintas cada vez
    return bot.suggest_questions(top_n=3)

def use_suggestion(suggestion, history):
    response = bot.get_response(suggestion)
    history = history + [[suggestion, response]]
    return history

def clear_fn():
    return []

with gr.Blocks(theme="soft") as demo:
    gr.Markdown("## Chatbot Universitario")
    gr.Markdown("Haz tu pregunta o explora sugerencias predefinidas.")

    chatbot = gr.Chatbot(label=" Conversación")
    user_input = gr.Textbox(label="Tu pregunta", placeholder="Escribe aquí...")

    with gr.Row():
        send_btn = gr.Button(" Preguntar")
        clear_btn = gr.Button(" Limpiar Chat")

    with gr.Accordion(" PREGUNTAS SUGERIDAS", open=False):
        suggest_btn = gr.Button(" Generar nuevas sugerencias")
        with gr.Row() as suggestion_row:
            suggestion_btns = [gr.Button("", visible=False) for _ in range(3)]

    # Enviar pregunta escrita
    send_btn.click(fn=chat_fn, inputs=[user_input, chatbot], outputs=chatbot)
    user_input.submit(fn=chat_fn, inputs=[user_input, chatbot], outputs=chatbot)

    # Limpiar chat
    clear_btn.click(fn=clear_fn, outputs=chatbot)

    # Generar sugerencias dinámicas
    def update_suggestions():
        s = suggest_fn()
        return [
            gr.update(value=s[0], visible=True),
            gr.update(value=s[1], visible=True),
            gr.update(value=s[2], visible=True),
        ]

    suggest_btn.click(fn=update_suggestions, outputs=suggestion_btns)

    # Cuando hago click en una sugerencia, se manda al bot
    for btn in suggestion_btns:
        btn.click(fn=use_suggestion, inputs=[btn, chatbot], outputs=chatbot)

if __name__ == "__main__":
    demo.launch()
