# GEO1000 - Assignment 4
# Authors: Maundri Prihanggo & Pratyush Kumar
# Studentnumbers: 5151279 & 5359252

from geometry import Point, Rectangle, Circle
from strips import StripStructure


def read(file_nm, no_strips):
    """Reads a file with on the first uncommented line a bbox 
    (4 numbers separated by a space) and subsequently 0 or more lines with 
    points (2 numbers separated by a space) into a Strip Structure.
    
    If no valid box is found in the input file, it returns None.
    Otherwise a StripStructure with 0 or more points is returned.
    
    Returns - None or a StripStructure instance
    """
    with open ("points2.txt", 'r') as file_nm:
        line = [c for c in file_nm.readlines() if not c.startswith('#')]
        bbox = (line[0].strip().split())
        if len(bbox) == 4 :
            if bbox [2] > bbox [0] and bbox [3] > bbox [1] : 
                a = []
                b = StripStructure(Rectangle(Point(bbox[0], bbox[1]), Point(bbox[2], bbox[3])), no_strips)
                for i in range (1,len(list(line))):
                    a.append(line[i].strip().split(" "))
                for j in a:
                    b.append_point(Point(i[0], i[1]))
                return b
        else :
            return None


def dump(structure, strip_file_nm="strips.wkt", point_file_nm="points.wkt"):
    """Dump the contents of a strip structure to 2 files that can be opened
    with QGIS.
    
    Returns - None
    """
    with open(strip_file_nm, "w") as fh:
        fh.write(structure.dump_strips())
    with open(point_file_nm, "w") as fh:
        fh.write(structure.dump_points())
    
