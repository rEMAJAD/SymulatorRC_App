import numpy as np
from scipy import signal

def generate_time_array(duration=5.0, dt=0.001):
    return np.arange(0, duration, dt)

def sine_input(t, frequency=1.0, amplitude=1.0):
    return amplitude * np.sin(2 * np.pi * frequency * t)

def step_input(t, amplitude=1.0):
    return amplitude * np.ones_like(t)

def impulse_input(t, amplitude=1.0, width=0.01):
    sig = np.zeros_like(t)
    sig[t < width] = amplitude
    return sig

def triangle_input(t, frequency=1.0, amplitude=1.0):
    return amplitude * signal.sawtooth(2 * np.pi * frequency * t, width=0.5)

def sawtooth_input(t, frequency=1.0, amplitude=1.0):
    return amplitude * signal.sawtooth(2 * np.pi * frequency * t)

def noise_input(t, amplitude=1.0):
    return amplitude * np.random.normal(0, 1, len(t))

def combined_input(t, frequency=1.0):
    return sine_input(t, frequency) + 0.3 * noise_input(t)
