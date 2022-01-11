import time
import math
import CustomLib as Fcn

st=Fcn.step_time

input("Start")  # Wait for keyboard interrupt

time.sleep(2)   # Delay before robot starts moving

t=0
while t <8:     #Time counter, doesnt measure actual time and processing delays can affect, but not to a great extent over small runtimes.
    c = [Fcn.mux0(t % (6 * st)),Fcn.mux1(t % (6 * st)),Fcn.mux2(t % (6 * st)),Fcn.mux3(t % (6 * st))]
    for i in range(4):
        Fcn.SetC(i,c[i][0],c[i][1])
    t += .01
    time.sleep(.01) # Mimcks time jump of t+=.01

time.sleep(2)
Fcn.Rest()  #Brings down robot to resting postition
