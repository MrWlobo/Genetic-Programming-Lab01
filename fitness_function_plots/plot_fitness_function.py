import matplotlib.pyplot as plt
import numpy as np

filename = "tinygp_output/example3.txt"
task_name = "Task_5_(-3.14-3.14)"

with open(filename, "r") as f:
    lines = f.readlines()

generation_data = []

for line in lines:
    if line.split(" ")[0].split("=")[0] == "Generation":
        generation_data.append(line.split(" "))

generations = []
avg_fitness = []
best_fitness = []

for line in generation_data:
    generations.append(int(line[0].split("=")[1]))
    avg_fitness.append(round(float(line[2].split("=")[1]), 2))
    best_fitness.append(round(float(line[4].split("=")[1]), 2))

figure, axis = plt.subplots(1, 2)

axis[0].set_xticks(np.arange(0, max(generations), 5))
axis[1].set_xticks(np.arange(0, max(generations), 5))

axis[0].plot(generations, best_fitness)
axis[1].plot(generations, avg_fitness)

axis[0].set_xlabel("Generation")
axis[0].set_ylabel("Fitness function score")
axis[0].set_title("Best fitness per generation")

axis[1].set_xlabel("Generation")
axis[1].set_ylabel("Fitness function score")
axis[1].set_title("Average fitness per generation")

plt.tight_layout()
figure.savefig(f"plots/{task_name}_plots.png", dpi=300)


