import matplotlib.pyplot as plt
import numpy as np
import sys
import plotly.graph_objects as go


def main():
    """Creates a plot from TinyGP output format.

    run: python plot_tinygp_output.py <filename>

    file contents: 
        first row: <n_variables> <domain_lower_bound> <domain_upper_bound> <step>
        second row: the function as printed by tinygp

    
"""
    filename = sys.argv[1]

    with open(filename, "r") as f:
        X = []
        equation = None
        for i, line in enumerate(f):
            if i == 0:
                n_vars = int(line.strip().split()[0])
                if n_vars > 2:
                    raise ValueError("2 args max pls")

                a = int(line.strip().split()[1])
                b = int(line.strip().split()[2])
                step = float(line.strip().split()[3])
            elif i == 1:
                equation = line.strip()

                X = []
                for j in range(1, n_vars + 1):
                    equation = equation.replace(f"X{j}", f"X[{j-1}]")

                    X.append(np.arange(a, b, step))
            else:
                break
                    
        if n_vars == 1:
            Y = eval(equation)

            plt.figure()
            plt.plot(X[0], Y)
            plt.show()
        elif n_vars == 2:
            X[0], X[1] = np.meshgrid(X[0], X[1])

            Y = eval(equation)

            fig = go.Figure(data=[go.Surface(z=Y, x=X[0], y=X[1])])

            fig.update_layout(
                autosize=False,
                width=700,
                height=700,
                margin=dict(l=65, r=50, b=65, t=90),
                scene=dict(
                    xaxis_title='X Axis',
                    yaxis_title='Y Axis',
                    zaxis_title='Z Axis'
                )
            )

            fig.show()

if __name__ == "__main__":
    main()