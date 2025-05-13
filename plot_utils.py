import matplotlib.pyplot as plt

def plot_signals(t, input_signal, output_signal, title="RC Response"):
    plt.figure(figsize=(10, 5))
    plt.plot(t, input_signal, label='Vin(t)', linestyle='--')
    plt.plot(t, output_signal, label='Vout(t)', linewidth=2)
    plt.title(title)
    plt.xlabel("Czas [s]")
    plt.ylabel("Napięcie [V]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
