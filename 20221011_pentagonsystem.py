import numpy as np
import cv2

def getline(x0, y0, x1, y1):
  points = []
    
  if abs(x1 - x0) >= abs(y1-y0): #slope is less than 1
    #formula to check the slope of the line
    if x0 < x1:  
      for x in range(x0,x1+1):
        y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
        yint = int(y)
        points.append((x, yint))
        
    else:
      for x in range(x1, x0-1):
        y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
        yint = int(y)
        points.append((x, yint))
    return points

  else: #slope is greater than one
    if y0 < y1:  
      for y in range(y0,y1+1):
        x = (y - y0) * (x1 - x0) / (y1 - y0) + x0
        xint = int(x)
        points.append((xint, y))

    else:
      for y in range(y1, y0-1):
        x = (y - y0) * (x1 - x0) / (y1 - y0) + x0
        xint = int(x)
        points.append((xint, y))
    return points

def drawline(canvas, x0,y0,x1,y1, color=(255,255,255)):
  xys = getline(x0,y0,x1,y1)
  for xy in xys:
    x, y = xy
    canvas[y,x, :] = color
  return

def drawLinePQ(canvas, p, q, color):
  drawline(canvas, p[0], p[1], q[0], q[1], color)
  return

def deg2rad(deg):
  rad = deg * np.pi/180
  return rad

def getregularpolygon(N):
  delta_degree = 360./N
  points = []
  for i in range(N):
    degree = i*delta_degree
    radian = deg2rad(degree)
    x = np.cos(radian)
    y = np.sin(radian)
    points.append((x,y,1))

  points = np.array(points)
  return points

def drawPolygon(canvas, pts, color = (255,255,255), axis=False):
  for k in range(pts.shape[0]-1):
    drawline(canvas, pts[k,0], pts[k,1], pts[k+1,0], pts[k+1, 1], color)

  drawLinePQ(canvas, pts[-1], pts[0], color)

  if axis == True: # center - pts[0]
    center = np.mean(pts, axis=0).astype('int')
    drawLinePQ(canvas, center, pts[0], color=(0, 128, 128))

  return

def makeRmat(degree):
  r = deg2rad(degree)
  c, s = np.cos(r), np.sin(r)
  Rmat = np.eye(3,3)
  Rmat[0,0] = c
  Rmat[0,1] = -s
  Rmat[1,0] = s
  Rmat[1,1] = c
  return Rmat
  
  #return np.array([[c,-s, 0], [s,c, 0], [0, 0, 1]])

def makeTmat(a,b):
    #return np.array([[1,0,0], [0,1,0], [a, b, 1]])
    Tmat = np.eye(3,3)
    Tmat[0,2] = a
    Tmat[1,2] = b
    return Tmat

def getcentre(pts):
  center = np.mean(pts, axis=0).astype('int')
  return np.array(center)
  
def drawpentagon(theta, scale, canvas, color=(255,255,255)):
  points = getregularpolygon(5)
  points = points*scale
  points[:,2] = 1

  T = makeTmat(canvas.shape[0]/2, canvas.shape[1]/2)
  R = makeRmat(theta)

  Q = R @ points.T
  Q = (T @ Q).T

  Q = Q.astype('int')
  drawPolygon(canvas, Q, color, axis=True)

def drawstar(canvas, pts, color = (100,100,100)):
  drawLinePQ(canvas, pts[0], pts[2], color)
  drawLinePQ(canvas, pts[2], pts[4], color)
  drawLinePQ(canvas, pts[4], pts[1], color)
  drawLinePQ(canvas, pts[1], pts[3], color)
  drawLinePQ(canvas, pts[3], pts[0], color)

def star(alpha,beta, scale, canvas, len,  color=(255,255,255)):
  points = getregularpolygon(5)
  points = points*scale
  points[:,2] = 1

  T = makeTmat(canvas.shape[0]/2, canvas.shape[1]/2)
  T1 = makeTmat(len, 0)
  R1 = makeRmat(alpha)
  R2 = makeRmat(-alpha)
  R3 = makeRmat(beta)

  S_transformations = T @ R1 @ T1 @ R3 @ R2  
  S = (S_transformations @ points.T).T 

  S = S.astype('int')
  
  drawstar(canvas, S, color)
  return np.array(S)

def planet(alpha,gamma, scale, canvas, len, h, color=(255,255,255)):
  points = getregularpolygon(6)
  points = points*scale
  points[:,2] = 1

  T = makeTmat(canvas.shape[0]/2, canvas.shape[1]/2)
  T1 = makeTmat(len, h)
  R1 = makeRmat(alpha)
  R2 = makeRmat(-alpha)
  R3 = makeRmat(gamma)

  M_transformations = T @ R1 @ T1 @ R3 @ R2
  M = (M_transformations @ points.T).T 

  M = M.astype('int')
  
  drawPolygon(canvas, M, color)

def main():
  width = 700
  height = 700
  window = np.zeros((height, width, 3), dtype = 'uint8')

  theta = 5
  len = 200
  h = 70
  alpha = 6
  beta = 6
  gamma = 50

  while True:
    drawpentagon(theta, 100, window)
    star(alpha, beta, 35, window, len, color = (100,100,100))
    planet(alpha, gamma, 10, window, len, h, color = (250,0,0))
    
    cv2.imshow("window",window)

    theta += 4
    alpha += 3
    beta += 8
    gamma += 5

    window = np.zeros((height, width, 3), dtype = 'uint8')

    if cv2.waitKey(50) == 27: break
    
    
main()





