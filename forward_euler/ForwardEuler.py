# ForwardEuler.py
#
# Fixed-stepsize forward Euler stepper class implementation file.
#
# Class to perform fixed-stepsize time evolution of the IVP
#      y' = f(t,y),  t in [t0, Tf],  y(t0) = y0
# using the forward Euler (explicit Euler) time stepping method.
#
# D.R. Reynolds
# Math 6321 @ SMU
# Fall 2023
import numpy as np

class ForwardEuler:
    """
    Fixed stepsize forward Euler class

    The two required arguments when constructing a ForwardEuler object
    are a function for the IVP right-hand side, and a stepsize to use:
        f = ODE RHS function with calling syntax f(t,y).
        h = optional input with stepsize to use for time stepping.  Note
            that this MUST be set either here on in the Evolve call.
    """
    def __init__(self, f, h=0.0):
        # required inputs
        self.f = f
        self.h = h
        # internal data
        self.steps = 0

    def forward_euler_step(self, t, y):
        """
        Usage: t, y, success = forward_euler_step(t, y)

        Utility routine to take a single forward Euler time step,
        where the inputs (t,y) are overwritten by the updated versions.
        If success==True then the step succeeded; otherwise it failed.
        """
        y += self.h * self.f(t,y)
        t += self.h
        self.steps += 1
        return t, y, True

    def reset(self):
        """ Resets the accumulated number of steps """
        self.steps = 0

    def get_num_steps(self):
        """ Returns the accumulated number of steps """
        return self.steps

    def Evolve(self, tspan, y0, h=0.0):
        """
        Usage: Y, success = Evolve(tspan, y0, h)

        The fixed-step forward Euler evolution routine

        Inputs:  tspan holds the current time interval, [t0, tf], including any
                     intermediate times when the solution is desired, i.e.
                     [t0, t1, ..., tf]
                 y holds the initial condition, y(t0)
                 h optionally holds the requested step size (if it is not
                     provided then the stored value will be used)
        Outputs: Y holds the computed solution at all tspan values,
                     [y(t0), y(t1), ..., y(tf)]
                 success = True if the solver traversed the interval,
                     false if an integration step failed [bool]
        """
        import numpy as np

        # set time step for evoluation based on input-vs-stored value
        if (h != 0.0):
            self.h = h

        # verify that tspan values are separated by multiples of h
        for n in range(tspan.size-1):
            hn = tspan[n+1]-tspan[n]
            if (abs(round(hn/self.h) - (hn/self.h)) > 100*np.sqrt(np.finfo(h).eps)*abs(self.h)):
                print("input values in tspan (%e,%e) are not separated by a multiple of h = %e" % (tspan[n],tspan[n+1],h))
                return y0, False

        # initialize output, and set first entry corresponding to initial condition
        y = y0.copy()
        Y = np.zeros((tspan.size,y0.size))
        Y[0,:] = y

        # loop over desired output times
        for iout in range(1,tspan.size):

            # determine how many internal steps are required
            N = int(round((tspan[iout]-tspan[iout-1])/self.h))

            # reset "current" (t,y) that will be evolved internally
            t = tspan[iout-1]

            # iterate over internal time steps to reach next output
            for n in range(N):

                # perform forward Euler update
                t, y, success = self.forward_euler_step(t, y)
                if (not success):
                    print("forward_euler error in time step at t =", t)
                    return Y, False

            # store current results in output arrays
            Y[iout,:] = y.copy()

        # return with "success" flag
        return Y, True