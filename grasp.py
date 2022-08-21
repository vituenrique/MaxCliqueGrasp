import random

def createMatrixGraph(vertices, edges):
	graph = [[0 for x in range(len(vertices))] for y in range(len(vertices))] 
	for i in range(len(edges)):  
		graph[edges[i][0] - 1][edges[i][1] - 1] = 1 
		graph[edges[i][1] - 1][edges[i][0] - 1] = 1
	return graph

def getGraphComplement(graph):
	for i in range(len(graph)):
		for j in range(len(graph)):
			if i == j:
				continue
			if graph[i][j] == 1:
				graph[i][j] = 0
			elif graph[i][j] == 0:
				graph[i][j] = 1
	return graph

def getComplementEdges(graph):
	edges = []
	for i in range(len(graph)):
		for j in range(len(graph)):
			if graph[i][j] == 1:
				isEdgeInArray = False
				for x in range(len(edges)):
					if edges[x][0] == j + 1 and edges[x][1] == i + 1:
						isEdgeInArray = True
						break
				if not isEdgeInArray:		
					edges.append([i + 1, j + 1])
	return edges

def computeVerticesDegree(vertices, edges):
	degrees = []
	for vertice in vertices:
		sumDegrees = 0
		for edge in edges:
			sumDegrees += edge.count(vertice)
		degrees.append(sumDegrees)
	return degrees

def getMaxDegree(degrees, vertices):
	maxDegreeIndex = 0
	maxDegree = 0
	for i in range(len(degrees)):
		if degrees[i] > maxDegree:
			maxDegree = degrees[i]
			maxDegreeIndex = i
	return vertices[maxDegreeIndex] 


def candidatesVertices(vertices, degrees, threshold):
	candidates = []
	for i in range(len(vertices)):
		if(degrees[i] <= threshold):
			candidates.append(vertices[i])
	return candidates

def setNewVertices(vertices, edges, newVertice):
	remove = []
	remove.append(newVertice)
	for edge in edges:
		if(edge[0] == newVertice):
			remove.append(edge[1])
		if(edge[1] == newVertice):
			remove.append(edge[0])
	for r in remove:
		vertice = r  
		vertices.remove(vertice)
		removedEdges = []
		for edge in edges:
			if(edge[0] == vertice or edge[1] == vertice):
				removedEdges.append(edge)
		for removedEdge in removedEdges:
			edges.remove(removedEdge)  

def getNeighbors(vertice, edges):
	neighbors = []
	for edge in edges:
		if(edge[0] == vertice):
			neighbors.append(edge[1])
		if(edge[1] == vertice):
			neighbors.append(edge[0])
	return neighbors

def getNonAdjacentNeighbors(allNeighbors, solution, edges, w):
	neighbors = []
	for an in allNeighbors: 
		areNeighborsAdjacents = False
		for s in solution:
			if(s != w):
				for edge in edges:
					if(edge[0] == an and edge[1] == s):
						areNeighborsAdjacents = True
						break
					if(edge[1] == an and edge[0] == s):
						areNeighborsAdjacents = True
						break
					if(len(neighbors) == 1):
						if(edge[0] == an and edge[1] == neighbors[0]):
							areNeighborsAdjacents = True
							break
						if(edge[1] == an and edge[0] == neighbors[0]):
							areNeighborsAdjacents = True
							break
			if(areNeighborsAdjacents):
				break
		if (not areNeighborsAdjacents):
			neighbors.append(an)
		if(len(neighbors) == 2):
			neighbors.append(w)
			break
	return neighbors  

#(u, v, w) where u and v are nonadjacent to all vertices except w
def getAdjacentsW(solution, edges):
	for s in solution:
		neighbors = getNeighbors(s, edges)

		uvw = getNonAdjacentNeighbors(neighbors, solution, edges, s) 
		
		if(len(uvw) >= 3):
			break
	return uvw

def greedyRandomizedConstruction(seed, vertices, edges):
	solution = []

	tmpVertices = vertices[:]
	tmpEdges = edges[:]

	for i in range(len(tmpVertices)):
		degrees = computeVerticesDegree(tmpVertices, tmpEdges)
		lowerDegree = min(degrees)
		higherDegree = max(degrees)
		maxDegree = lowerDegree + seed * (higherDegree - lowerDegree)
		
		candidates = candidatesVertices(tmpVertices, degrees, maxDegree)
		randomCandidate = random.choice(candidates)
		solution.append(randomCandidate)
		
		setNewVertices(tmpVertices, tmpEdges, randomCandidate)
		
		if len(tmpVertices) <= 0:
			break
	return solution

def localSearch(solution, edges):
	
	h = getAdjacentsW(solution, edges)

	indexs = random.sample(range(0, 3), 3)
	while(len(h) == 3):
		solution.remove(h[2])
		solution.append(h[1])
		solution.append(h[0])
		h = getAdjacentsW(solution, edges)
	return solution

def grasp(maxIteration, vertices, edges):
	bestSolution = []
			
	for i in range(maxIteration):

		seed = random.uniform(0, 1)

		greedySolution = greedyRandomizedConstruction(seed, vertices, edges)
		
		localSolution = localSearch(greedySolution, edges)
		
		if(len(localSolution) > len(bestSolution)):
			bestSolution = localSolution
	return bestSolution