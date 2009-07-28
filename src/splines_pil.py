#!/usr/bin/env python


from PIL import Image, ImageDraw

#double newX = (1-t)^3*a.x + (1-t)^2*t*b.x + (1-t)*t^2*c.x + t^3 + d.x;
#double newY = (1-t)^3*a.y + (1-t)^2*t*b.y + (1-t)*t^2*c.y + t^3 + d.y;


def cubic_spline_F(t, (A, B, C, D)):
	return A*t**3 + B*t**2 + C*t + D


def spline_params_from_points(c0, c1, c2, c3):
	return (c3 - 3*c2 + 3*c1 - c0,
			     3*c2 - 6*c1 + 3*c0,
			 			3*c1 - 3*c0,
							   c0)



def bezier_f(t, c1, c2, c3, c4):
   return ( (1-t)**3           *  c1   + 
			(1-t)**2  *  t     *  c2   + 
			(1-t)     *  t**2  *  c3   + 
			             t**3  *  c4)
			
def bezier_F(t, a, b, c, d):
	x_t = bezier_f(t, a[0], b[0], c[0], d[0])
	y_t = bezier_f(t, a[1], b[1], c[1], d[1])
	return (x_t, y_t)



def draw_grid(canvas, size):
	w, h = size
	x0, y0 = w/2, h/2
	# axes
	canvas.line((x0, 0, x0, h), fill=(0, 255, 0))
	canvas.line((0, y0, w, y0), fill=(255, 0, 0))
	
	#grid
	def draw_horizontal_lines(canvas, center, size, offset, colour):
		(x0, y0), (w, h) = center, size
		canvas.line((x0+offset, 0, x0+offset, h), fill=colour) 
		canvas.line((x0-offset, 0, x0-offset, h), fill=colour)
		
	def draw_vertical_lines(canvas, center, size, offset, colour):
		(x0, y0), (w, h) = center, size
		canvas.line((0, y0+offset, w, y0+offset), fill=colour)
		canvas.line((0, y0-offset, w, y0-offset), fill=colour)
	
	colour_choice = ((200, 200, 200), (100, 100, 100))
	
	for i in range(10, w/2, 10):
		draw_horizontal_lines(canvas, (x0, y0), (w, h), i, colour_choice[i%100==0])
		
	for i in range(10, h/2, 10):
		draw_vertical_lines(canvas, (x0, y0), (w, h), i, colour_choice[i%100==0]) 
		
		
def draw_points(canvas, size, points, colour=(255, 0, 120)):
	xc, yc = size[0]/2, size[1]/2 
	transformed_points = [(xc+100*x, yc-100*y) for (x,y) in points]
	canvas.line(transformed_points, fill=colour)
		
		
def draw_vector(canvas, size, point, vector):
	xc, yc = size[0]/2, size[1]/2
	p0 = point
	p1 = (point[0]+vector[0], point[1]+vector[1]) 
	
	transformed_points = [(xc+100*x, yc-100*y) for (x,y) in (p0, p1)]
	canvas.line(transformed_points, fill=(0, 0, 255))


def draw_circle(canvas, size, point, color=(255,0,0)):
	xc, yc = size[0]/2, size[1]/2

	canvas.ellipse([(xc+100*point[0]+off, yc-100*point[1]+off) for off in (-5,+5)],
		       outline = color)


def draw_point(canvas, size, point):
	xc, yc = size[0]/2, size[1]/2
	#canvas.ellipse()

def add_vectors(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])


def sub_vectors(v1, v2):
	return (v1[0] - v2[0], v1[1] - v2[1])



class BezierSplineDrawer(object):
	"""docstring for SplineDrawer"""
	def __init__(self, (p1, v1), (p2, v2)):
		super(BezierSplineDrawer, self).__init__()
		self.a = p1
		self.d = p2
		self.va = v1
		self.vd = v2
		
		a, d = self.a, self.d
		b = add_vectors(self.a, self.va)
		c = add_vectors(self.d, self.vd)
		self.spline = [bezier_F(float(t)/100, a, b, c, d) for t in range(100)]
		

	def dump_in_image(self, filename):
		spline = self.spline
		img = Image.new("RGB", (800, 600), (255, 255, 255))
	
		draw = ImageDraw.Draw(img)
		draw_grid(draw, (800, 600))
	
		draw_points(draw, img.size, spline)
		draw_vector(draw, img.size, self.a, self.va)
		draw_vector(draw, img.size, self.d, self.vd)
	
		img.save(filename)
		img.show()
	
	
class CubicSplineDrawer(object):
	"""docstring for CubicSplineDrawer"""
	def __init__(self):
		super(CubicSplineDrawer, self).__init__()	
		self.splines = []
		self.points = []
	
	def add_points(self, p1, p2, p3, p4):
		self.points += (p1, p2, p3, p4)
		
		x_params = spline_params_from_points(*[x for (x, y) in (p1, p2, p3, p4)])
		y_params = spline_params_from_points(*[y for (x, y) in (p1, p2, p3, p4)])
		
		self.splines += [(cubic_spline_F(float(t)/100, x_params),
						  cubic_spline_F(float(t)/100, y_params)) for t in range(100) ]
	
	
	
	def dump_in_image(self, filename):
		spline = self.splines
		img = Image.new("RGB", (800, 600), (255, 255, 255))
	
		draw = ImageDraw.Draw(img)
		draw_grid(draw, (800, 600))
	
		draw_points(draw, img.size, spline)
		print self.points
		draw_points(draw, img.size, self.points, (0, 0, 200))


		colors = [(255,0,0), (0,255,0), (0, 0, 255), (255,0,255)]
		
		for (i, p) in enumerate(self.points):
			draw_circle(draw, img.size, p, colors[i%4])
	
		img.save(filename)
		img.show()

	
def mul_vector(v, s):
	return (s*v[0], s*v[1])

def predict_points(p_old, v_old, p, v_p, a_p, t):
	"""
	"""
	p1 = add_vectors(p_old, v_old)
	p2 = add_vectors(add_vectors(p, v_p), (.5*a_p[0]*t**2, .5*a_p[1]*t**2))
	p3 = sub_vectors(p2, add_vectors(v_p, mul_vector(a_p, t)))
	
	return (p_old, p1, p2, p3)

def derive(v1, v2, dt):
	return (float(v1[0]-v2[0]) / dt,
		float(v1[1]-v2[1]) / dt)


def print_points(points):
	for (i,p) in enumerate(points):
		print "p[%d] : (%.1f, %.1f)" % (i, p[0], p[1])

	
def main():
	"""docstring for main"""
	#p1, p2 = (0, 0), (3, 0)
	#v1, v2 = (1, 1), (-3, 3)
	# 
	#s = BezierSplineDrawer((p1, v1), (p2, v2))
	#s.dump_in_image("blah.png")
	
	#(0, 0), (1, 1.5), (2, 1), (3, 0)

	s2 = CubicSplineDrawer()


	# batch 1
	p_old, v_old = (0, 0), (0.5, 0.5)
	p, v_p, a_p = (2, 0), (0.3, 0.3), (0, 0)
	points = predict_points(p_old, v_old, p, v_p, a_p, 0.5)
	print_points(points)

	s2.add_points(*points)
	

	#batch 2
	p_old, v_old = points[3], derive(points[3], points[2], 0.1)
       	#sub_vectors(points[3], points[2])
	p, v_p, a_p = (-1, -1), v_p, (0, 0)
	points = predict_points(p_old, v_old, p, v_p, a_p, 0.5)

	print_points(points)
	
	s2.add_points(*points)



	
	s2.dump_in_image("blah2.png")


if __name__ == '__main__':
	main()
