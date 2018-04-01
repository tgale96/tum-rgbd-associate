import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def mult(q0, q1, q2, q3, r0, r1, r2, r3):
    return [r0*q0 - r1*q1 - r2*q2 - r3*q3,
            r0*q1 + r1*q0 - r2*q3 + r3*q2,
            r0*q2 + r1*q3 + r2*q0 - r3*q1,
            r0*q3 - r1*q2 + r2*q1 + r3*q0]

def conj(q0, q1, q2, q3):
    return [q0, -q1, -q2, -q3]

def norm(q0, q1, q2, q3):
    return q0**2 + q1**2 + q2**2 + q3**2

def inv(q0, q1, q2, q3):
    n = norm(q0, q1, q2, q3)
    c = conj(q0, q1, q2, q3)
    return [float(x) / n for x in c]

def rotate(x, y, z, w, p, q, r):
    tmp = mult(w, p, q, r, 0, x, y, z)
    i = inv(w, p, q, r)
    res = mult(tmp[0], tmp[1], tmp[2], tmp[3], i[0], i[1], i[2], i[3])
    return res[1:]

def magnitude(x, y, z):
    return (x**2 + y**2 + z**2)**(0.5)
    
# x, y, z, w, p, q, r = 1.3434, 0.6271, 1.6606, 0.6583, 0.6112, -0.2938, -0.3266

# x2, y2, z2 = rotate(x, y, z, w, p, q, r)

# x3, y3, z3 = rotate(0, 0, 0, w, p, q, r)
# x3, y3, z3 = x3+x, y3+y, z3+z

# # Rotation on origin stays the same
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter([0, x, x2, x3], [0, y, y2, y3], [0, z, z2, z3])
# plt.show()

# # Rotation is magnitude preserving
# x, y, z = 1, 1, 1
# print((x, y, z))
# print(magnitude(x, y, z))
# x, y, z = rotate(x, y, z, w, p, q, r)
# print((x, y, z))
# print(magnitude(x, y, z))
