import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from circuit_rc import create_rc_transfer_function, simulate_response
from signals import generate_time_array, sine_input, step_input, impulse_input

# Funkcja do uruchomienia symulacji
def run_simulation():
    R = r_scale.get()
    C = c_scale.get()
    signal_type = signal_var.get()
    t = generate_time_array(5.0)

    if signal_type == "Sinus":
        vin = sine_input(t)
    elif signal_type == "Skok":
        vin = step_input(t)
    elif signal_type == "Impuls":
        vin = impulse_input(t)
    else:
        return

    system = create_rc_transfer_function(R, C)
    t_out, vout = simulate_response(system, t, vin)

    # Wyczyść i narysuj wykres
    ax.clear()
    ax.plot(t_out, vin, label="Vin", linestyle="--")
    ax.plot(t_out, vout, label="Vout", linewidth=2)
    ax.set_title(f"Odpowiedź RC (R={R} Ω, C={C:.5f} F)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Napięcie [V]")
    ax.grid(True)
    ax.legend()
    canvas.draw()

# === INICJALIZACJA GUI ===
root = tk.Tk()
root.title("Symulator Obwodu RC – GUI")
root.geometry("900x600")

# === OBRAZEK UKŁADU RC ===
try:
    img = Image.open("assets/rc_circuit.png")
    img = img.resize((200, 100), Image.Resampling.LANCZOS)
    circuit_img = ImageTk.PhotoImage(img)
    img_label = ttk.Label(root, image=circuit_img)
    img_label.grid(row=0, column=0, padx=20, pady=10)
except Exception as e:
    print(f"Błąd wczytywania obrazka: {e}")

# === PANEL STEROWANIA ===
control_frame = ttk.Frame(root)
control_frame.grid(row=0, column=1, padx=20, pady=10, sticky="n")

ttk.Label(control_frame, text="R (Ohmy)").pack()
r_scale = tk.Scale(control_frame, from_=100, to=10000, orient=tk.HORIZONTAL, resolution=100)
r_scale.set(1000)
r_scale.pack()

ttk.Label(control_frame, text="C (Farady)").pack()
c_scale = tk.Scale(control_frame, from_=1e-5, to=1e-1, orient=tk.HORIZONTAL, resolution=0.0001)
c_scale.set(0.001)
c_scale.pack()

ttk.Label(control_frame, text="Typ sygnału").pack()
signal_var = tk.StringVar()
signal_menu = ttk.Combobox(control_frame, textvariable=signal_var)
signal_menu['values'] = ("Sinus", "Skok", "Impuls")
signal_menu.current(0)
signal_menu.pack(pady=5)

ttk.Button(control_frame, text="Symuluj", command=run_simulation).pack(pady=10)

# === OBSZAR WYKRESU ===
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, pady=10)

# === START GUI ===
root.mainloop()
