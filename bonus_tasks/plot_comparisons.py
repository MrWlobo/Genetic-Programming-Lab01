import matplotlib.pyplot as plt
import numpy as np
import math

def safe_exp(x, limit=20):
    if x > limit:
        x = limit
    elif x < -limit:
        x = -limit
    return math.exp(x)

filename1 = "tinygp_outputs/bonus_task_2_3a.txt"
filename2 = "tinygp_outputs/bonus_task_2_3b.txt"

with open(filename1, "r") as f:
    function1 = f.readline().strip()

with open(filename2, "r") as f:
    function2 = f.readline().strip()

function1 = function1.replace("EXP", "safe_exp")
function2 = function2.replace("EXP", "safe_exp")

start = 0
end = 4
X = np.linspace(start, end, 100)
Y1_list = []
Y2_list = []

for X1 in X:
    Y_val = eval(function1)
    Y1_list.append(Y_val)

for X1 in X:
    Y_val = eval(function1)
    Y2_list.append(Y_val)

# for X1 in X:
#     try:
#         Y_val = eval(function2, {"__builtins__": None}, {"safe_exp": safe_exp, "X1": X1, "math": math})
#         if Y_val > 100:
#             Y_val = 100
#         elif Y_val < -100:
#             Y_val = -100
#     except OverflowError:
#         Y_val = 100
#     Y2_list.append(Y_val)

Y1 = np.array(Y1_list)
Y2 = np.array(Y2_list)

fig, axis = plt.subplots(1, 2)

axis[0].plot(X, Y1)
axis[1].plot(X, Y2)

axis[0].set_xlabel("X")
axis[0].set_ylabel("Y")
axis[1].set_xlabel("X")
axis[1].set_ylabel("Y")

axis[0].set_title("5x^3 - 2x^2 + 3x - 17 no exp")
axis[1].set_title("5x^3 - 2x^2 + 3x - 17 exp")

plt.tight_layout()
plt.savefig(f"plots/task2/task_2_plot_2.png", dpi=300)
plt.show()
