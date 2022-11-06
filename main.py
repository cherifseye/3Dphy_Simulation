from vpython import *
TH = 400
TL = 339
T = Tinitial = TH



def adjust(temp):
    global TH
    if temp > TH: # small adjustments to eliminate e.g. '401 K' from displaying 
        return TH
    elif temp < 340:
        return 340
    else:
        return T

def showT():
    temp = adjust(T)
    thermometer.axis.y = temp*Tscale
    Tlabel.text = str(int(round(temp)))+' K'
    
def showomega():
    omegalabel.text = str(round(10.*L.z/Iwheel)/10.)+' rad/s'

winh=600
winw=600

scene = canvas(title="Carnot Cycle", width=winw, height=winh, x=0, y=0, align='left')
#PHYS172x = text(text='PHYS172x ',pos=vector(2,4,0),depth=0.1, height=0.15,color=color.blue)
label(pos=vector(-2,1.5,0), text='Click to step through the cycle', color=color.black,
        opacity=0, box=0, line=0)

thick = 0.1
wide = 1
deep = wide
high = 2
Lreservoir = 2*deep
offsetReservoir = 1.4*Lreservoir
Tscale = (0.7*high)/T
# monatomic gas
gamma = 1.4 
Rwheel = 0.8*wide
Iwheel = 10
Rpin = 0.8*Rwheel
theta = -0.9*pi/2
L = vector(0,0,0)
dt = 0.01
scene.background = color.white
scene.center = vector(0,0.8*high,0)
scene.forward = vector(0,-.3,-1)
scene.range = 3.5

cylcolor = vector(0.788,0.788,0.788)
pistoncolor = vector(1,0.704,0)
op = 0.2
bottom = box(pos=vector(0,-thick/2,0), size=vector(wide,thick,deep), color=cylcolor)
left = box(pos=vector(-wide/2-thick/2,high/2,-thick/2), size=vector(thick,high+2*thick,deep+thick),
           color=cylcolor, opacity=op)
right = box(pos=vector(wide/2+thick/2,high/2,-thick/2), size=vector(thick,high+2*thick,deep+thick),
            color=cylcolor, opacity=op)
back = box(pos=vector(0,high/2,-deep/2-thick/2), size=vector(wide,high+2*thick,thick),
           color=cylcolor, opacity=op)
front = box(pos=vector(0,high/2,deep/2+thick/2), size=vector(wide+2*thick,high+2*thick,thick),
            color=cylcolor, opacity=op)

wheel = cylinder(pos=vector(0,0,0), axis=vector(0,0,thick), radius=Rwheel, color=cylcolor)
axle = cylinder(pos=-vector(0,0,2*thick), axis=vector(0,0,3.5*thick), radius=thick/2, color=color.red)
pin = cylinder(pos=Rpin*vector(cos(theta),sin(theta),0), axis=vector(0,0,3*thick), radius=thick/2, color=color.red)
stripethick = 0.01
stripe1 = box(pos=vector(0,0,thick+stripethick/2), 
            size=vector(2*Rwheel,stripethick,stripethick), color=color.blue)
stripe2 = box(pos=vector(0,0,thick+stripethick/2), 
            size=vector(stripethick,2*Rwheel,stripethick), color=color.blue)
stripe1.rotate(angle=theta, axis=vector(0,0,1))
stripe2.rotate(angle=theta, axis=vector(0,0,1))
lifter = compound([wheel, axle, pin, stripe1, stripe2])
lifter.pos = vector(0,2*high,-2*thick)

piston = box(pos=vector(0,0.2*high+thick/2,0), size=vector(wide,thick,deep), color=pistoncolor)
pivot = cylinder(pos=piston.pos+vector(0,thick/2,-thick/2), axis=vector(0,0,thick), radius=thick/2, color=pistoncolor)
pinloc = vector(lifter.pos.x+Rpin*cos(theta),lifter.pos.y+Rpin*sin(theta),pivot.pos.z)
rod = cylinder(pos=vector(pivot.pos.x,pivot.pos.y,0), axis=pinloc-pivot.pos, radius=thick/5, color=pistoncolor)
Lrod = mag(rod.axis)          

thermometer = cylinder(pos=vector(bottom.pos.x+wide/2+thick/2,bottom.pos.y+thick,deep/2), radius=thick/5., axis=vector(0,T*Tscale,0), color=color.red)
sphere(pos=thermometer.pos, radius=thick/2, color=thermometer.color)
Tlabel = label(pos=vector(bottom.pos.x+wide/2+thick/2+thick,bottom.pos.y+high/2,deep/2), xoffset=10, 
                line=0, box=0, opacity=0, color=color.black, text=str(int(round(T)))+' K')
omegalabel = label(pos=lifter.pos+vector(Rwheel,0,0), xoffset=10, 
                line=0, box=0, opacity=0, color=color.black, text='0 rad/s', visible=False)

THreservoir = box(pos=bottom.pos+vector(0,-Lreservoir/2-thick/2,0), size=vector(Lreservoir,Lreservoir,Lreservoir), color=color.red)
THlabel = label(pos=THreservoir.pos + vector(0,0*0.4*Lreservoir,0*Lreservoir/2), text=str(int(round(adjust(TH))))+' K',
            color=color.white, opacity=0, box=0, line=0)
TLreservoir = box(pos=THreservoir.pos+vector(offsetReservoir,0,0), size=vector(Lreservoir,Lreservoir,Lreservoir), color=color.blue)
TLlabel = label(pos=TLreservoir.pos + vector(0,0.4*Lreservoir,Lreservoir/2), text=str(int(round(adjust(TL))))+' K',
            color=color.white, opacity=0, box=0, line=0)

graph(xtitle='V', ytitle='P', xmin=0.2, xmax=1.8, ymin=0, ymax=90, x=winw, width=400, height=scene.height, align='left')
PV = gcurve(color=color.red, dot=True, dot_color=color.black)

P = Pinitial = 80
showT()

Natoms = 50  # change this to have more or fewer atoms
Matom = 4E-3/6E23 # helium mass
Ratom = 0.03 # wildly exaggerated size of helium atom
k = 1.4E-23 # Boltzmann constant
Atoms = []
colors = [color.red, color.green, color.blue,
          color.yellow, color.cyan, color.magenta]
plist = []
mlist = []
offset = 1.1*Ratom

# average kinetic energy p**2/(2mass) = (3/2)kT
pavg = sqrt(2*Matom*1.5*k*TH)*(5E-5/dt) 

for i in range(Natoms):
    Lmin = -wide/2+offset
    Lmax = wide/2-offset
    x = Lmin+(Lmax-Lmin)*random()
    Lmin = bottom.pos.y+thick/2+offset
    Lmax = piston.pos.y-thick/2-offset
    y = Lmin+(Lmax-Lmin)*random()
    Lmin = -deep/2+offset
    Lmax = deep/2-offset
    z = Lmin+(Lmax-Lmin)*random()
    Atoms.append(sphere(pos=vector(x,y,z), radius=Ratom, color=colors[i % 6]))
    angle = pi*random()
    phi = 2*pi*random()
    px = pavg*sin(angle)*cos(phi)
    py = pavg*sin(angle)*sin(phi)
    pz = pavg*cos(angle)
    plist.append(vector(px,py,pz))
    mlist.append(Matom)

phase = 0
run = False
first = True
second = False
clicked = False
freerun = False
yinitial = 0

def getclick():
    global clicked
    clicked = True

scene.bind('click', getclick)

while True:
    rate(150)
    if not run or first:
        if clicked:
            clicked = False
            if first:
                run = False
                first = False
                second = True
                continue
            run = not first
    if run:
        torque = cross(pinloc-lifter.pos,P*norm(rod.axis)) # approximate force
        L = L + torque*dt
        omega = L.z/Iwheel
        dtheta = omega*dt
        if omega >= 4 and T <= 340:
            break
        theta += dtheta
        lifter.rotate(angle=dtheta, axis=vector(0,0,1))
        pinloc = vector(lifter.pos.x+Rpin*cos(theta),lifter.pos.y+Rpin*sin(theta),pivot.pos.z)
        
        deltay = sqrt(Lrod**2-pinloc.x**2)
        oldy = piston.pos.y-thick/2
        pivot.pos.y = pinloc.y-deltay
        piston.pos.y = pivot.pos.y-thick/2
        newy = piston.pos.y-thick/2
        Vratio = oldy/newy
        rod.pos = pivot.pos
        rod.axis = pinloc-rod.pos
        if phase == 1 or phase == 3: # isothermal
            P = P*Vratio
        else: # adiabatic
            P = P*Vratio**gamma
        T = Tinitial*(P*newy)/(Pinitial*yinitial)

        showT()
        showomega()
        PV.plot(pos=(newy,P))

    if phase == 0:
        oldy = newy = yinitial = piston.pos.y-thick/2
        PV.plot(pos=(newy,P))
        plotcolor = color.red
        clicked = False
        first = False
        run = False
        freerun = False
        phase = 1
    if phase == 1: # isothermal expansion
        if newy >= 1.1:
            phase = 2
            PV = gcurve(color=color.green, dot=True, dot_color=color.black)
            PV.plot(pos=(newy,P))
            if freerun:
                second = True
                continue
            else:
                run = False
                first = True
                continue
    elif phase == 2: # adiabatic expansion
        if second:
            THreservoir.pos.x -= offsetReservoir
            THlabel.pos.x -= offsetReservoir
            second = False
            continue
        if pinloc.x <= 0:
            phase = 3
            PV = gcurve(color=color.orange, dot=True, dot_color=color.black)
            PV.plot(pos=(newy,P))
            if freerun:
                second = True
                continue
            else:
                run = False
                first = True
                continue
    elif phase == 3: # isothermal compression
        if second:
            TLreservoir.pos.x -= offsetReservoir
            TLlabel.pos.x -= offsetReservoir
            second = False
            continue
        if newy <= yinitial*(Tinitial/T)**(1/(gamma-1)):
            phase = 4
            PV = gcurve(color=color.blue, dot=True, dot_color=color.black)
            PV.plot(pos=(newy,P))
            if freerun:
                second = True
                continue
            else:
                run = False
                first = True
                continue
    else: # adiabatic compression
        if second:
            TLreservoir.pos.x += offsetReservoir
            TLlabel.pos.x += offsetReservoir
            second = False 
            continue
        if T >= TH:
            phase = 1
            PV = gcurve(color=color.red, dot=True, dot_color=color.black)
            PV.plot(pos=(newy,P))
            run = True
            freerun = True
            omegalabel.visible = True
            first = False
            THreservoir.pos.x += offsetReservoir
            THlabel.pos.x += offsetReservoir
            continue
            
    # Update all positions of gas molecules
    psum = 0
    for i in range(Natoms):
        p = plist[i]
        pos = Atoms[i].pos + (p/mlist[i])*dt
        psum += mag(p)
        collide = False
        if not (-wide/2 < pos.x < wide/2):
            plist[i].x = -plist[i].x
            collide = True
        if not (bottom.pos.y+thick/2+offset < pos.y < piston.pos.y-thick/2-offset):
            plist[i].y = -plist[i].y
            # If piston headed downward, move atoms above the piston to just below the piston
            if newy < oldy and pos.y >= piston.pos.y-thick/2-offset:
                Atoms[i].pos.y = piston.pos.y-thick/2-offset
            collide = True
        if not (-deep/2 < pos.z < deep/2):
            plist[i].z = -plist[i].z
            collide = True
        if not collide:
            Atoms[i].pos = pos
    
    # Make sure the current average energy is consistent with the current temperature
    pavgnow = psum/Natoms
    for i in range(Natoms):
        plist[i] = plist[i]*sqrt(T/Tinitial)*(pavg/pavgnow)