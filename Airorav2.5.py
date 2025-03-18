import customtkinter as ctk
import requests
import json
import os
import psutil
import pynvml
import threading
import time

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")  # Modo oscuro (puedes cambiarlo a "light")
ctk.set_default_color_theme("blue")  # Tema de colores

# Configuración de Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "Xekend/Chat:latest"

# Archivo para guardar el historial
HISTORY_FILE = "chat_history.json"

# Cargar el historial de conversación desde el archivo (si existe)
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Guardar el historial de conversación en el archivo
def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

# Historial de conversación
conversation_history = load_history()

# Función para enviar mensajes a Ollama
def send_message():
    user_message = entry.get()
    entry.delete(0, "end")

    conversation_history.append({"role": "user", "content": user_message})
    chat_display.configure(state="normal")
    chat_display.insert("end", f"Tú: {user_message}\n")
    chat_display.configure(state="disabled")

    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }

    with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
        if response.status_code == 200:
            assistant_message = ""
            chat_display.configure(state="normal")
            chat_display.insert("end", "Airora: ")
            chat_display.configure(state="disabled")

            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    if "response" in chunk:
                        fragment = chunk["response"]
                        assistant_message += fragment
                        chat_display.configure(state="normal")
                        chat_display.insert("end", fragment)
                        chat_display.configure(state="disabled")
                        chat_display.see("end")
                        chat_display.update()

            conversation_history.append({"role": "assistant", "content": assistant_message})
            chat_display.configure(state="normal")
            chat_display.insert("end", "\n")
            chat_display.configure(state="disabled")

            save_history(conversation_history)
        else:
            chat_display.configure(state="normal")
            chat_display.insert("end", "Error: No se pudo obtener una respuesta.\n")
            chat_display.configure(state="disabled")

# Función para cargar el historial en el chat al iniciar la aplicación
def load_chat_history():
    chat_display.configure(state="normal")
    for message in conversation_history:
        if message["role"] == "user":
            chat_display.insert("end", f"Tú: {message['content']}\n")
        else:
            chat_display.insert("end", f"Airora: {message['content']}\n")
    chat_display.configure(state="disabled")
    chat_display.see("end")

# Función para borrar el historial
def clear_history():
    global conversation_history
    conversation_history = []
    save_history(conversation_history)
    chat_display.configure(state="normal")
    chat_display.delete(1.0, "end")
    chat_display.configure(state="disabled")

# Función para obtener el uso de CPU, RAM y GPU
def get_system_usage():
    # Uso de CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    
    # Uso de RAM
    ram_info = psutil.virtual_memory()
    ram_percent = ram_info.percent
    
    # Uso de GPU
    gpu_percent = "N/A"
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Primera GPU
        gpu_info = pynvml.nvmlDeviceGetUtilizationRates(handle)
        gpu_percent = gpu_info.gpu
        pynvml.nvmlShutdown()
    except pynvml.NVMLError:
        gpu_percent = "N/A"
    
    return cpu_percent, ram_percent, gpu_percent

# Función para actualizar el navbar con el uso de recursos
def update_navbar():
    while True:
        cpu_percent, ram_percent, gpu_percent = get_system_usage()
        navbar_text = f"CPU: {cpu_percent}% | RAM: {ram_percent}% | GPU: {gpu_percent}%"
        navbar_label.configure(text=navbar_text)
        time.sleep(1)  # Actualizar cada segundo

# Crear la ventana principal
window = ctk.CTk()
window.title("Airora By Xekend")
window.geometry("800x650")
window.configure(bg="#2E2E2E")

# Área de chat (Text widget)
chat_display = ctk.CTkTextbox(
    window,
    width=700,
    height=400,
    corner_radius=10,
    font=("Arial", 14),
    wrap="word",
    state="disabled"
)
chat_display.place(x=50, y=50)

# Campo de entrada para el usuario
entry = ctk.CTkEntry(
    window,
    width=500,
    height=40,
    corner_radius=10,
    font=("Arial", 14),
    placeholder_text="Escribe tu mensaje..."
)
entry.place(x=50, y=480)

# Botón para enviar mensajes
send_button = ctk.CTkButton(
    window,
    text="Enviar",
    command=send_message,
    width=180,
    height=40,
    corner_radius=10,
    font=("Arial", 14)
)
send_button.place(x=570, y=480)

# Botón para borrar el historial
clear_button = ctk.CTkButton(
    window,
    text="Borrar Historial",
    command=clear_history,
    width=700,
    height=40,
    corner_radius=10,
    font=("Arial", 14),
    fg_color="#D32F2F",  # Color rojo
    hover_color="#B71C1C"
)
clear_button.place(x=50, y=540)

# Navbar para mostrar el uso de recursos
navbar_label = ctk.CTkLabel(
    window,
    text="CPU: 0% | RAM: 0% | GPU: 0%",
    width=800,
    height=40,
    corner_radius=0,
    font=("Arial", 12),
    fg_color="#333333",
    text_color="#FFFFFF"
)
navbar_label.place(x=0, y=610)

# Cargar el historial en el chat al iniciar la aplicación
load_chat_history()

# Iniciar la actualización del navbar en un hilo separado
navbar_thread = threading.Thread(target=update_navbar, daemon=True)
navbar_thread.start()

# Iniciar la aplicación
window.resizable(False, False)
window.mainloop()