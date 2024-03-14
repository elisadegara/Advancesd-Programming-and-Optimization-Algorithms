import numpy as np
import cvxpy as cp


#######
# DATA, do not change this part!
#######
a=[0.5, -0.5, 0.2, -0.7, 0.6, -0.2, 0.7, -0.5, 0.8, -0.4]
l=[40, 20, 40, 40, 20, 40, 30, 40, 30, 60]
Preq=np.arange(a[0],a[0]*(l[0]+0.5),a[0])
for i in range(1, len(l)):
    Preq=np.r_[ Preq, np.arange(Preq[-1]+a[i],Preq[-1]+a[i]*(l[i]+0.5),a[i]) ]

T = sum(l)

Peng_max = 20.0
Pmg_min = -6.0
Pmg_max = 6.0
eta = 0.1
gamma = 0.1
#####
# End of DATA part
#####

# Implement the following functions
# they should return a dictionary retval such that
# retval['Peng'] is a list of floats of length T such that retval['Peng'][t] = P_eng(t+1) for each t=0,...,T-1
# retval['Pmg'] is a list of floats of length T such that retval['Pmg'][t] = P_mg(t+1) for each t=0,...,T-1
# retval['Pbr'] is a list of floats of length T such that retval['Pbr'][t] = P_br(t+1) for each t=0,...,T-1
# retval['E'] is a list of floats of length T+1 such that retval['E'][t] = E(t+1) for each t=0,...,T

def car_with_battery():
    Ebatt_max = 100.0
    

    # Variables
    Peng = cp.Variable(T)
    Pmg = cp.Variable(T)
    Pbr = cp.Variable(T)
    E = cp.Variable(T+1)
    epsilon = 1e-4

    obj = 0

    #constraints
    constraints = [E[T] == E[0]]

    for i in range(T): 
        constraints += [Preq[i] == Peng[i] + Pmg[i] - Pbr[i],
                      Peng[i] >= 0, Peng[i] <= Peng_max,
                      Pmg[i] >= Pmg_min, Pmg[i] <= Pmg_max,
                      Pbr[i] >= 0,
                      E[i] >= 0, E[i] <= Ebatt_max,
                      eta * Pmg[i] <= -E[i+1] + E[i] - Pmg[i], 
                      eta * Pmg[i] >= E[i+1] - E[i] + Pmg[i]] 
        obj += cp.sum(Peng[i] + gamma * cp.square(Peng[i]) + epsilon * cp.maximum(0, - Pmg[i]))


    # Solve the problem
    prob = cp.Problem(cp.Minimize(obj), constraints)
    prob.solve(solver = cp.ECOS, abstol=1e-8, reltol=1e-8)
    
    retval = {}
    retval['Peng'] = list(Peng.value)
    retval['Pmg'] = list(Pmg.value)
    retval['Pbr'] = list(Pbr.value)
    retval['E'] = list(E.value)

    return retval

    # Note that the problematic constraint is E(t+1) == E(t) - Pmg(t) - eta*|Pmg(t)|,
    # so we need to relax it to E(t+1) <= E(t) - Pmg(t) - eta*|Pmg(t)|.
    # We can write it as eta*|Pmg(t)| <= -E(t+1) + E(t) - Pmg(t).
    # Then , splitting the absolute value, we obtain:
    # -(-E(t+1) + E(t) - Pmg(t)) <= eta*Pmg(t) <= -E(t+1) + E(t) - Pmg(t)
    # that is eta*Pmg(t) <= -E(t+1) + E(t) - Pmg(t) and eta*Pmg(t) >= E(t+1) - E(t) + Pmg(t).

    # We are relaxing the contraint but the solution does not change, since the problem will try to make this constraint tight.
    # Indeed, relaxing the constraint, we let the battery discharge but we do not require it to recharge when not in use.
    # Since our objective is to minimize the total fuel consumption, the solver will still try to keep the battery level as high as possible,
    # so that we are reducing the power we require to the combustion engine.
    # In fact, since we are trying to minimize Peng(t) + gamma*(Peng(t))^2 and Peng >= 0 for every t, we will try to minimize Peng(t).
    # This is the same as saying that we are minimizing Preq(t) - Pmg(t) + Pbr(t), by the first constraint.
    # Since Preq(t) is fixed for every t and Pbr(t) is non negative, we will try to minimize - Pmg(t), that is to maximize Pmg(t).
    # Consider the relaxed constraint E(t+1) <= E(t) - Pmg(t) - eta*|Pmg(t)|, that is eta*|Pmg(t)| + Pmg(t) <= -E(t+1) + E(t).
    # The problem will try to make it tight since we are maximixing Pmg(t). Indeed, consider the left hand side of the inequality:
    # when Pmg(t) >= 0, eta*|Pmg(t)| + Pmg(t) == eta*Pmg(t) + Pmg(t), therefore if we maximize Pmg(t) we maximize this sum trying to make this constraint tight;
    # when Pmg(t) < 0, eta*|Pmg(t)| + Pmg(t) == -eta*Pmg(t) + Pmg(t) == (1 - eta)*Pmg(t) where 1 - eta > 0, so again if we maximize Pmg(t) we maximize (1 - eta)*Pmg(t) trying to make this constraint tight.
    # In both cases, the left hand side will be maximized, trying to make the inequality tight.





def car_without_battery():
    Ebatt_max = 0

    # Variables
    Peng = cp.Variable(T)
    Pmg = cp.Variable(T)
    Pbr = cp.Variable(T)
    E = cp.Variable(T+1)
    epsilon = 1e-4

    obj = 0

    #constraints
    constraints = [E[T] == E[0]]

    for i in range(T): 
        constraints += [Preq[i] == Peng[i] + Pmg[i] - Pbr[i],
                      Peng[i] >= 0, Peng[i] <= Peng_max,
                      Pmg[i] >= Pmg_min, Pmg[i] <= Pmg_max,
                      Pbr[i] >= 0,
                      E[i] >= 0, E[i] <= Ebatt_max,
                      eta * Pmg[i] <= -E[i+1] + E[i] - Pmg[i], 
                      eta * Pmg[i] >= E[i+1] - E[i] + Pmg[i]] 
        obj += cp.sum(Peng[i] + gamma * cp.square(Peng[i]) + epsilon * cp.maximum(0, - Pmg[i]))


    # Solve the problem
    prob = cp.Problem(cp.Minimize(obj), constraints)
    prob.solve(solver = cp.ECOS, abstol=1e-8, reltol=1e-8, feastol = 1e-10)
    

    retval = {}
    retval['Peng'] = list(Peng.value)
    retval['Pmg'] = list(Pmg.value)
    retval['Pbr'] = list(Pbr.value)
    retval['E'] = list(E.value)

    return retval

    # When we set Ebatt_max to 0, the battery is removed from the system, which means that there is no longer any energy storage available.
    # In this case, the optimal solution shows that the fuel consumption increases,
    # since the car requires the generation of more and more power to run.
    # This is expected, since there is no longer any battery to provide a reserve of power, so the combustion engine has to compensate.


