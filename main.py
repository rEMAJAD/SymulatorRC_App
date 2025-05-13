import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from circuit import create_transfer_function, simulate_response
from signals import (
    generate_time_array, sine_input, step_input, impulse_input,
    triangle_input, sawtooth_input, noise_input, combined_input
)

import numpy as np

last_vin = last_vout = last_t = None

def run_simulation():
    global last_vin, last_vout, last_t

    try:
        R = float(r_entry.get())
        C = float(c_entry.get())
        L = float(l_entry.get()) if "RLC" in circuit_type.get() else None
        freq = float(freq_entry.get())
        if R <= 0 or C <= 0 or freq <= 0 or (L is not None and L <= 0):
            raise ValueError
    except ValueError:
        print("Błąd: Nieprawidłowe dane wejściowe.")
        return

    topology = circuit_type.get()
    signal_type = signal_var.get()

    # dynamiczne dt i czas
    if freq >= 1000:
        duration = 0.01
    elif freq >= 100:
        duration = 0.05
    elif freq >= 10:
        duration = 0.2
    else:
        duration = 5.0

    dt = 1 / (freq * 50)
    t = generate_time_array(duration, dt=dt)

    if signal_type == "Sinus":
        vin = sine_input(t, frequency=freq)
    elif signal_type == "Skok":
        vin = step_input(t)
    elif signal_type == "Impuls":
        vin = impulse_input(t)
    elif signal_type == "Trójkątny":
        vin = triangle_input(t, frequency=freq)
    elif signal_type == "Piłokształtny":
        vin = sawtooth_input(t, frequency=freq)
    elif signal_type == "Szum":
        vin = noise_input(t)
    elif signal_type == "Złożony":
        vin = combined_input(t, frequency=freq)
    else:
        return

    system = create_transfer_function(R, C, L, topology=topology)
    t_out, vout = simulate_response(system, t, vin)

    last_vin, last_vout, last_t = vin, vout, t_out

    plot_time(t_out, vin, vout)
    plot_fft(t_out, vin, vout)

    desc_label.config(text=f"Typ układu: {topology}")

def toggle_l_entry(*args):
    if "RLC" in circuit_type.get():
        l_label.pack()
        l_entry.pack()
    else:
        l_label.pack_forget()
        l_entry.pack_forget()

def plot_time(t, vin, vout):
    time_ax.clear()
    time_ax.plot(t, vin, label="Vin", linestyle="--")
    time_ax.plot(t, vout, label="Vout", linewidth=2)
    time_ax.set_title("Odpowiedź układu – domena czasu")
    time_ax.set_xlabel("Czas [s]")
    time_ax.set_ylabel("Napięcie [V]")
    time_ax.set_xlim(t[0], t[-1])
    time_ax.grid(True)
    time_ax.legend()
    time_canvas.draw()

def plot_fft(t, vin, vout):
    dt = t[1] - t[0]
    freqs = np.fft.rfftfreq(len(t), dt)
    Vin_f = np.abs(np.fft.rfft(vin))
    Vout_f = np.abs(np.fft.rfft(vout))

    fft_ax.clear()
    fft_ax.plot(freqs, Vin_f, label="FFT Vin", linestyle="--")
    fft_ax.plot(freqs, Vout_f, label="FFT Vout", linewidth=2)
    fft_ax.set_title("Widmo częstotliwościowe (FFT)")
    fft_ax.set_xlabel("Częstotliwość [Hz]")
    fft_ax.set_ylabel("Amplituda")
    fft_ax.set_xlim(freqs[0], freqs[-1])
    fft_ax.grid(True)
    fft_ax.legend()
    fft_canvas.draw()

# === GUI ===
root = tk.Tk()
root.title("Symulator RC/RLC – wpisywanie parametrów")
root.geometry("1100x800")
root.configure(bg="#f4f4f4")

control_frame = ttk.Frame(root, padding=10)
control_frame.pack(side=tk.TOP, fill=tk.X)

ttk.Label(control_frame, text="Typ układu:").pack()
circuit_type = tk.StringVar()
circuit_type.set("RC szeregowy")
ttk.Combobox(control_frame, textvariable=circuit_type,
             values=["RC szeregowy", "RC równoległy", "RLC szeregowy", "RLC równoległy"]).pack()
circuit_type.trace_add("write", toggle_l_entry)

ttk.Label(control_frame, text="R (Ohmy):").pack()
r_entry = ttk.Entry(control_frame)
r_entry.insert(0, "100")
r_entry.pack()

ttk.Label(control_frame, text="C (Farady):").pack()
c_entry = ttk.Entry(control_frame)
c_entry.insert(0, "0.001")
c_entry.pack()

l_label = ttk.Label(control_frame, text="L (Henry):")
l_entry = ttk.Entry(control_frame)
l_entry.insert(0, "0.01")

ttk.Label(control_frame, text="Typ sygnału").pack()
signal_var = tk.StringVar()
signal_menu = ttk.Combobox(control_frame, textvariable=signal_var)
signal_menu['values'] = ("Sinus", "Skok", "Impuls", "Trójkątny", "Piłokształtny", "Szum", "Złożony")
signal_menu.current(0)
signal_menu.pack(pady=5)

ttk.Label(control_frame, text="Częstotliwość (Hz):").pack()
freq_entry = ttk.Entry(control_frame)
freq_entry.insert(0, "1000.0")
freq_entry.pack(pady=5)

ttk.Button(control_frame, text="Symuluj", command=run_simulation).pack(pady=10)

desc_label = ttk.Label(root, text="Typ układu: RC szeregowy", font=("Arial", 12, "bold"))
desc_label.pack(pady=10)

plot_frame = ttk.Frame(root, padding=10)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

time_fig = Figure(figsize=(6, 3.5), dpi=100)
time_ax = time_fig.add_subplot(111)
time_canvas = FigureCanvasTkAgg(time_fig, master=plot_frame)
time_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fft_fig = Figure(figsize=(6, 3.5), dpi=100)
fft_ax = fft_fig.add_subplot(111)
fft_canvas = FigureCanvasTkAgg(fft_fig, master=plot_frame)
fft_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()
