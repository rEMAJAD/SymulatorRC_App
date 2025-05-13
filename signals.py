import numpy as np

def generate_time_array(duration=5.0, dt=0.001):
    return np.arange(0, duration, dt)

def sine_input(t, frequency=1.0, amplitude=1.0):
    return amplitude * np.sin(2 * np.pi * frequency * t)

def step_input(t, amplitude=1.0):
    return amplitude * np.ones_like(t)

def impulse_input(t, amplitude=1.0, width=0.01):
    signal = np.zeros_like(t)
    signal[t < width] = amplitude
    return signal
