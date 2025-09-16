# Gemini Notes

## Project Overview

- **Objective:** Implement and solve two route-planning problems.
- **Files to Modify:** `submission.py`
- **Files to Create:** `report.pdf`
- **Key Classes:** `ShortestPathProblem`, `MultipleVisitProblem` in `submission.py`.
- **Helper classes:** `State` in `util.py`, `CityMap` in `mapUtil.py`.

## `ShortestPathProblem`

- **Goal:** Find the shortest path from a start location to any location with a given `endTag`.
- **`startState()`:** Return a `State` object with the starting location.
- **`isEnd(state)`:** Check if the state's location has the `endTag`.
- **`successorsAndCosts(state)`:** Return successor states and costs from the current state.

## `MultipleVisitProblem`

- **Goal:** Find the shortest path starting at `startLocation`, visiting all `otherLocations`, and returning to `startLocation`.
- **`startState()`:** Return a `State` object with the starting location and the set of `otherLocations` to visit in `memory`.
- **`isEnd(state)`:** Check if all `otherLocations` have been visited and the agent is back at the `startLocation`.
- **`successorsAndCosts(state)`:** Return successor states and costs, updating the `memory` field with the remaining locations to visit.

## Written Questions

- Analyze the Grid City problem.
- Answer questions about the minimum cost path and the behavior of UCS.

## Plan

1.  [ ] Read `util.py` and `mapUtil.py`.
2.  [ ] Implement `ShortestPathProblem` in `submission.py`.
3.  [ ] Implement `getSanJoseShortestPathProblem()` and test.
4.  [ ] Implement `MultipleVisitProblem` in `submission.py`.
5.  [ ] Implement `getSanJoseMultipleVisitProblem()` and test.
6.  [ ] Answer written questions.
7.  [ ] Create `report.pdf`.
8.  [ ] Create submission zip file.
