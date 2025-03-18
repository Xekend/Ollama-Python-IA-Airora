import tkinter as tk
from pycaw.pycaw import AudioUtilities

class AiroraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Airora")
        self.geometry("800x600")

        # Crear una ventana secundaria para mostrar el uso de recursos
        self.ventana_uso_recurso = tk.Toplevel(self)
        self.ventana_uso_recurso.title("Uso de Recursos")

        # Crear etiquetas para mostrar los datos
        label_cpu_usage = tk.Label(self.ventana_uso_recurso, text="Uso de CPU:")
        label_gpu_usage = tk.Label(self.ventana_uso_recurso, text="Uso de GPU:")
        label_ram_usage = tk.Label(self.ventana_uso_recurso, text="Uso de RAM:")

        # Crear botones para actualizar la información
        button_update = tk.Button(self.ventana_uso_recurso, text="Actualizar", command=self.get_resource_usage)

        # Agregar los componentes a la ventana
        label_cpu_usage.pack()
        label_gpu_usage.pack()
        label_ram_usage.pack()
        self.button_update = button_update

    def get_resource_usage(self):
        # Obtener el objeto de audio
        units = AudioUtilities.GetSpeakers()
        device = units.Activate(
            interfaceClass=pycaw.PYAudioInterface,
            flags=pycaw.PYAudioInterfaceFlags.STREAM,
            clientVolume=None)

        # Obtener la información del dispositivo de audio
        info = device.GetDeviceProperties(0)
        device_info = device.GetDeviceInfoList(0)

        # Extraer el uso de CPU, GPU y RAM
        cpu_usage = device_info[2][0]  # Uso de CPU (en porcentaje)
        gpu_usage = device_info[3][0]  # Uso de GPU (en porcentaje)
        ram_usage = device_info[4][0]  # Uso de RAM (en GB)

        # Mostrar los datos en la ventana
        self.label_cpu_usage.config(text=f"Uso de CPU: {cpu_usage}%")
        self.label_gpu_usage.config(text=f"Uso de GPU: {gpu_usage}%")
        self.label_ram_usage.config(text=f"Uso de RAM: {ram_usage} GB")

# Crear una instancia de la aplicación
app = AiroraApp()

# Mostrar la ventana principal
app.mainloop()