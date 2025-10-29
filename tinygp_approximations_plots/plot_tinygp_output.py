from typing import Any, Optional
import matplotlib.pyplot as plt
import numpy as np
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from numpy import cos, sin, exp, log


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
                    equation = equation.replace("COS", "cos")
                    equation = equation.replace("SIN", "sin")
                    equation = equation.replace("EXP", "exp")
                    equation = equation.replace("LOG", "log")

                    current_var = []
                    start = a
                    while start <= b:
                        current_var.append(Variable(start))
                        start += step
                    X.append(np.array(current_var, dtype=object))
            elif i == 2:
                if line.strip() == "":
                    break
                    
                original_equation = line.strip()
                for j in range(1, n_vars + 1):
                    original_equation = original_equation.replace(f"X{j}", f"X[{j-1}]")
                    original_equation = original_equation.replace("COS", "cos")
                    original_equation = original_equation.replace("SIN", "sin")
                    original_equation = original_equation.replace("EXP", "exp")
                    original_equation = original_equation.replace("LOG", "log")
            else:
                break
                    
        if n_vars == 1:
            if original_equation is None:
                Y = eval(equation)

                plt.figure()
                plt.grid()
                plt.plot(X[0], Y)
                plt.savefig(f"{filename.replace(".txt", "").replace("examples", "plots")}.png")
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
                plt.savefig(f"{filename.replace(".txt", "").replace("examples", "plots")}.png")
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

                pio.write_html(
                    fig,
                    file=f"{filename.replace(".txt", "").replace("examples", "plots")}.html",
                    auto_open=False, # Set to True to open the file in your default browser immediately
                    include_plotlyjs='cdn' # Use 'cdn' for a smaller file size (requires internet to load the JS)
                                        # or use 'full' (default) for a completely offline, standalone file.
)
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

                pio.write_html(
                    fig,
                    file=f"{filename.replace(".txt", "").replace("examples", "plots")}.html",
                    auto_open=False, # Set to True to open the file in your default browser immediately
                    include_plotlyjs='cdn' # Use 'cdn' for a smaller file size (requires internet to load the JS)
                                        # or use 'full' (default) for a completely offline, standalone file.
                )


class Variable:
    def __init__(self, value):
        self.value = value

    def __array__(self, dtype: Optional[np.dtype] = None) -> np.ndarray:
        return np.array(self.value, dtype=dtype)
    
    def __float__(self):
        return self.value

    def __add__(self, other):
        if isinstance(other, Variable):
            return Variable(self.value + other.value)
        else:
            return Variable(self.value + other)
    
    def __radd__(self, other):
        return Variable(self.value + other)
    

    def __sub__(self, other):
        if isinstance(other, Variable):
            return Variable(self.value - other.value)
        else:
            return Variable(self.value - other)
    
    def __rsub__(self, other):
        return Variable(other - self.value)
    
    def __mul__(self, other):
        if isinstance(other, Variable):
            return Variable(self.value * other.value)
        else:
            return Variable(self.value * other)
    
    def __rmul__(self, other):
        return Variable(self.value * other)
    
    def __truediv__(self, other):
        if isinstance(other, Variable):
            if np.abs(other.value) <= 0.001:
                return Variable(self.value)
            else:
                return Variable(self.value / other.value)
        else:
            if np.abs(other) <= 0.001:
                return Variable(self.value)
            else:
                return Variable(self.value / other)
    
    def __rtruediv__(self, other):
        if np.abs(self.value) <= 0.001:
            return Variable(other)
        else:
            return Variable(other / self.value)

    def __array_ufunc__(self, ufunc: np.ufunc, method: str, *inputs: Any, **kwargs: Any) -> Any:
        if method != '__call__' or 'out' in kwargs:
            return NotImplemented

        unwrapped_inputs = tuple(x.value if isinstance(x, Variable) else x for x in inputs)
        
        result = ufunc(*unwrapped_inputs, **kwargs)
        
        if np.isscalar(result):
            return Variable(result)
        else:
            return result
    
    def to_plotly_json(self):
        return self.value

    def sin(self):
        return Variable(np.sin(self.value))

    def cos(self):
        return Variable(np.cos(self.value))
    
    def exp(self):
        return Variable(np.exp(self.value))
    
    def log(self):
        return Variable(np.log(self.value))

if __name__ == "__main__":
    main()