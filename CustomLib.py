import board
import time
import busio
import math
import adafruit_pca9685

A=2
B=3
ph=-8
w=20
a = float(6)
b = float(7)
pi = math.pi
phase=0

stride = 2          # Parameters that charcterise the movement
step_time = .2
pi = math.pi
stride_height = 1
rest_height = 7
x_offset = -2

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)   #Initialise the interface, scl and sda values correspond to the connections on pi pico board
pca = adafruit_pca9685.PCA9685(i2c)             #Initialise the Servo Driver over the i2c interface
pca.frequency = 50                              #Set frequency of the PWM of pca board
data = [                                        #References each port on the pca board and sets the calibration values of the servos on each leg
    [pca.channels[0], 1800, 8400, 0],
    [pca.channels[1], 8600, 1800, 0],
    [pca.channels[2], 2000, 8800, 0],
    [pca.channels[3], 7950, 1250, 0],
    [pca.channels[4], 8000, 1200, 0],
    [pca.channels[5], 1600, 8350, 0],
    [pca.channels[6], 8800, 2200, 0],
    [pca.channels[7], 2300, 9200, 0],
]

for i in range(8):
    data[i][3] = (data[i][2] - data[i][1]) / 180    #Set degrees per duty cycle

def convert(coord):                                 #Accepts coordinate values and return corresponding servo degree values
    x = coord[0]
    y = coord[1]
    cosphi = (x * x + y * y - a * a - b * b) / (2 * a * b)
    phi = math.acos(cosphi)
    dnmtr = math.sqrt(a * a + b * b + 2 * a * b * cosphi)
    cosalpha = (a + b * cosphi) / dnmtr
    alpha = math.acos(cosalpha)
    cosbeta = -x / dnmtr
    beta = math.acos(cosbeta)
    theta = beta - alpha
    return [theta * 180 / pi, phi * 180 / pi]

def SetD(mno, deg):   #The job of this function is to make sure the angles are always between certain limits, so that the limbs wont hit each other
    if mno%2 ==1:
        deg+=3
    if mno % 4 == 0:  # 0 4
        if deg < 5:
            deg = 5
        if deg > 135:
            deg = 135
    elif mno % 4 == 2:  # 2 6
        if deg > 90:
            deg = 90
        if deg < 0:
            deg = 0
    else:  # 1 3 5 7
        if deg > 160:
            deg = 160
        if deg < 0:
            deg = 0
    vlu = int(data[mno][1] + deg * data[mno][3])    #Gets the value to set the duty cycle to for the corresponding angle deg
    data[mno][0].duty_cycle = vlu


def SetC(limb, xc, yc):     #Converts the coordinated xc and yc to the corresponding angles and sends that information to SetD function
    ang = convert([float(xc), float(yc)])
    limb = int(limb)        # Corresponds to the limb in order R1, R2, L1, L2
    SetD(limb * 2, ang[0])
    SetD(limb * 2 + 1, ang[1])



def Alpha(t):              # Function generator of Alpha function
    return [
        (t * 2 * stride / step_time) % (2 * stride) - stride + x_offset,
        abs(stride_height * math.sin(t * pi / step_time)) - rest_height,
    ]


def Beta10(t):             # Function generator of Beta10 function
    return [stride - (t * stride / step_time) % (stride) + x_offset, -rest_height]


def Beta01(t):             # Function generator of Beta0(-1) function
    return [-(t * stride / step_time) % (stride) - stride + x_offset, -rest_height]


def Gamma1(t):             # Function generator of Gamma1 function
    return [stride + x_offset, -rest_height]


def Gamma0(t):             # Function generator of Gamma0 function
    return [0 + x_offset, -rest_height]


def Gamma_1(t):            # Function generator of Gamma(-1) function
    return [-stride + x_offset, -rest_height]


def mod(t2):               # Converts time into a step function for the multiplexer functions
    if t2 < 1 * step_time:
        return 1
    elif t2 < 2 * step_time:
        return 2
    elif t2 < 3 * step_time:
        return 3
    elif t2 < 4 * step_time:
        return 4
    elif t2 < 5 * step_time:
        return 5
    elif t2 < 6 * step_time:
        return 6


def mux2(t1):                   # Multiplexer functions that cut and combine the base movements into the pattern for each limb
    n = mod(t1)
    if n <= 1:                  #mux0 - R1
        return Alpha(t1)        #mux1 - R2
    elif n <= 2:                #mux2 - L1
        return Gamma1(t1)       #mux3 - L2
    elif n <= 3:
        return Beta10(t1)
    elif n <= 4:
        return Gamma0(t1)
    elif n <= 5:
        return Gamma0(t1)
    elif n <= 6:
        return Beta01(t1)


def mux3(t1):
    n = mod(t1)
    if n <= 1:
        return Gamma0(t1)
    elif n <= 2:
        return Gamma0(t1)
    elif n <= 3:
        return Beta01(t1)
    elif n <= 4:
        return Gamma_1(t1)
    elif n <= 5:
        return Alpha(t1)
    elif n <= 6:
        return Beta10(t1)


def mux0(t1):
    n = mod(t1)
    if n <= 1:
        return Gamma0(t1)
    elif n <= 2:
        return Gamma0(t1)
    elif n <= 3:
        return Beta01(t1)
    elif n <= 4:
        return Alpha(t1)
    elif n <= 5:
        return Gamma1(t1)
    elif n <= 6:
        return Beta10(t1)


def mux1(t1):
    n = mod(t1)
    if n <= 1:
        return Gamma_1(t1)
    elif n <= 2:
        return Alpha(t1)
    elif n <= 3:
        return Beta10(t1)
    elif n <= 4:
        return Gamma0(t1)
    elif n <= 5:
        return Gamma0(t1)
    elif n <= 6:
        return Beta01(t1)

def Rest():                 # Sets the robot down in a resting position
    for i in range(4):
        SetD(2 * i, 20)
        SetD(2 * i + 1, 150)

