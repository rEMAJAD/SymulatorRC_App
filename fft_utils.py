import numpy as np
import matplotlib.pyplot as plt

def plot_fft(t, vin, vout):
    dt = t[1] - t[0]
    N = len(t)
    freqs = np.fft.rfftfreq(N, dt)
    Vin_f = np.abs(np.fft.rfft(vin))
    Vout_f = np.abs(np.fft.rfft(vout))

    plt.figure(figsize=(10, 5))
    plt.plot(freqs, Vin_f, label="FFT Vin", linestyle="--")
    plt.plot(freqs, Vout_f, label="FFT Vout", linewidth=2)
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Amplituda")
    plt.title("Widmo częstotliwościowe sygnałów")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
