import numpy as np

def lerp(A, B, t):#linear interpolation
  return A + (B-A)*t

def getIntersection(A,B,C,D):
  tTop = (D["x"]-C["x"])*(A["y"]-C["y"]) - (D["y"]-C["y"])*(A["x"]-C["x"]) 
  uTop = (C["y"]-A["y"])*(A["x"]-B["x"]) - (C["x"]-A["x"])*(A["y"]-B["y"]) 
  bottom = (D["y"]-C["y"])*(B["x"]-A["x"]) - (D["x"]-C["x"])*(B["y"]-A["y"])

  if(bottom!=0):
    t = tTop/bottom
    u = uTop/bottom
    if(t>=0 and t<=1 and u>=0 and u<=1): 
      return {"x":lerp(A["x"], B["x"], t), 
              "y":lerp(A["y"], B["y"], t),
              "offset":t
            }
  return None

def polysIntersect(poly1, poly2):#This method works because compares each segment forming the polygon
  for i in range(0, len(poly1)):
    for j in range(0, len(poly2)):
      touch = getIntersection(
        poly1[i],
        poly1[(i+1)%len(poly1)],
        poly2[j],
        poly2[(j+1)%len(poly2)]
      )
      if touch is not None:
        return True
  return False

def getRGBA(value):
  alpha = int(np.floor(np.abs(value)*255))
  R = 0 if value<0 else 255
  G=R
  B = 0 if value>0 else 255
  return (R, G, B, alpha)
