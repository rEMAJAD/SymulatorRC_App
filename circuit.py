from scipy import signal

def create_transfer_function(R, C, L=None, topology="RC szeregowy"):
    if topology == "RC szeregowy":
        num = [1]
        den = [R * C, 1]

    elif topology == "RC równoległy":
        num = [1]
        den = [1, 1 / (R * C)]

    elif topology == "RLC szeregowy":
        num = [1]
        den = [L * C, R * C, 1]

    elif topology == "RLC równoległy":
        num = [1]
        den = [1, 1 / (R * C), 1 / (L * C)]

    else:
        raise ValueError("Nieobsługiwany typ układu")

    return signal.TransferFunction(num, den)

def simulate_response(system, t, input_signal):
    t_out, y_out, _ = signal.lsim(system, U=input_signal, T=t)
    return t_out, y_out
