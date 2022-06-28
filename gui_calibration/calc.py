from math import sin, cos, tan


x = 1114
y = 4337
theta = -1.733


x2 = (x/cos(theta)) + (y - x*tan(theta))*sin(theta)
y2 = (y - x*tan(theta))*cos(theta)

print(x2*0.05)
print(y2*0.05)
