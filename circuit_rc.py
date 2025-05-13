from scipy import signal

def create_rc_transfer_function(R, C):
    num = [1]
    den = [R * C, 1]
    return signal.TransferFunction(num, den)

def simulate_response(system, t, input_signal):
    t_out, y_out, _ = signal.lsim(system, U=input_signal, T=t)
    return t_out, y_out
