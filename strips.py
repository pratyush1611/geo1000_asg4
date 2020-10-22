# GEO1000 - Assignment 4
# Authors: Maundri Prihanggo & Pratyush Kumar
# Studentnumbers: 5151279 & 5359252

from geometry import Point, Rectangle


class Strip(object):
    def __init__(self, rectangle):
        """Constructor. Inits a Strip instance with a Rectangle describing 
        its shape and an empty points list.
        """
        self.rect = rectangle
        self.points = []


class StripStructure(object):
    def __init__(self, extent, no_strips):
        """Constructor. Inits a StripStructure instance with the correct
        number of Strip instances and makes sure that the domain is 
        correctly divided over the strips.
        """
        self.strips = []
        # Extend this method,
        # so that the right number of strip objects (with the correct extent)
        # are appended to the strips list
        # assuming that the extent is a rectangle instance
        # should have no_strips no of strips as rectangle instances, need to divide the extent into multiple rects
        ll = extent.ll
        ur = extent.ur
        del_x = extent.width()

        strip_leng = del_x/no_strips
        new_ll_x = ll.x
        new_ur_x = ll.x + strip_leng
        for _ in range(no_strips):
            
            
            s = Strip(Rectangle( Point(new_ll_x , ll.y), Point( new_ur_x, ur.y)  )  )
            new_ll_x += strip_leng
            new_ur_x += strip_leng
            #append a strip rect instance to strips list
            self.strips.append(s)
        


    def find_overlapping_strips(self, shape):
        """Returns a list of strip objects for which their rectangle intersects 
        with the shape given.
        
        Returns - list of Strips
        """
        ls=[]
        for i in self.strips:
            if i.rect.intersects(shape):
                ls.append(i)
        return(ls)

    def query(self, shape):
        """Returns a list of points that overlaps the given shape.
        
        For this it first finds the strips that overlap the shape,
        using the find_overlapping_strips method.

        Then, all points of the selected strips are checked for intersection
        with the query shape.
        
        Returns - list of Points
        """ 
        pt_list = []
        overlap_strips = self.find_overlapping_strips(shape) 
        # list of overlapping strip objects 
        # overlap_strips = [strip_item.find_overlapping_strips(shape) for strip_item in self.strips]
        for strip in overlap_strips:
            # check for intersections of points in the strips with shapes
            strp_pnt = strip.points #list of points in strip
            for pnt in strp_pnt:
                if pnt.intersects(shape):
                    pt_list.append(pnt)
        
        return( pt_list )


    def append_point(self, pt):
        """Appends a point object to the list of points of the correct strip
        (i.e. the strip the Point intersects).

        For this it first finds the strips that overlap the point,
        using the find_overlapping_strips method.

        In case multiple strips overlap the point, the point is added
        to the strip with the left most coordinate.
        
        Returns - None
        """
        # strips = [strip_item.find_overlapping_strips(pt) for strip_item in self.strips] 
        # strips = self.strips.find_overlapping_strips(pt)

        #TODO: BUG HERE  PLSS FIXXXXX
        strips = self.find_overlapping_strips(pt)
        for strip in strips:
            if pt.intersects(strip.rect):
                strip.points.append(pt)
                break
        #TODO: strip overlap put in the left one
        return(None)
    def print_strip_statistics(self):
        """Prints:
        * how many strips there are in the structure

        And then, for all the strips in the structure:
        * an id (starting at 1),
        * the number of points in a strip, 
        * the lower left point of a strip and 
        * the upper right point of a strip.
        
        Returns - None
        """
        # format for print output: #1 with 33 points, ll: POINT (0.0 0.0), ur: POINT (2.0 10.0)
        print(f"{len(self.strips)} strips")

        for id, strip in enumerate(self.strips):
            print(f"#{id+1} with {len(strip.points)} points, ll: {strip.rect.ll}, ur: {strip.rect.ur}")
            # print(strip.points)
            # print(f"ID: {id+1}")
            # print(f"No. of points in strips: {len(strip.points)}")
            # print(f"Lower left of strip: {strip.rect.ll}")
            # print(f"Upper right of strip: {strip.rect.ur}")
        return(None)

    def dumps_strips(self):
        """Dumps the strips of this structure to a str, 
        which (if saved in a text file) can be loaded as 
        delimited text layer in QGIS.
        
        Returns - str
        """
        lines = "strip;wkt\n"
        for i, strip in enumerate(self.strips, start = 1):
            t = "{0};{1}\n".format(i, strip.rect)
            lines += t
        return lines

    def dumps_points(self):
        """Dumps the points of this structure to a str, 
        which (if saved in a text file) can be loaded as 
        delimited text layer in QGIS.
        
        Returns - str
        """
        lines = "strip;wkt\n"
        for i, strip in enumerate(self.strips, start = 1):
            for pt in strip.points:
                t = "{0};{1}\n".format(i, pt)
                lines += t
        return lines

