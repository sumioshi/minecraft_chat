import pika
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Função para enviar mensagem
def send_message():
    username = username_entry.get()
    message = message_entry.get()

    if not username or not message:
        messagebox.showwarning("Aviso", "Insira seu nome e uma mensagem.")
        return

    # Conectar ao RabbitMQ e enviar a mensagem
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='minecraft_chat')

    # Formatar mensagem no estilo Minecraft (ex: "<Steve> Olá, mundo!")
    formatted_message = f"<{username}> {message}"
    channel.basic_publish(exchange='', routing_key='minecraft_chat', body=formatted_message)
    message_entry.delete(0, END)
    connection.close()

# Configuração da interface
app = ttk.Window(themename="solar")
app.title("Minecraft Chat - Enviar Mensagem")
app.geometry("400x250")

frame = ttk.Frame(app, padding=20, bootstyle="dark")
frame.pack(fill=BOTH, expand=True)

username_label = ttk.Label(frame, text="Nome do Jogador:", bootstyle="info")
username_label.pack(pady=(0, 5))

username_entry = ttk.Entry(frame, width=30)
username_entry.pack(pady=(0, 10))

message_label = ttk.Label(frame, text="Digite a Mensagem:", bootstyle="info")
message_label.pack(pady=(0, 5))

message_entry = ttk.Entry(frame, width=40)
message_entry.pack(pady=(0, 10))

send_button = ttk.Button(frame, text="Enviar", command=send_message, bootstyle="success")
send_button.pack(pady=(10, 0))

app.mainloop()
