from vpython import *

pos1 = vector(0, 0, 0)
pos2 = vector(-3, 4, 0)
fix_sphere = sphere(pos=pos1, radius=0.5, color=color.green)
movingsphere = sphere(pos=pos2, radius=0.5, color=color.cyan)
pointer = arrow(pos=pos1, axis=pos2-pos1)

while pos2.x <= 10:
    rate(5)
    movingsphere.pos = pos2
    pointer.axis = pos2 - pos1
    pos2.x += 1