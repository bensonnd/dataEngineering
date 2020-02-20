import math

class Points(object):
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __sub__(self, no):
        subvar = Points((self.x - no.x), (self.y - no.y), (self.z - no.z))
        return subvar

    def dot(self, no):
        dotvar = (self.x * no.x) + (self.y * no.y) + (self.z * no.z)
        return dotvar

    def cross(self, no):
        crossvar = Points((self.y * no.z - self.z * no.y), (self.z * no.x - self.x * no.z), (self.x * no.y - self.y * no.x))
        return crossvar

    def absolute(self):
        powvar = pow((self.x ** 2 + self.y ** 2 + self.z ** 2), 0.5)
        return powvar


#if __name__ == '__main__':
input_var = ['-1 2 5', '8 2 -10', '1 6 -8', '9 5 3']
points = list()
for i in input_var:
    a = list(map(float, i.split()))
    points.append(a)

a, b, c, d = Points(*points[0]), Points(*points[1]), Points(*points[2]), Points(*points[3])
x = (b - a).cross(c - b)
y = (c - b).cross(d - c)
angle = math.acos(x.dot(y) / (x.absolute() * y.absolute()))

print("%.2f" % math.degrees(angle))