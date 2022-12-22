
#if no value is given in the brackets, it will be set to 3 as default

def getRegularPolygon(N=3):
    points = []

    delta_degree = 360./N
    points = []
    for i in range(N):
        degree = delta_degree * i
        radian = degree * np.pi/360
        x = np.cos(degree)
        y = np.sin(degree)

        points.append((x,y))

    return np.array(points)

'''

Geometric transformations

Euclidean Transformation --> rotation, translation

E + isotropic scaling = similarity transformation

E + simple scaling in both directions + sharing = affine transformation

affine transf + perspective transformation = projective transformation

'''
