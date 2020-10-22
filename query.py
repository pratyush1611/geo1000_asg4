# GEO1000 - Assignment 4
# Authors: Maundri Prihanggo & Pratyush Kumar
# Studentnumbers: 5151279 & 5359252

from reader import read
from geometry import Rectangle, Circle, Point
from os.path import basename


def parse(geom_str):
    """Parse a string into a shape object (Point, Circle, or Rectangle)

    Formats that can be given:
    p <px> <py>
    c <cx> <cy> <r>
    r <llx> <lly> <urx> <ury>
    
    Returns - Point, Circle, or Rectangle
    """
    geom = geom_str.split()

    #POINT
    if geom_str.startswith('p'):
        return Point(float(geom[1]), float(geom[2]) )
    #CIRCLE
    elif geom_str.startswith('c'):
        centerofcircle = Point(float(geom[1]), float(geom[2]) )
        return Circle(centerofcircle, float(geom[3]) )
    #RECTANGLE
    elif geom_str.startswith('r'):
        lowleft    = Point(float(geom[1]), float(geom[2]) )
        upperright = Point(float(geom[3]), float(geom[4]) )
        return Rectangle(lowleft, upperright)

def print_statistics(result):
    """Prints statistics for the resulting list of Points of a query
    
    * Number of points overlapping (i.e. number of points in the list)
    * The leftmost point and its identity given by the id function
    * The rightmost point and its identity given by the id function
    
    Returns - None
    """
    if len(result)>0:
        left = right = result[0]
        for point in result:
            if point.x < left.x or (point.x == left.x and point.y < left.y):
                left = point
            if point.x > right.x or (point.x == right.x and point.y > right.y):
                right = point
        print("""
+--------------+
+ Result       +
+--------------+""")
#TODO: add no of points
        print (len(result), "point(s)")
        print(f"leftmost : {left} id: {id(left)}")
        print(f"rightmost: {right} id: {id(right)}")
    else :
        not_found = """
+--------------+ 
+ Result   '^' + 
+--------------+ 
no overlapping points found inside the shape
"""
        print(not_found)

def print_help():
    """Prints a help message to the user, what can be done with the program.
    """
    helptxt = """
Commands available:
-------------------
General:
    help
    quit

Reading points in a structure, defining how many strips should be used:
    open <filenm> into <number_of_strips>

Querying:
    with a point:     p <px> <py>
    with a circle:    c <cx> <cy> <radius>
    with a rectangle: r <llx> <lly> <urx> <ury>"""
    print(helptxt)

# =============================================================================
# Below are some commands that you may use to test your codes:
# open points2.txt into 5
# p 5.0 5.0
# c 10.0 10.0 1.0
# r 2.0 2.0 8.0 4.0
# =============================================================================
def main():
    """The main function of this program.
    """
    structure = None
    print("Welcome to {0}.".format(basename(__file__)))
    print("=" * 76)
    print_help()

    while True:
        in_str = input("your command>>>\n").lower().strip()
    
        if in_str.startswith("quit"):
            print("Bye, bye.")
            return
    
        elif in_str.startswith("help"):
            print_help()
    
        elif in_str.startswith("open"):
            filenm, nstrips = in_str.replace("open ", "").split(" into ")
            structure = read(filenm, int(nstrips))
            structure.print_strip_statistics()
       
        elif in_str.startswith("p") or in_str.startswith("c") or in_str.startswith("r"):
       
            if structure is None:
                print("No points read yet, open a file first!")
       
            else:
                print_statistics(structure.query(parse(in_str)))

if __name__ == "__main__":
    main()
