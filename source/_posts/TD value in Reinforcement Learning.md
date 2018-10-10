---
title: How to calculate TD(lam) in Reinforcement Learning
author: Li-Ke Ma
date: 2018-10-09
category: Computer Science
tags: Reinforcement Learning
---

Estimating state value in reinforcement learning is a hard task, since the sample process is very noisy. $TD(\lambda)$ learning try to take as much information as possible to estimate the state value. In this note, I will briefly give the derivation of $TD(\lambda)$ and its pseudo-code for computing. 

<!-- toc -->

---
# Definitions in Reinforcement Learning
We mainly regard reinforcement learning process as a Markov Decision Process(MDP): an agent interacts with environment by making decisions at every step/timestep, gets to next state and receives reward. This makes a state-action chain like 
$$
\mathbf{s}_0 \rightarrow \mathbf{a}_0 \rightarrow r_0 \rightarrow \mathbf{s}_1 \rightarrow \cdots, 
$$
Where $\mathbf{s}_t$ represents the agent's state at time $t$, $\mathbf{a}_t$ represents the decision made by agent at time t with its state $\mathbf{s}_t$, $r_t$ represents the reward agent received between states $\mathbf{s}_t$ and $\mathbf{s}_{t+1}$ after action $\mathbf{a}_t$ was taken.

To evaluate the quality of policy $\pi(\mathbf{a}_t|\mathbf{s}_t)$, accumulated reward for state $\mathbf{s}_T$ with decay ratio $\gamma$ is defined as following:
$$
R(\mathbf{s}_T) = \mathbf{E}_{\mathbf{a}_t \sim \pi(\mathbf{a}_t|\mathbf{s}_t) } \left[\sum_{t = T}^{\infty} \gamma^{t-T} r_t\right].
$$

Also, the $Q$ value for state $\mathbf{s}_T$ after taking action $\mathbf{a}_T$ is defined as 
$$
Q(\mathbf{s}_T, \mathbf{a}_T) = \mathbf{E}_{\mathbf{a}_t \sim \pi(\mathbf{a}_t|\mathbf{s}_t) } \left[r_T + \sum_{t = T+1}^{\infty} \gamma^{t-T} r_t\right].
$$

---
# Bellman Equation and Update Rules
Assume we have an accurate estimation of accumulated reward $R$ of policy $\pi(\mathbf{a}_t|\mathbf{s}_t)$, denoted by $V_\pi^*$, then we will have a equilibrium like:
$$
V_\pi^*(\mathbf{s}_t) = \mathbf{E}_{\mathbf{a}_t \sim \pi(\mathbf{a}_t|\mathbf{s}_t) } \left[r_t + \gamma V_\pi^*(\mathbf{s}_{t+1}) \right]
$$
or
$$
Q_\pi^*(\mathbf{s}_t, \mathbf{a}_t) = \mathbf{E}_{\mathbf{a}_{t+1} \sim \pi(\mathbf{a}_{t+1}|\mathbf{s}_{t+1}) } \left[r_t + \gamma Q_\pi^*(\mathbf{s}_{t+1}, \mathbf{a}_{t+1}) \right].
$$

However, the accurate estimation is exactly what we don't know, so we need to improve the accuracy of our estimation based on current samples. Assume we have a series of functions $V_\pi^{(n)}$ to approach to $V_\pi^*$, then we can update the function by
$$
V_\pi^{(n+1)}(\mathbf{s}_t) = \mathbf{E}_{\mathbf{a}_t \sim \pi(\mathbf{a}_t|\mathbf{s}_t) } \left[r_t + \gamma V_\pi^{(n)}(\mathbf{s}_{t+1}) \right].
$$

---
# Derivation of $TD(\lambda)$

## $TD(n)$ learning
From a chain of samples, we can update the state value by 
$$
V(\mathbf{s}_t) \leftarrow r_t + \gamma V(\mathbf{s}_{t+1}).
$$
But how about other states in the chian? The Bellman equation can be also written as any of the followings:
$$
\begin{split}
V_\pi^*(\mathbf{s}_t) &= \mathbf{E}_{\mathbf{a}_t \sim \pi(\mathbf{a}_t|\mathbf{s}_t) } \left[r_t + \gamma r_{t+1} + \gamma^2 V_\pi^*(\mathbf{s}_{t+2}) \right] \\
V_\pi^*(\mathbf{s}_t) &= \mathbf{E}_{\mathbf{a}_t \sim \pi(\mathbf{a}_t|\mathbf{s}_t) } \left[r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \gamma^3 V_\pi^*(\mathbf{s}_{t+2}) \right]  \\
&\cdots
\end{split}
$$

Define $G_t^{(n)}$ as estimated state value considering $n$ step further.
$$
\begin{split}
G_t^{(1)} &= r_t + \gamma V(\mathbf{s}_{t+1}) \\
G_t^{(2)} &= r_t + \gamma r_{t+1} + \gamma^2 V(\mathbf{s}_{t+2}) \\
&\cdots \\
G_t^{(n)} &= r_t + \gamma r_{t+1} + ... + \gamma^n V(\mathbf{s}_{t+n}) \\
\end{split}
$$

Using $G^{(n)}$ to update value can take $n$ steps into account, we call this $TD(n)$ learning (Temporal Difference Learning). 

## $TD(\lambda)$ learning
What if we make a combination of all these $G^{(n)}$ ? By weighted averaging, we can get $G^{(\lambda)}$ as unbiased estimation of $R$, and takes all information into consideration.
$$
G_t^{(\lambda)} = (1-\lambda) \sum_{n=1}\lambda^{n-1} G_t^{(n)}
$$

So, how to calculate $G_t^{(\lambda)}$ when we know the sample chain $\{\mathbf{s}_0, \mathbf{a}_0, r_0, \mathbf{s}_1, \cdots\}$? Here is the formula derivation. (Lemma: $G_t^{(n)} = r_t + \gamma G_{t+1}^{(n-1)}$, I leave the proof for readers.)
$$
\begin{split}
	G_t^{(\lambda)} &= (1-\lambda) \sum_{n=1}\lambda^{n-1} G_t^{(n)} \\
	&=(1-\lambda) \sum_{n=1}\lambda^{n-1} ( r_t + \gamma G_{t+1}^{(n-1)}) \\
	&= (1-\lambda)\gamma G_{t+1}^{(0)} + r_t +  \lambda \gamma (1-\lambda) \sum_{n=1}\lambda^{n-1} G_{t+1}^{(n-1)} \\
	&= (1-\lambda)\gamma V_{t+1} + r_t + \lambda \gamma  G_{t+1}^{(\lambda)} \\
	&= G_t^{(1)} + \lambda \gamma (G_{t+1}^{(\lambda)} - V_{t+1})
\end{split}
$$

Define advantage function $\delta_t^{(n)} = G_t^{(n)} - V_t$, we can get the recurrent relation
$$
\delta_t^{(\lambda)} = \delta_t^{(1)} + \lambda \gamma  \delta_{t+1}^{(\lambda)}
$$

---
# Psudo Code for Computing $TD(\lambda)$ 
When we have a sample chain 
$$
\mathbf{s}_0 \rightarrow \mathbf{a}_0 \rightarrow r_0 \rightarrow \mathbf{s}_1 \rightarrow \mathbf{a}_1 \rightarrow r_1 \rightarrow \cdots \mathbf{s}_{n-1} \rightarrow  \mathbf{a}_{n-1} \rightarrow r_{n-1} \rightarrow \mathbf{s}_{end}
$$
 ```python
def TD_lambda(s, r, value_func, gamma, lam):
"""
    Inputs:
	    s    list of states 
	    r    list of rewards
	    value_func    function predict accumulated reward for state
	    gamma     reward decal factor
	    lam       TD(lam) parameter
	Outputs:
	    TD_lam    list of TD(lam) value for each state
"""
    for i in range(n):
        V[i] = value_func(s[i])  # compute predicted value for each state

	V[n] = 0 if (s[n] is END) else value_func(s[n]) # predicted value for end state
	delt_lam[n] = 0

	for i in reversed(range(n)): # calculate in reversed order 
	    # calculate delt(1) for each state
	    delt_1[i] = r[i] + gamma * V[i+1] - V[i]  
	    # calculate delt(lam) for each state
	    delt_lam[i] = delt_1[i] + gamma * lam * delt_lam[i+1] 
	    # calculate TD(lam) for each state
	    TD_lam[i] = delt_lam[i] + V[i]

	return TD_lam
 ```
# Reference
1. Wikipedia Page: [Temporal difference learning](https://en.wikipedia.org/wiki/Temporal_difference_learning)
2. Alister Reis's blog: [Reinforcement Learning: Eligibility Traces and TD(lambda)](https://amreis.github.io/ml/reinf-learn/2017/11/02/reinforcement-learning-eligibility-traces.html)
3. David Silver's [slides](http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching_files/MC-TD.pdf)
4. Richard S. Sutton's paper of TD(lam): [Learning to predict by the methods of temporal differences]()
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTgzNDg4NzU4OCw1NDUyNzM2NzAsMTM4MT
U0NDU1LC0xMDgwOTU2MTMxLDExNzI3NDI1NTAsMjg0NjUwMDI4
LC0yMDkzOTQxMTUsLTk2Mjg3NjcxNSwtMTkzNzEwNjMxMCw0Nz
YxMjg3MCwtMTQyNDE0MTg4OSwxMTc0OTI5OTA3LC0xMTk3Mzc4
NTg4LC0xOTcwMzk5NjM5LDE2MTkwNzk2OTMsLTY1MTc1MjM2NS
w3MjU5ODM0MzUsLTEzNzkzODIyNTYsNDE3MDQ0MDcsMTU1MjQ1
MTM1NV19
-->