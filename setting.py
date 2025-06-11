import tkinter as tk
from tkinter import ttk
import pyaudio

def get_devices():
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info.get('maxInputChannels') > 0:
            devices.append((info.get('index'), info.get('name')))
    p.terminate()
    return devices

def select_device():
    window = tk.Tk()
    window.title("Выбор устройства записи")

    devices = get_devices()
    selected_device = tk.StringVar()
    selected_device.set(devices[0][0])  # По умолчанию выбрано первое устройство

    options = [device[1] for device in devices]
    device_menu = ttk.Combobox(window, textvariable=selected_device)
    device_menu['values'] = options

    def save_selection():
        with open('selected_device.txt', 'w') as f:
            f.write(str(devices[options.index(device_menu.get())][0]))
        window.destroy()

    tk.Button(window, text="Сохранить", command=save_selection).pack()
    device_menu.pack()
    window.mainloop()

if __name__ == "__main__":
    select_device()
