import matplotlib.pyplot as plt
import numpy as np
import math

def safe_exp(x, limit=20):
    if x > limit:
        x = limit
    elif x < -limit:
        x = -limit
    return math.exp(x)

filename = "tinygp_outputs/bonus_task_1_(-4-4).txt"

with open(filename, "r") as f:
    function = f.readline().strip()

function = function.replace("Best Individual: ", "").replace("EXP", "safe_exp")

start = -4
end = 4
X = np.linspace(start, end, 100)
Y_list = []

for X1 in X:
    try:
        Y_val = eval(function, {"__builtins__": None}, {"safe_exp": safe_exp, "X1": X1, "math": math})
        if Y_val > 20:
            Y_val = 20
        elif Y_val < -20:
            Y_val = -20
    except OverflowError:
        Y_val = 20.0
    Y_list.append(Y_val)

Y = np.array(Y_list)

plt.plot(X, Y)
plt.title(f"Gauss Function <{start}, {end}>")
plt.xlabel("X")
plt.ylabel("Y")
plt.tight_layout()
plt.savefig(f"plots/GaussFunction({start}-{end}).png", dpi=300)
plt.show()
