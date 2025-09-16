from typing import List, Tuple

from mapUtil import (
    CityMap,
    computeDistance,
    createSanJoseMap,
    locationFromTag,
    makeTag, getTotalCost,
)
from util import Heuristic, SearchProblem, State, UniformCostSearch


# *IMPORTANT* :: A key part of this assignment is figuring out how to model states
# effectively. We've defined a class `State` to help you think through this, with a
# field called `memory`.
#
# As you implement the different types of search problems below, think about what
# `memory` should contain to enable efficient search!
#   > Please read the docstring for `State` in `util.py` for more details and code.

# Please also read the docstrings for the relevant classes and functions defined in `mapUtil.py`

########################################################################################
# Problem 1a: Modeling the Shortest Path Problem.


class ShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path
    from `startLocation` to any location with the specified `endTag`.
    """

    def __init__(self, startLocation: str, endTag: str, cityMap: CityMap):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

    def startState(self) -> State:
        # The state consists of the starting location and no memory needed for this problem
        return State(location=self.startLocation, memory=None)

    def isEnd(self, state: State) -> bool:
        # Return True if the current location has the endTag
        tags = self.cityMap.tags.get(state.location, [])
        return self.endTag in tags

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        """
        Return a list of (successorLocation, successorState, cost) for all neighbors.
        """
        result = []
        current_location = state.location
        for neighbor, cost in self.cityMap.distances.get(current_location, {}).items():
            successor_state = State(location=neighbor, memory=None)
            result.append((neighbor, successor_state, cost))
        return result


########################################################################################
# Problem 1b: Custom -- Plan a Route through San Jose


def getSanJoseShortestPathProblem() -> ShortestPathProblem:
    """
    Create your own search problem using the map of San Jose, specifying your own
    `startLocation`/`endTag`. If you prefer, you may create a new map using via
    `createCustomMap()`.

    Run `python mapUtil.py > readableSanJoseMap.txt` to dump a file with a list of
    locations and associated tags; you might find it useful to search for the following
    tag keys (amongst others):
        - `landmark=` - Hand-defined landmarks (from `data/sanjose-landmarks.json`)
        - `amenity=`  - Various amenity types (e.g., "parking_entrance", "food")
        - `parking=`  - Assorted parking options (e.g., "underground")
    """
    cityMap = createSanJoseMap()

    # Or, if you would rather use a custom map, you can uncomment the following!
    # cityMap = createCustomMap("data/custom.pbf", "data/custom-landmarks".json")

    # BEGIN_YOUR_CODE
    # Example: choose a start location and an end tag. You can change these as needed.
    # To find available locations and tags, run: python mapUtil.py > readableSanJoseMap.txt
    startLocation = "7830771487"  # olla cocina
    endTag = "landmark=city_hall"  # city hall
    return ShortestPathProblem(startLocation, endTag, cityMap)
    # END_YOUR_CODE


########################################################################################
# Problem 2a: Modeling the Waypoints Shortest Path Problem.


class WaypointsShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path from
    `startLocation` to any location with the specified `endTag` such that the path also
    traverses locations that cover the set of tags in `waypointTags`.

    Hint: naively, your `memory` representation could be a list of all locations visited.
    However, that would be too large of a state space to search over! Think 
    carefully about what `memory` should represent.
    """
    def __init__(
        self, startLocation: str, waypointTags: List[str], endTag: str, cityMap: CityMap
    ):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

        # We want waypointTags to be consistent/canonical (sorted) and hashable (tuple)
        self.waypointTags = tuple(sorted(waypointTags))

    def startState(self) -> State:
        # Remove any waypoint tags already present at the start location
        start_tags = set(self.cityMap.tags.get(self.startLocation, []))
        unvisited = tuple(sorted(set(self.waypointTags) - (start_tags & set(self.waypointTags))))
        return State(location=self.startLocation, memory=unvisited)

    def isEnd(self, state: State) -> bool:
        # End if all waypoints have been visited (memory is empty) and location has endTag
        tags = self.cityMap.tags.get(state.location, [])
        unvisited = state.memory if state.memory is not None else ()
        return (len(unvisited) == 0) and (self.endTag in tags)

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        result = []
        current_location = state.location
        unvisited = set(state.memory) if state.memory is not None else set()
        for neighbor, cost in self.cityMap.distances.get(current_location, {}).items():
            neighbor_tags = set(self.cityMap.tags.get(neighbor, []))
            # Remove any waypoint tags that are present at the neighbor
            new_unvisited = tuple(sorted(unvisited - (neighbor_tags & set(self.waypointTags))))
            successor_state = State(location=neighbor, memory=new_unvisited)
            result.append((neighbor, successor_state, cost))
        return result


########################################################################################
# Problem 2b: Custom -- Plan a Route with Unordered Waypoints through San Jose


def getSanJoseWaypointsShortestPathProblem() -> WaypointsShortestPathProblem:
    """
    Create your own search problem using the map of San Jose, specifying your own
    `startLocation`/`waypointTags`/`endTag`.

    Similar to Problem 1b, use `readableSanJoseMap.txt` to identify potential
    locations and tags.
    """
    cityMap = createSanJoseMap()
    # Example: choose a start location, waypoint tags, and an end tag. You can change these as needed.
    # To find available locations and tags, run: python mapUtil.py > readableSanJoseMap.txt
    startLocation = "7830771487"  # olla cocina
    waypointTags = ["landmark=san_pedro_market", "landmark=philz"]  # must visit san pedro market and philz
    endTag = "landmark=city_hall"  # end at city hall
    return WaypointsShortestPathProblem(startLocation, waypointTags, endTag, cityMap)

########################################################################################
# Problem 4a: A* to UCS reduction

# Turn an existing SearchProblem (`problem`) you are trying to solve with a
# Heuristic (`heuristic`) into a new SearchProblem (`newSearchProblem`), such
# that running uniform cost search on `newSearchProblem` is equivalent to
# running A* on `problem` subject to `heuristic`.
#
# This process of translating a model of a problem + extra constraints into a
# new instance of the same problem is called a reduction; it's a powerful tool
# for writing down "new" models in a language we're already familiar with.
# See util.py for the class definitions and methods of Heuristic and SearchProblem.


def aStarReduction(problem: SearchProblem, heuristic: Heuristic) -> SearchProblem:
    class NewSearchProblem(SearchProblem):
        def startState(self) -> State:
            # Start state is the same as the original problem
            return problem.startState()

        def isEnd(self, state: State) -> bool:
            # End state is the same as the original problem
            return problem.isEnd(state)

        def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
            # For each successor, add the heuristic difference to the cost
            result = []
            for action, succ, cost in problem.successorsAndCosts(state):
                # A* cost: g(n) + h(n') - h(n)
                h_curr = heuristic.evaluate(state)
                h_succ = heuristic.evaluate(succ)
                new_cost = cost + h_succ - h_curr
                result.append((action, succ, new_cost))
            return result

    return NewSearchProblem()


########################################################################################
# Problem 4b: "straight-line" heuristic for A*


class StraightLineHeuristic(Heuristic):
    """
    Estimate the cost between locations as the straight-line distance.
        > Hint: you might consider using `computeDistance` defined in `mapUtil.py`
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        self.endTag = endTag
        self.cityMap = cityMap
        # Precompute all geolocations for locations with the endTag
        self.goal_geos = [cityMap.geoLocations[loc]
                          for loc, tags in cityMap.tags.items()
                          if endTag in tags and loc in cityMap.geoLocations]

    def evaluate(self, state: State) -> float:
        # If no goal geos, return 0
        if not self.goal_geos:
            return 0.0
        # If current location is not in geoLocations, return 0
        if state.location not in self.cityMap.geoLocations:
            return 0.0
        curr_geo = self.cityMap.geoLocations[state.location]
        # Return the minimum straight-line distance to any goal
        return min(computeDistance(curr_geo, goal_geo) for goal_geo in self.goal_geos)