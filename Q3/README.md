# Q3

## a

Consider a chemical reaction system consisting of substances $x,y,z,w,X,Y,Z,W$ that have the following reactions
(the number marked on the arrow is the reaction rate constant;
all the reactions are elementary reactions):

```math
\begin{align*}
y&\xrightarrow{\sigma}x,\\
x&\xrightarrow{\sigma}X\downarrow,\\
x&\xrightarrow{\rho}y,\\
x+z&\xrightarrow{1}w,\\
w+y&\xrightarrow{\infty}W\downarrow,\\
y&\xrightarrow{1}Y\downarrow,\\
x+y&\xrightarrow{1}z,\\
z&\xrightarrow{\beta}Z\downarrow.
\end{align*}
```

Then, the concentration of $x,y,z$ changes as follows:

```math
\dot x=\sigma y-\sigma x,\quad
\dot y=\rho x-xz-y,\quad
\dot z=xy-\beta z,
```

which is exactly the Lorenz system.
The physical meanings of the parameters $\sigma,\rho,\beta$ are the reaction rate constants.
