---
title: Finite Element Method for Soft Deformable Object Simulation
date: 2016-09-29
category: Computer Science
title_banner: https://d3gyiijzpk1c44.cloudfront.net/upload/product_photos/base/0/39/92/original1.2579507.2.jpg

---

# Introduction
This note is based on SIGGRAPH course of 2012, which introduced basic techniques to simulate elastic material using FEM.

<!-- toc -->


---
# Elastisity in 3D

## Deformation and deformation gradient
$X \in \Omega$ is the location of material in undeformed position, and the deformation function $\phi: R^3 \to R^3$ transfer material to its current position.

define deformation gradient $F$ as:
$$
	F = \frac{\partial(\phi_1, \phi_2, \phi_3)}{\partial(X_1, X_2, X_3)}, \\
	F_{ij} = \frac{\partial \phi_i}{\partial X_j}
$$

e.x. when the material is on its rest position, $F = I$

## Strain energy and hyperelasticity
the deformation energy is defined as
$$
	E[\phi] = \int_{\Omega} \Psi[\phi; X] dX
$$

since the local property is fully defined by deformation gradient
$$
	\phi(X) = \phi(X_*) + F(X_*) \cdot (X - X_*) = F(X_*) \cdot X + (\phi(X_*) - F(X_*) \cdot X_*) =  F(X_*) \cdot X + t_*
$$

thus we can write $\Psi[\phi; X] = \Psi[F]$, there are many energy models such as 
$$
	\Psi[F] = \frac{k}{2} ||F||^2_F,  \\
	\Psi[F] = \frac{k}{2} ||F - I||^2_F
$$

## Force and traction
Since $f = -\frac{\partial E}{\partial x}$, the force inner and on boundaries are defined:

- for the volume force, $f_{aggreagte}(A) = \int_A f(X) dX, A \subset \Omega$
- for the surface force, $f_{aggreagte}(B) = \int_B \tau(X) dS, B \subset \partial \Omega$

## First Piola-Kirchhoff stress tensor
$P$ is a $3\times3$ tensor, defined as
$$
	P[F] = \frac{\partial \Psi[F]}{\partial F}
$$

- $\tau = - P \cdot N \iff \tau_j = - P_{ij} N_i$
- $f = \nabla_X \cdot P \iff f_i = \frac{\partial P_{ij}}{\partial X_j}$

the formula can be derived by calculus of variations
$$
\begin{split}
\delta E &= \delta \left[\int_\Omega \Psi[F] dX \right] 
	= \int_\Omega \delta \Psi[F] dX 
	=  \int_\Omega  \left[ \frac{\partial \Psi[F]}{\partial F} : \delta F \right] dX 
	=  \int_\Omega [P : \delta F] dX \\
 &= \int_\Omega P_{ij} \delta F_{ij} dX = \int_\Omega P_{ij} \frac{\partial \delta \phi_i}{\partial X_j} dX \\
 &= \int_\Omega \frac{\partial}{\partial X_j}(P_{ij} \delta \phi_i) -  \frac{\partial P_{ij}}{\partial X_j} \delta \phi_i dX \\
 &=  - \int_\Omega \frac{\partial P_{ij}}{\partial X_j} \delta \phi_i dX + \int_{\partial \Omega} P_{ij} N_j \delta \phi_i dS \\
 &= -  \int_\Omega f_i  \delta \phi_i dX - \int_{\partial \Omega} \tau_i \delta \phi_i dS \\
 \end{split}
$$

---
# Constitutive Models of Material

## Strain Measures
Think of $\Psi(F) = ||F-I||^2_F$, this form of deform energy is not zero when $F$ is just a rigid rotation, so there is another measure to describe the deformation, named Green strain tensor
$$
	E = \frac{1}{2} (F^TF - I) 
$$

the Green strain tensor can handle both rest and rigid rotation situation.

## Linear Elasticity Model
When $F$ is a small disturb, 
$$
	\delta E |_{F = I} = \frac{1}{2} (\delta F^TF + F^T\delta F ) =   \frac{1}{2} (\delta F^T + \delta F )
$$

$$
	\epsilon = E(F) \approx \frac{1}{2} ( F^T + F ) - I
$$
then the terms of the strain energy density is
$$
	\Psi(F) = \mu \epsilon : \epsilon +\frac{\lambda}{2} tr^2(\epsilon) \\
	P(F) = 2\mu \epsilon + \lambda tr(\epsilon)I
$$

## St. Vernan-Kickoff Model
When the deformation is large and $F$ can no longer be represented by $\epsilon$, then the energy density is
$$
	\Psi(F) = \mu E: E +\frac{\lambda}{2} tr^2(E) \\
	P(F) = F[2\mu E + \lambda tr(E)I]
$$

There is a vital problem of StVK model, that when the material is compressed, the resistant force may decrease when deformation exceeds a threshold. This may results in the fail of the model.

e.x. For a tetrahedron defined by $O(0, 0, 0), A(1, 0, 0), B(0,1,0), C(0,0,1)$, when $C$ is compressed along z-axis by ratio $l$, the energy on it becomes $\Psi = (\mu + \frac{\lambda}{2} )(\frac{l^2}{2} - 1)^2$, and the force becomes $f= - (\mu + \frac{\lambda}{2} )(l^2 - 2)l$
 
## Corotation Model
Another way to handle rotation is to polar decompose $F = RS$ and compute $\Psi(F) = \Psi(S)$. However, since the decomposition is costly, corotation model is not used widely.

## Isotropic Model
An ideal energy function $\Psi(F)$ should remain const when a rigid rotation applied to $F$, namely $\Psi(RF) = \Psi(F)$. An isotropic model has another property that when the material coordinate rotate, the energy density remains const (isotropic), namely $\Psi(FQ) = \Psi(F)$. $F$ can be SVD decomposite to $U^T \Sigma V$, then $\Psi(F) = \Psi(\Sigma) = \Psi(\lambda_1, \lambda_2, \lambda_3)$

there is another way to represent $\Psi$ by invariant 
$$
\begin{split}
I_1 &= tr(F^TF) = tr(\Sigma^2) = \sum_{i=1}^3 \lambda^2_i \\
I_2 &= tr(F^TFF^TF) = tr(\Sigma^4) = \sum_{i=1}^3 \lambda^4_i \\
I_3 &= det(F^TF) = \prod_{i=1}^3 \lambda^2_i 
\end{split}
$$

$$
	P(F) =  \frac{\partial \Psi}{\partial I_1} 2F+  \frac{\partial \Psi}{\partial I_2} 4FF^TF + \frac{\partial \Psi}{\partial I_3} 2I_3 F^{-T}
$$

## Neo-hookean Model
In order to get over compress problems of StVK model, we can introduce $\log |F|$ into energy density to punish its compression. Neo-hookean model is a specific type of isotropic model.

$$
	\Psi(I_1. I_3) = \frac{\mu}{2}(I_1 - \log{I_3} - 3) + \frac{\lambda}{8} \log^2{I_3} \\
	P(F) = \mu(F -F^{-T}) + \frac{\lambda}{2} \log{I_3} F^{-T}
$$

--- 
# Dynamics and Simulation

When we want to simulate the interaction of objects in computer, we get tetrahedron mesh representation of objects. Thus we model the whole continue material as piece-wise linear.
For each tetrahedron we can compute a const $F$ and then using 
$$
	f = - \frac{\partial E}{\partial x} =  - \frac{\partial E}{\partial F}  \frac{\partial F}{\partial x} = - P \frac{\partial F}{\partial x}
$$ 

## Algorithms for Elastic Force
Deformation gradient $F$ in each tetrahedron is uniform
$$
	F [X_1 - X_4, X_2 - X_4, X_1 - X_4]= [x_1 - x_4, x_2 - x_4, x_3 - x_4] 
$$
$$
F = D_s \cdot B_m \\
	D_s = [x_1 - x_4, x_2 - x_4, x_3 - x_4] , \\
	B_m =  [X_1 - X_4, X_2 - X_4, X_1 - X_4]^{-1}
$$
there is a small tip for force computing:
$$
	H = [f_1, f_2, f_3] =  P(F) \cdot B_m^T
$$
```python
def precompute():
	for each tetrahedron t:
		Dm = [X1 - X4, X2 - X4, X3 - X4]
		t.Bm = inverse(Dm)
		t.V = determinant(Dm)

def computeForce():
	for each tetrahedron t:
		Ds = [x1 - x4, x2 - x4, x3 - x4]
		F = Ds * t.Bm
		H = P(F) * t.Bm.transpose()
		f1 += H[:,0], f2 += H[:,1], f3 += H[:,2]
		f4 -= H[:,0] + H[:,1] + H[:,2]

```

## Algorithms for Stiffness Differential
The influence of $\delta x$ on $f$ for a single tetrahedron can be $12 \times 12$ matrix, since the 3-dim force on 4 vertices can be influenced by 3-dim position of 4 vertices. There is a way to compute this matrix column by column:

$$
	\delta H = [\delta f_1 , \delta f_2, \delta f_3] = \delta P(F, \delta F) \cdot B_m^T \\
	\delta P (F, \delta F) = P(F+\delta F) - P(F)
$$

since $\delta P (F, \delta F)$ is linear for $\delta F$, namely $\delta P (F, \lambda \delta F) =\lambda \delta P (F, \delta F)$, we can feed different $\frac{\partial F}{\partial x_{ij}}$ into it. Where $x_{ij}$ is the $i$ th element of $j$ th vertex

$$
	F_{ij} = \frac{\partial F}{\partial x_{ij}} = 
	\begin{cases} 
		\delta_{ij}, &i = \{1, 2, 3\}, j \leq 3 \\
		 -\delta_{i1} -\delta_{i2} -\delta_{i3},  &i = \{1, 2, 3\}, j = 4
		 \end{cases}
$$

```python
def computeGradient():
	for each tetrahedron t:
		Ds = [x1 - x4, x2 - x4, x3 - x4]
		F = Ds * t.Bm
		for dF in F_ij:
			dH = dP(F, dF) * t.Bm.transpose()
			K(f1, x_ij) += dH[:,0]
			K(f2, x_ij) += dH[:,1]
			K(f3, x_ij) += dH[:,2]
			K(f4, x_ij) -= dH[:,0] + dH[:,1] + dH[:,2]
```

the method used in *FEM simulation of 3D deformable solids: a practitioner's guide to theory [1]* is implicit, namely they only computing $\delta f(x, \delta x)$, and then using iterative methods like conjugate gradient.

However, I introduce a method to compute stiffness matrix explicitly, for the reason that iterative methods are too sloooooow. According to my experiment in practice, implemented in Eigen, CG method is slower than simple Newton Method in a magnitude of $10^2$ (3600 seconds vs 20 seconds )! So, I strongly recommend you to construct stiffness explicitly and use standard sparse linear algebra tools.

## Dynamic Equation 
The movement of objects obey Newton's law
$$
	M \ddot{x} = f_{sum}(x, v) 
$$ 

$$
\begin{cases}
	\dot{x} = v \\
	M \dot{v} = f_{sum}(x, v)	
\end{cases}
$$

$$
\begin{cases}
	x_{t+1}  = x_t + \Delta t \cdot v_t \\
	v_{t+1} = v_t + \Delta t \cdot M^{-1} f_{sum}(x_t, v_t)	
\end{cases}
$$

using backward Euler method
$$
\begin{cases}
	x_{t+1}  = x_t + \Delta t \cdot v_{t+1} \\
	v_{t+1} = v_t + \Delta t \cdot M^{-1} f_{sum}(x_{t+1}, v_{t+1})	
\end{cases}
$$

for each time step $\Delta t$, we need to try the solutions $(x_{t+1}, v_{t+1})$ for backward Euler equation iteratively until converge, denoted as $\{ x_{t+1}^{(0)}, x_{t+1}^{(1)}, ..., x_{t+1}^{(k)}, ...\}$. Each iteration, we estimate $ f_{sum}(x_{t+1}^{(k+1)}, v_{t+1}^{(k+1)})$ by Taylor series approximation on $(x_{t+1}^{(k)}, v_{t+1}^{(k)})$

define $\Delta x = x_{t+1}^{(k+1)} - x_{t+1}^{(k)}, \Delta v =  v_{t+1}^{(k+1)} - v_{t+1}^{(k)}$, then we can get:

$$
\begin{split}
	f_{sum}(x_{t+1}^{(k+1)}, v_{t+1}^{(k+1)}) &= f_{sum}(x_{t+1}^{(k)} + \Delta x, v_{t+1}^{(k)} + \Delta v) \\
	&\approx f_{sum}(x_{t+1}^{(k)} , v_{t+1}^{(k)}) -K \Delta x + \gamma K \Delta v
	\end{split}
$$
where $K = -\frac{\partial f_{elas}}{\partial x}\bigg|_{x = x_{t+1}^{(k)}}, K_{damp} = \frac{\partial f_{elas}}{\partial v}\bigg|_{x = x_{t+1}^{(k)}} =-\gamma K$

since $v_{t+1}^{(k+1)} = v_{t+1}^{(k)} + \Delta v = v_{t+1}^{(k)} + \frac{\Delta x}{\Delta t}$

$$
	v_{t+1}^{(k)} + \frac{\Delta x}{\Delta t} = v_t  + \Delta t \cdot M^{-1} \left(f_{sum}(x_{t+1}^{(k)}, v_{t+1}^{(k)}) -K \Delta x + \gamma K \frac{\Delta x}{\Delta t}\right) 
$$

then we can get the linear equation of $\Delta x = x_{t+1}^{(k+1)} - x_{t+1}^{(k)}$. Solve it, update, and enter next iteration, until converge.
$$
	\left[\frac{1}{\Delta t} - \Delta t \cdot  (1 -  \frac{\gamma}{\Delta t}) M^{-1} K\right] \Delta x= v_t -v_{t+1}^{(k)} + \Delta t \cdot M^{-1} f_{sum}(x_{t+1}^{(k)}, v_{t+1}^{(k)})
$$

---
# Reference
[1] Sifakis E, Barbic J. FEM simulation of 3D deformable solids: a practitioner's guide to theory, discretization and model reduction[C]//ACM SIGGRAPH 2012 Courses. ACM, 2012: 20.
<!--stackedit_data:
eyJoaXN0b3J5IjpbNDU5ODAwMTUzLC03ODM5ODk3NzBdfQ==
-->