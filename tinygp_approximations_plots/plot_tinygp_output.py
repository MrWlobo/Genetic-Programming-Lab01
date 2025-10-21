import matplotlib.pyplot as plt
import numpy as np
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    """Creates a plot from TinyGP output format.

    run: python plot_tinygp_output.py <filename>

    file contents: 
        first row: <n_variables> <domain_lower_bound> <domain_upper_bound> <step>
        second row: the function as printed by tinygp
        third row (optional): the original function

    
    """
    filename = sys.argv[1]

    with open(filename, "r") as f:
        X = []
        equation = None
        original_equation = None
        for i, line in enumerate(f):
            if i == 0:
                n_vars = int(line.strip().split()[0])
                if n_vars > 2:
                    raise ValueError("2 args max pls")

                a = float(line.strip().split()[1])
                b = float(line.strip().split()[2])
                step = float(line.strip().split()[3])
            elif i == 1:
                equation = line.strip()

                X = []
                for j in range(1, n_vars + 1):
                    equation = equation.replace(f"X{j}", f"X[{j-1}]")

                    X.append(np.arange(a, b, step))
            elif i == 2:
                if line.strip() == "":
                    break
                    
                original_equation = line.strip()
                for j in range(1, n_vars + 1):
                    original_equation = original_equation.replace(f"X{j}", f"X[{j-1}]")
            else:
                break
                    
        if n_vars == 1:
            if original_equation is None:
                Y = eval(equation)

                plt.figure()
                plt.grid()
                plt.plot(X[0], Y)
                plt.savefig("plot.png")
                plt.show()
            else:
                Y = eval(equation)
                Y_original = eval(original_equation)

                fig, ax = plt.subplots(1, 2)
                ax[0].plot(X[0], Y)
                ax[0].set_title("TinyGP")
                ax[0].grid()
                ax[1].plot(X[0], Y_original)
                ax[1].set_title("Original")
                ax[1].grid()
                plt.savefig("plot.png")
                plt.show()
        elif n_vars == 2:
            if original_equation is None:
                X[0], X[1] = np.meshgrid(X[0], X[1])

                Y = eval(equation)
                # Y = np.clip(Y, -5, None)

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
            else:
                X[0], X[1] = np.meshgrid(X[0], X[1])

                Y = eval(equation)
                # Y = np.clip(Y, -300, None)
                Y_original = eval(original_equation)

                fig = make_subplots(
                    rows=1, cols=2, 
                    specs=[[{'is_3d': True}, {'is_3d': True}]],
                    subplot_titles=("TinyGP", "Original")
                )

                fig.add_trace(
                    go.Surface(z=Y, x=X[0], y=X[1], colorscale='Viridis', showscale=False),
                    row=1, col=1
                )

                fig.add_trace(
                    go.Surface(z=Y_original, x=X[0], y=X[1], colorscale='Plasma', showscale=True),
                    row=1, col=2
                )

                fig.update_layout(
                    height=550, 
                )

                fig.show()
                
                

if __name__ == "__main__":
    main()