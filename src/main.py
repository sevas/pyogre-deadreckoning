#!/usr/bin/env python2.5

import math, random, operator

import ogre.renderer.OGRE as ogre
import SampleFramework as sf
import ogre.io.OIS as OIS


random.seed()


def add_vectors(v1, v2):
    """
    
    Paramters:
    - `v1`: 
    - `v2`: 
    """
    return op_vectors(operator.add, v1, v2)

def sub_vectors(v1, v2):
    return op_vectors(operator.sub, v1, v2)


def op_vectors(op, v1, v2):
    return map(op, v1, v2)


def op_vector(op, v):
    return map(op, v)


def mul_vector(v, s):
    return (s*v[0], s*v[1], s*v[2])
    


def derive(v1, v2, dt):
	return (float(v1[0]-v2[0]) / dt,
		float(v1[1]-v2[1]) / dt,
                float(v1[2]-v2[2]) / dt
                )



class PathListener(sf.FrameListener):
    "docstring for PathListener"
    def __init__(self, renderWindow, camera, dynamic_line):
        sf.FrameListener.__init__(self, renderWindow, camera)
        self.renderWindow, self.camera = renderWindow, camera
        self.dynamic_line = dynamic_line
        self.timeLapse = 0.0
        

        self.pdu = {"pos"  : self.dynamic_line["vertices"][-1],
                    "speed": (1, 1, 1),
                    "accel"  : (1, 1, 1)}

        self.points = [None] * 4
        self.p_old = (0,0,0)
        self.v_old = (0.5, 0, 0.5)

        self.p, self.v_p, self.a_p = None, None, None

        self.current_pos = (0, 0, 0)
        self.current_t = 0.0
        self.last_t = 0.0

        self.vars = {"x":None, "y":None, "z":None}
        
        

    def frameStarted(self, frameEvent):
        if( sf.FrameListener.frameStarted(self, frameEvent) == False ):
            return False 
        self.timeLapse += frameEvent.timeSinceLastFrame 


        if self.timeLapse > 1:
            print "*** Begin line update"
            self.timeLapse = 0.0
            manual_object = self.dynamic_line["manual_object"]

            last_index = self.dynamic_line["current_index"] - 1
            last_point = self.dynamic_line["vertices"][last_index]


            new_point = add_vectors(last_point,
                                    (3*random.uniform(-1, 1),
                                     #random.uniform(-1, 1),
                                     0,
                                     3*random.uniform(-1, 1)))



            self.dynamic_line["vertices"].append(new_point)

            manual_object.estimateVertexCount(len(self.dynamic_line["vertices"]) + 1 + 35)

            self._add_circle(new_point, manual_object)
            self._add_line_segment(last_point, new_point, manual_object)
        
            self.dynamic_line["current_index"] += 1





            self.p = new_point#add_vectors(self.p_old, new_point)  #(random.randint(-2, 2), random.randint(-2, 2)))

            self.v_p = add_vectors(self.v_old, (random.uniform(-1,1)/100, 0, random.uniform(-1,1)/100))
            self.a_p = (0,0,0)

            points = self._predict_points(self.p_old, self.v_old, self.p, self.v_p, self.a_p, 1.0)

            self._update_spline_parameters(points)
            #plot(*make_spline(points, 100))
            self.p_old, self.v_old = points[3], (-self.v_p[0], 0, -self.v_p[1]) #derive(points[3], points[2], 1.0)



            
            self.current_t = 0.0

            

        else:
            #update spline
            last_pos = self.current_pos
            self.current_pos = (self._eval_func("x", self.current_t),
                                0,
                                self._eval_func("z", self.current_t))

        

            spline_object = self.dynamic_line["spline_object"]

            spline_object.begin("Objects/Spline", ogre.RenderOperation.OT_LINE_STRIP)
            spline_object.position(last_pos)
            spline_object.colour(0, 0, 0)
            spline_object.position(self.current_pos)
            spline_object.colour(0, 0, 0)
            
            spline_object.end()

            self.last_t = self.current_t
            self.current_t += frameEvent.timeSinceLastFrame
            #print self.current_pos

        return True


    def _eval_mrua(self, last_pos, v, a):
        t = self.current_t - self.last_t
        return (last_pos[0] + v[0] * t + 0.5 * a[0] * t**2,
                0,
                last_pos[2] + v[2] * t + 0.5 * a[2] * t**2)
                                            

    def _get_speed_vector(self, last_point, new_point):
        return tuple(map(operator.sub, new_point, last_point))


    def _get_accel_vector(self, last_speed, new_speed):
        return tuple(map(operator.sub, new_speed, last_speed))



    def _update_spline_parameters(self, points):
        """
        updates x(t), y(t) and z(t) equations according to the new projected point
        """
        self.vars["x"] = self._update_spline_variables([p[0] for p in points])
        self.vars["y"] = self._update_spline_variables([p[1] for p in points])
        self.vars["z"] = self._update_spline_variables([p[2] for p in points])


    def _update_spline_variables(self, coords):
        """
        returns A, B, C, D splines params, for a certain dimension
        """
        return (coords[3] - 3*coords[2] + 3*coords[1] - coords[0],
                3*coords[2] - 6*coords[1] + 3*coords[0],
                3*coords[1] - 3*coords[0],
                coords[0])
                

    def _project_point(self):
        """
        """
        p0 = self.pdu["pos"]
        v, a = self.pdu["speed"], self.pdu["acc"]
        

    def _eval_func(self, var, t):
        """
        evaluates VAR(t), VAR being x, y or z
        """
        if self.vars[var]:
            A, B, C, D = self.vars[var];
            return A*t**3 + B*t**2 + C*t + D
        else:
            return 0
    

    def _predict_points(self, p_old, v_old, p, v_p, a_p, t):
	"""
	"""
        print p_old, v_old, p, v_p, a_p
	p1 = add_vectors(p_old, v_old)
	p2 = add_vectors(add_vectors(p, mul_vector(v_p, t)), (.5*a_p[0]*t**2, .5*a_p[1]*t**2, 5*a_p[2]*t**2))
	p3 = sub_vectors(p2, add_vectors(v_p, mul_vector(a_p, t)))
	
	return [p_old, p1, p2, p3]



    def _add_circle(self, center, manual_object, radius=0.05):
        point_index = 0
        accuracy = 35
        theta = 0.0
        
        manual_object.begin("Objects/DynamicLinePoint", ogre.RenderOperation.OT_LINE_STRIP)

        while theta <= 2*math.pi:
            manual_object.position(center[0] + radius * math.cos(theta),
                                   center[1] + radius * math.sin(theta),
                                   center[2] + 0)
            manual_object.index(point_index)
            point_index += 1
         
            theta += math.pi / accuracy

        manual_object.index(0)
        manual_object.end()

    def _add_line_segment(self, p0, p1, manual_object):
        """
        
        Parameters:
        - `p0`: 
        - `p1`: 
        - `manual_object`: 
        """
        manual_object.begin("Objects/DynamicLine", ogre.RenderOperation.OT_LINE_STRIP)
        manual_object.position(*p0)
        manual_object.colour((0, 0, 0))
        manual_object.position(*p1)
        manual_object.colour((0, 0, 0)) 
        manual_object.end()

    

    

class Application(sf.Application):
    "docstring for Application"
    def __init__(self):
        sf.Application.__init__(self)

        self.vertices = [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0),
                         (1, 1, 0), (0, 1, 0), (0, 1, 1), (1, 1, 1),
                         (1, 2, 1)]

        self.vertices = [(0,0,0)]

        self.current_vert_index = len(self.vertices)
        self.dynamic_line = {"vertices" : self.vertices,
                             "current_index" : self.current_vert_index,
                             "manual_object" : None,
                             "spline_object" : None}


    #def __del__(self):
    #    sf.Application.__del__(self)


        
    def _createScene(self):
        sceneManager = self.sceneManager
        camera = self.camera
        #sceneManager.ambientLight = [0.9, 0.9, 0.9]
        sceneManager.setNormaliseNormalsOnScale(True)
        
        camera.Position = (100, 100, 100)
        camera.lookAt((0, 0, 0))
        
        ## Create the SkyBox
        #sceneManager.setSkyBox(True, "Examples/CloudyNoonSkyBox")
        self.renderWindow.getViewport(0).backgroundColour = (0.7, 0.7, 0.7)

        ## create simple cube
        #entity = sceneManager.createEntity("sphere" , "sphere.mesh")
        #entity.setMaterialName("Objects/Ball");
        #node = sceneManager.getRootSceneNode().createChildSceneNode()
        #node.attachObject(entity)

        #w = entity.boundingBox.size.x;
	#ws = 50.0 / w;
        #node.setScale(ws,ws,ws)
        
        #node.setPosition(ogre.Vector3(20, 0, 0))

        self._createLight()
        self._createAxes(300)
        self._createLine()


    def _createLight(self):
        """
        """
        self.light = self.sceneManager.createLight("Main Light")
        self.light.type = ogre.Light.LightTypes.LT_POINT
        self.light.specularColour = (1.0, 1.0, 1.0)
        self.light.diffuseColour = (1.0, 1.0, 1.0)

        self.light_node = self.sceneManager.getRootSceneNode().createChildSceneNode("light node")
        self.light_node.attachObject(self.light)
        self.light_node.Position = (0, 200, 0)
        


    def _createAxes(self, units):
        """
        
        Parameters:
        - `units`: 
        """
        self.grid_node = self.sceneManager.getRootSceneNode().createChildSceneNode("WorldGrid Node")

        x_axis = self._createAxis(units, 0, "X Axis", "WorldGrid/XAxis")
        y_axis = self._createAxis(units, 1, "Y Axis", "WorldGrid/YAxis")
        z_axis = self._createAxis(units, 2, "Z Axis", "WorldGrid/ZAxis")

        self.grid_node.attachObject(x_axis)
        self.grid_node.attachObject(y_axis)
        self.grid_node.attachObject(z_axis)

        grid = self._createGrid(units, "Grid Lines", "WorldGrid/Lines")
        self.grid_node.attachObject(grid)

    

    def _createAxis(self, units, axis_id, object_name, material_name):
        """
        """
        axis_drawer = self.sceneManager.createManualObject(object_name)

        axis_drawer.begin(material_name, ogre.RenderOperation.OT_LINE_LIST)

        pos, colour = [0,0,0], [0, 0, 0]
        pos[axis_id] = -units
        colour[axis_id] = 0.1

        axis_drawer.position(pos)
        #axis_drawer.normal(0.0, 1.0, 0.0)
        axis_drawer.colour(*colour)

        pos[axis_id] = units
        colour[axis_id] = 1.0

        axis_drawer.position(*pos)
        #axis_drawer.normal(0.0, 1.0, 0.0)
        axis_drawer.colour(*colour)

        axis_drawer.end()
    
        return axis_drawer

    

    def _createGrid(self, units, object_name, material_name):
        """
        """
        step = 10
        grid = self.sceneManager.createManualObject(object_name)

        grid.begin(material_name, ogre.RenderOperation.OT_LINE_LIST)

        for i in range(step, units+step, step):
            offset = i
            colour = (int(abs(i))%100 == 0) and 0.3 or 0.65

            #  -----
            #  -----
            #  -----
            grid.position(-units, 0.0, offset)
            grid.colour(colour, colour, colour)

            grid.position( units, 0.0, offset)
            grid.colour(colour, colour, colour)


            grid.position(-units, 0.0, -offset)
            grid.colour(colour, colour, colour)

            grid.position( units, 0.0, -offset)
            grid.colour(colour, colour, colour)


            #  | | |
            #  | | |
            #  | | |
            grid.position(offset, 0.0, -units)
            grid.colour(colour, colour, colour)

            grid.position(offset, 0.0, units)
            grid.colour(colour, colour, colour)

            grid.position(-offset, 0.0, -units)
            grid.colour(colour, colour, colour)

            grid.position(-offset, 0.0, units)
            grid.colour(colour, colour, colour)


        grid.end()

        return grid

    def _createLine(self):
        ""
        dynamic_line_object = self.sceneManager.createManualObject("Dynamic Line")

        dynamic_line_object.begin("Objects/DynamicLine", ogre.RenderOperation.OT_LINE_STRIP)

        for vert in self.vertices:
            dynamic_line_object.position(*vert)
            dynamic_line_object.colour((0, 0, 0))
            
        
        dynamic_line_object.end()

        dynamic_line_object.dynamic = True

        self.line_node =  self.sceneManager.getRootSceneNode().createChildSceneNode("Dynamic Line Node")
        self.line_node.attachObject(dynamic_line_object)
        #self.line_node.translate(0, 10, 0)
        self.line_node.scale(10, 10, 10)

        self.dynamic_line["manual_object"] = dynamic_line_object
        
        self.dynamic_line["spline_object"] =  self.sceneManager.createManualObject("Dynamic Spline")
        self.line_node.attachObject(self.dynamic_line["spline_object"])
        

    def _createFrameListener(self):
        self.frameListener = PathListener(self.renderWindow, self.camera, self.dynamic_line)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay( True )


if __name__ == '__main__':
    try:
        TA = Application()
        TA.go()
    except ogre.OgreException, e:
        print '***', e

