from visual import *
from visual.graph import *
from math import *

scene = display( title="Oscillating Sliding Mass", range=(50,50,50), autoscale=0, width=700, height=700)

# Acceleration due to gravity near Earth's surface
g = vector(0,-9.80665,0)

#Initial conditions
"""
theta0 = -0.087542937411
omega0 = -0.241665
r0 = -4.01562349524
v0 = -11.2637378021
alpha = 2
m=20
"""
"""
theta0 = 0.334182871668
omega0 = -0.180513
r0 = 15.8781818109
v0 = -8.86123062263
alpha = 2
"""
"""
theta0 = pi/6
omega0 = 0
r0 = 25.490644
v0 = 0
alpha = 2
m=20
"""

#--------------------------
"""
theta0 = 0.552165391964
omega0 = -0.291905
r0 = 17.6178863019
v0 = -10.5864885254
alpha = 0.5
"""

"""
theta0 = math.pi/4
omega0 = 0
r0 = 26.81632831772
v0 = 0
alpha = 0.5
m=20
"""
"""
theta0 = 0.347651772474
omega:0 = -0.405456
r0 = 10.6362405553
v0 = -13.1057162035
alpha  = 0.5
"""

#---------------------------
theta0=-0.001
omega0=0
r0=15.675253
v0=-10
alpha=0.5
m=1

scene2 = display(title="Phase Space", xtitle="Displacement", xmin=-r0, xmax=r0, ytitle="Momentum")
phase = gcurve(color=color.red)

# Polar unit vector
rhat = vector(cos(theta0),sin(theta0),0)

# Block inital conditions
block = box(size=(10,10,10), color=color.yellow, opacity=0.85, axis=rhat, make_trail=True)
block.mass = m
block.radius = r0
block.pos = block.radius * rhat
block.speed = v0
block.velocity = block.speed * rhat
block.inertia = block.mass * (block.length**2 + block.height**2 + 12* block.radius**2) / 12

# Board initial conditions
board = box(size=(100,5,5), color=color.red, opacity=0.3, axis=rhat)
midpoint = cylinder(axis=(0,0,board.width+0.5), radius=board.height/4)
board.mass = alpha * m             # mass
board.inertia = board.mass * (board.length**2 + board.height**2) / 12 # Moment of inertia I = m(a^2+b^2)/12 for a rectangular plate
board.theta = theta0
board.omega = vector(0,0,omega0)        # angular velocity

dt = 1e-5
t = 0

while (t<1000):
    rate(100000)
    t += dt
        
    #if (floor(t) % 2 == 0):
    #    phase.color = color.red
    #else:
    #    phase.color = color.blue
    
    phase.plot(pos=(block.radius,block.speed*block.mass))
    
    # Force Calculations
    Fg = block.mass * g                 # Force of gravity on block
    #print "Fg: " + str(Fg)
    T = cross(block.pos, Fg)            # Torque on board
    #print "T: " + str(T)
    Fr = comp(Fg, rhat)                 # Radial component of gravity
    #print "Fr: " + str(Fr)
    
    # Update angular components
    # Mass and moment of inertia are constant
    board.omega += dt * T / (board.inertia + block.inertia)# update angular velocity of board
    #print "omega: ", str(board.omega)
    dtheta = dt * board.omega           # omega = dtheta/dt
    #print "dtheta: ", str(dtheta)
    if (board.omega[2] < 0):
        board.theta -= mag(dtheta)      # update angular displacement of board
    else:
        board.theta += mag(dtheta)
    #print "theta: ", str(board.theta)

    # Update radial components
    # Mass is constant
    block.speed += dt * Fr / block.mass
    block.velocity = block.speed * rhat
    #print "speed: ", str(block.speed)
    dr = dt * block.velocity
    if (block.speed < 0):
        block.radius -= mag(dr)
    else:
        block.radius += mag(dr)
        
    # Update axes
    rhat = vector(cos(board.theta),sin(board.theta),0)
    board.axis = board.length * rhat
    block.axis = block.length * rhat

    block.pos = block.radius * rhat # update radial displacement of block
    block.inertia = block.mass * (block.length**2 + block.height**2 + 12* block.radius**2) / 12
    #print "position: ", str(block.radius)

    #if (abs(block.pos[0] +4) < 5e-4):
     #   print "theta: ", board.theta
      #  print "omega: ", board.omega
      #  print "r: ", block.radius
       # print "v: ", block.speed
        #print "alpha: ", alpha
        #print "\n"

    
    # Test for block going off the board
    if mag(block.pos) > board.length / 2:
        print "Block fell off at ", t, "seconds"
        print "Initial Conditions"
        print "Angle: ", theta0
        print "Position: ", r0
        print "Mass of block: ", m
        print "Mass constant: ", alpha
        break
