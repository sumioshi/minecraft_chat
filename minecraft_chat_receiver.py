import pika
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from threading import Thread

# Função para processar mensagens recebidas
def receive_messages():
    # Conectar ao RabbitMQ e ouvir mensagens
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='minecraft_chat')

    # Callback para exibir mensagem
    def callback(ch, method, properties, body):
        messages_text.config(state="normal")
        messages_text.insert("end", f"{body.decode()}\n")
        messages_text.config(state="disabled")

    # Inscrever-se na fila e consumir mensagens
    channel.basic_consume(queue='minecraft_chat', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Configuração da interface
app = ttk.Window(themename="solar")
app.title("Minecraft Chat - Mensagens Recebidas")
app.geometry("500x350")

frame = ttk.Frame(app, padding=20, bootstyle="dark")
frame.pack(fill=BOTH, expand=True)

messages_label = ttk.Label(frame, text="Chat do Servidor:", bootstyle="info")
messages_label.pack(pady=(0, 10))

messages_text = ttk.Text(frame, width=55, height=15, state="disabled", background="#282828", foreground="#00FF00")
messages_text.pack(pady=(0, 10))

# Executar o recebimento de mensagens em uma thread separada
thread = Thread(target=receive_messages)
thread.daemon = True
thread.start()

app.mainloop()
