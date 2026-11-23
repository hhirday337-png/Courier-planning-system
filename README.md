# Courier Planning System

**Student:** Hirday  
**Roll No.:** 2501060202  
**Language:** Python 3

## Features
- Merge Sort: prioritizes parcels by priority (descending), then deadline (ascending).
- 0/1 Knapsack using Dynamic Programming: chooses parcels within vehicle capacity.
- Dijkstra's algorithm: calculates shortest paths in a weighted road graph.
- Nearest Neighbour: creates an approximate route through selected delivery points.

## Files
- `main.py` — complete implementation.
- `parcels.csv` — sample parcel dataset.
- `Courier_Planning_Report.pdf` — project report.

## Run
Install Python 3, open a terminal in this folder, and run:

```bash
python main.py
```

Change vehicle capacity:

```bash
python main.py --capacity 30
```

Use another CSV file:

```bash
python main.py --data your_parcels.csv --capacity 25
```

## CSV format
Columns: `parcel_id,destination,weight,value,priority,deadline`

Destinations in the sample dataset correspond to nodes A–F in the sample road graph.
All distances are illustrative kilometres. Replace the sample data and graph with
real project data if required by your instructor.

## Complexity
- Merge Sort: O(n log n) time.
- 0/1 Knapsack DP: O(nW) time and O(nW) space, where W is capacity.
- Dijkstra with a binary heap: O((V + E) log V).
- Nearest Neighbour: heuristic; this implementation runs Dijkstra from each current stop.

## Important limitation
Nearest Neighbour is an approximation and does not guarantee the globally shortest
Travelling Salesperson route. The sample road network and parcel data are educational.
