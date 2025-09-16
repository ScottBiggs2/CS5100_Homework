2 Route Planning
In route planning, the objective is to find the best way to get from point A to point B, just like in Google
Maps. In this homework, we will build on top of the classic shortest path problem to allow for more powerful
queries. For example, not only will you be able to explicitly ask for the shortest path from the Northeastern
building to Starbucks, but you can ask for the shortest path from Northeastern back to your apartment,
stopping by the gym, Subway, and the library (in any order) along the way.
We will assume that we have a map of a city (e.g., San Jose) consisting of a set of locations. Each
location has:
• a unique label (e.g., 5674926221).
• a (latitude, longitude) pair specifying where the location is (e.g., 42.44219431, -25.253427).
• a set of tags which describes the type of location (e.g., amenity=food).
2
There are a set of connections between pairs of locations. Each connection has a distance, in meters, and can
be traversed in both directions. If the distance from A to B is 100 meters, then the distance from B to A is
also 100 meters.
There are two city maps that you’ll be working with: a grid map (createGridMap) and a map of San
Jose (createSanJoseMap), which is derived from Open Street Maps. We have also included instructions on
how to create your own maps in README.md.
2.1 Grid City
Consider an infinite city consisting of locations (x, y) where x, y are integers. From each location (x, y), one
can go east, west, north, or south. You start at (0, 0) and want to go to (m, n), where m, n ≥ 0. We can
define the following search problem to capture this:
• sstart = (0, 0)
• Actions(s) = {(1, 0), (−1, 0), (0, 1), (0, −1)}.
• Succ(s, a) = s + a.
• Cost((x, y), a) = 1 + max(x, 0) (it is more expensive as x increases).
• IsEnd(s) = 1[s = (m, n)]
1. What is the minimum cost of reaching location (m, n), with m, n ≥ 0, starting from location (0, 0) in
the above city? Describe one possible path achieving the minimum cost. Is it unique, i.e., are there
multiple paths that achieve the minimum cost?
2. True or False Specify if the following statements are true or false:
• Uniform Cost Search (UCS) will never terminate because the number of states is infinite.
• UCS will return the minimum cost path and explore only locations between (0, 0) and (m, n); that
is, (x, y) such that 0 ≤ x ≤ m and 0 ≤ y ≤ n.
• UCS will return the minimum cost path and explore only locations whose past costs are less than
or equal to the minimum cost from (0, 0) to (m, n).
2.2 Finding Shortest Paths
We first start out with the problem of finding the shortest path from a start location (e.g., the Northeast-
ern Building) to some end location. In Google Maps, you can only specify a specific end location (e.g., Subway).
In this problem, we want to give the user the flexibility of specifying multiple possible end locations
by specifying a set of "tags" (e.g., so you can say that you want to go to any place with food versus a specific
location like Subway).
1. Implement the class ShortestPathProblem so that given a startLocation and endTag, we can find the
minimum cost path corresponding to the shortest path from startLocation to any location that has the
endTag. Specifically, you need to implement,
• startState() which returns an object of type State containing the location of the starting state.
The memory argument can be kept as None for this problem.
• isEnd(state) which returns a boolean indicating whether state has the endTag.
• successorsAndCosts(state) which returns a list of tuples of the form:
(successorLocation: str, successorState: State, cost: float).
3
I would recommend to start by getting familiar with the whole code. Make sure to go over the class
State in util.py and the class CityMap in mapUtil.py as they will be needed in this part.
Recall the separation between search problem (modeling) and search algorithm (inference). You
should focus on modeling, i.e., defining the ShortestPathProblem. The default search algorithm,
UniformCostSearch (UCS), is implemented for you in util.py.
2. Run python mapUtil.py > readableSanJoseMap.txt to write a file of the possible locations on the San
Jose map along with their tags. Each tag is a [key]=[value]. Here are some examples of keys:
• landmark: Hand-defined landmarks (from data/sanjose-landmarks.json)
• amenity: Various amenity types (e.g., "park", "food")
• parking: Assorted parking options (e.g., "underground")
Choose a starting location and end tag, perhaps that’s relevant to your daily life, and implement
getSanJoseShortestPathProblem() to create a search problem. Then, run python grader.py 1b-custom
to generate path.json. Once generated, run python visualization.py to visualize it. It will open in your
browser. Include an image of the path you obtained in your submission.
You can add new landmarks by following the instructions in the README.md to use your own map
and landmarks.