import tkinter as tk
from tkinter import simpledialog
import socket
import threading

# ---- GUI ----
root = tk.Tk()
root.withdraw()  # Hide window while asking username

# Ask username
username = simpledialog.askstring("Username", "Enter your name:", parent=root)
if not username:
    username = "Anonymous"

root.deiconify()
root.title(f"Chat Client - {username}")
root.geometry("450x500")

chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side="right", fill="y")

chat = tk.Text(chat_frame, height=20, state="disabled", yscrollcommand=scrollbar.set)
chat.pack(side="left", fill="both", expand=True)
scrollbar.config(command=chat.yview)

entry = tk.Entry(root, width=40)
entry.pack(padx=10, pady=5)
entry.focus_set()

btn = tk.Button(root, text="Send", width=10)
btn.pack(pady=5)

# ---- Networking ----
HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Send username first
if client.recv(1024).decode('utf-8') == "USERNAME":
    client.send(username.encode('utf-8'))

# Receive messages
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat.config(state="normal")
            chat.insert("end", message + "\n")
            chat.config(state="disabled")
            chat.see("end")  # Auto-scroll
        except:
            break

# Send messages
def send():
    msg = entry.get()
    if msg.strip():
        client.send(f"{username}: {msg}".encode('utf-8'))
        entry.delete(0, "end")
        chat.config(state="normal")
        chat.insert("end", f"You: {msg}\n")
        chat.config(state="disabled")
        chat.see("end")

btn.config(command=send)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()