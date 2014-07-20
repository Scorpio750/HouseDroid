class Vector(object):

	"""A vector for the Timbot's graph-map, consisting of degrees and magnitude."""

	def __init__(self, deg, mag):
		self.degrees = deg
		self.magnitude = mag
	
	def __str__(self):
		return 'Degrees: ' + str(self.degrees) + '\nMagnitude: ' + str(self.magnitude)	

	def __eq__(self,other):
		#two vectors are equal if they have the same degree and magnitude
		if other is None:
			return False
		if self.degrees == other.degrees and self.magnitude == other.magnitude:
			return True
		return False

class Edge(object):

	"""An edge for the Timbot's graph-map, containing a vector object and a reference to the vertex they represent."""

	def __init__(self, vect,vert):
		self.vector = vect
		self.vertex = vert

	def __str__(self):
		return 'Vector: \n' + str(self.vector) + '\nVertex Coordinates: (' + str(self.vertex.x) + ',' + str(self.vertex.y) + ',' + str(self.vertex.z) + ')'

	def __eq__(self,other):
		#two edges are equal if they have the same vector and vertex reference
		if other is None:
			return False
		if self.vector == other.vector and self.vertex == other.vertex:
			return True
		return False

class Vertex(object):

	"""A Vertex for the Timbot's graph-map, containing (x,y,z) coordinates, a confidence percentage, a room check and an edge list."""

	def __init__(self, x, y, z, conf):
		self.isRoom = False
		self.x = x
		self.y = y
		self.z = z
		self.confidence = conf
		self.edge_list = []

	def __eq__(self,other):
		#two verticies are equal if they are at the same x,y,z coordinate, I assume no further checking is required
		if other is None:
			return False
		if self.x == other.x and self.y == other.y and self.z == other.z:
			return True
		return False

	def set_as_room(self):
		#set the node as a room, rather than a decision
		self.isRoom = True

	def unset_as_room(self):
		#not sure if this has any purpose, but here it is
		self.isRoom = False

	def add_edge(self, edge):
		#add this edge to the list, and add this vertex to the edge's vertex's list
		self.edge_list.append(edge)
		to_add = Edge(edge.vector, self)
		edge.vertex.edge_list.append(to_add)

	def remove_edge(self, edge):
		#remove this edge from the list, and remove this vertex from the edge's vertex's list
		reciprocate = edge.vertex
		self.edge_list.remove(edge)
		other_edge = Edge(edge.vector, self)
		reciprocate.edge_list.remove(other_edge)	

	def __str__(self):
		coord = 'Coordinates: (' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) +')'
		conf = 'Confidence: ' + str(self.confidence)
		rm = 'Room? ' + str(self.isRoom)
		el = ''
		for e in self.edge_list:
			el += '\nEdge{\n'
			el += str(e) + '\n}'
		return coord + '\n' + conf + '\n' + rm + el


class Graph(object):
	
	"""The graph-map for the Timbot."""

	def __init__(self):
		self.vertex_list = []

	def add_vertex(self, vertex):
		#add a new vertex to the list
		self.vertex_list.append(vertex)

	def remove_vertex(self, vertex):
		#remove this vertex from the list
		self.vertex_list.remove(vertex)

	def form_edge(self,vertex_one,vertex_two,vector):
		#create an edge between these two verticies
		#essentially an alternative to the vertex's built-in add_edge function because I forgot I wrote this when I wrote them
		vertex_one.add_edge(Edge(vector,vertex_two))
		vertex_two.add_edge(Edge(vector,vertex_one))

print Vector.__doc__
print Edge.__doc__
print Vertex.__doc__
print Graph.__doc__
