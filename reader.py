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
    with open (file_nm, 'r') as fh:
        lines_without_comment = [c for c in fh.readlines() if not c.startswith('#')]
        bbox = (lines_without_comment[0].strip().split())
        if len(bbox) == 4 : # there are exactly 2 coordinates in bbox
            if bbox [2] > bbox [0] and bbox [3] > bbox [1] : # ll and ul are satisfied
                structure = StripStructure(Rectangle(Point(bbox[0], bbox[1]), Point(bbox[2], bbox[3])), no_strips)
                points_list = [i.split() for i in lines_without_comment[1:]]
                for pt in points_list:
                    structure.append_point(Point(pt[0], pt[1]))
                return structure

            else:
                return None
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
    
