# GEO1000 - Assignment 4
# Authors: Maundri Prohanggo & Pratyush Kumar
# Studentnumbers: 5151279 & 5359252
#%%
import math
#%%
# __all__ leaves out _test method and only makes
# the classes available for "from geometry import *":
__all__ = ["Point", "Circle", "Rectangle"] 


class Point(object):

    def __init__(self, x, y):
        """Constructor. 
        Takes the x and y coordinates to define the Point instance.
        """
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        """Returns WKT String "POINT (x y)".
        """
        return( f"POINT ({self.x} , {self.y})" )

    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        returns - True / Falses
        """
        if isinstance(other, Point): #point class
            return(True if(other.x==self.x and other.y==self.y ) else False)   #trur if intersects
        elif isinstance(other, Circle): #circle class 
            #compute dist b/w points if >radius => good
            return( True if( self.distance(other.center) <= other.radius) else False )
        elif isinstance(other, Rectangle): #remains rectangle class
            return( True if((self.x >= other.ll.x and self.x <= other.ur.x ) or (self.y >= other.ll.y and self.y <= other.ur.y )) else False )

    def distance(self, other):
        """Returns cartesian distance between self and other Point
        """
        return( math.sqrt( (self.y - other.y)**2 + (self.x - other.x)**2) )


class Circle(object):

    def __init__(self, center, radius):
        """Constructor. 
        Takes the center point and radius defining the Circle.
        """
        assert radius > 0
        assert isinstance(center, Point)
        self.center = center
        self.radius = float(radius)

    def __str__(self):
        """Returns WKT str, discretizing the boundary of the circle 
        into straight line segments
        """
        N = 400
        step = 2 * math.pi / N
        pts = []
        for i in range(N):
            pts.append(Point(self.center.x + math.cos(i * step) * self.radius, 
                             self.center.y + math.sin(i * step) * self.radius))
        pts.append(pts[0])
        coordinates = ["{0} {1}".format(pt.x, pt.y) for pt in pts]
        coordinates = ", ".join(coordinates)
        return "POLYGON (({0}))".format(coordinates)

    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        Returns - True / False
        """
        if isinstance(other, Point):
            return( other.intersects(self) )
        elif isinstance(other, Circle):
            return( other.center.intersects(self) )
        elif isinstance(other, Rectangle):
            ll = other.ll
            ur = other.ur
            lr = Point(other.ur.x , other.ll.y)
            ul = Point(other.ll.x , other.ur.y)
            r = self.radius
            #check for if circle is in/on the rectangle corners
            if(ll.intersects(self)):
                return( True )
            if(lr.intersects(self)):
                return( True )
            if(ur.intersects(self)):
                return( True )
            if(ul.intersects(self)):
                return( True )
            # condition if the circle lies within the rectangle
            if(self.center.intersects(other)):
                return(True) 
            # TODO: check if the circle is about to approach and intersect the corner
            # perpendicular distance from line should be > radius
            # or 4 outer rectangles can be defined using coordinates mix with the radius of the circle
            r_b=Rectangle(Point(ll.x , ll.y- r ) , lr)
            r_u=Rectangle(ul , Point( ur.x, ur.y + r))
            r_r=Rectangle(lr , Point(lr.x+r ,ur.y ))
            r_l=Rectangle(Point( ll.x-r, ll.y) , ul)
            
            if(self.center.intersects(r_b)):
                return(True)
            if(self.center.intersects(r_u)):
                return(True)
            if(self.center.intersects(r_r)):
                return(True)
            if(self.center.intersects(r_l)):
                return(True)
                
            else:
                return(False)

class Rectangle(object):

    def __init__(self, pt_ll, pt_ur):
        """Constructor. 
        Takes the lower left and upper right point defining the Rectangle.
        """
        assert isinstance(pt_ll, Point)
        assert isinstance(pt_ur, Point)
        self.ll = pt_ll
        self.ur = pt_ur

    def __str__(self):
        """Returns WKT String "POLYGON ((x0 y0, x1 y1, ..., x0 y0))"
        """
        return( f"POLYGON (( {self.ll.x} {self.ll.y}, {self.ur.x} {self.ll.y}, {self.ur.x} {self.ur.y}, {self.ll.x} {self.ur.y}, {self.ll.x} {self.ll.y}, ))" )


    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        Returns - True / False
        """
        if isinstance(other , Point):
            return(other.intersects(self))
        elif isinstance(other, Circle):
            return(other.intersects(self))
        elif isinstance(other, Rectangle): #using Separating Axis Theorem
            return not (self.ur.x < other.ll.x or self.ll.x > other.ur.x or self.ur.y < other.ll.y or self.ll.y > other.ur.y)

    def width(self):
        """Returns the width of the Rectangle.
        
        Returns - float
        """
        #width = delta x
        return( float(self.ur.y - self.ll.y) )

    def height(self):
        """Returns the height of the Rectangle.
        
        Returns - float
        """
        #width = delta x
        return( float(self.ur.x - self.ll.x) )


def _test():
    """Test whether your implementation of all methods works correctly.
    """
    pt0 = Point(0, 0)
    pt1 = Point(0, 0)
    pt2 = Point(10, 10)
    assert pt0.intersects(pt1)
    assert pt1.intersects(pt0)
    assert not pt0.intersects(pt2)
    assert not pt2.intersects(pt0)

    c = Circle(Point(-1, -1), 1)
    r = Rectangle(Point(0,0), Point(10,10))
    assert not c.intersects(r)

    # Extend this method to be sure that you test all intersects methods!
    # Read Section 16.5 of the book if you have never seen the assert statement


if __name__ == "__main__":
    _test()

