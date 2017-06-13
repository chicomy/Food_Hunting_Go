Our agent is designed to learn about corresponding relationship between terrain blocks and objects on it, and it will apply what it has learnt in a more complex map to find objects it is asked for. It is like an auto-robot for searching required objects in places that human cannot reach, such as deep forest or seafloor. It will optimize its path while it is searching. 
On the right side is a training map, which is divided into four pieces with objects on it. Most objects are bind onto a certain type of block, but there are outliers just to confuse our agent. Expect some unexpected. 
Our agent traverses the training map via depth-first algorithm. It will learn that pumpkins are on sandstone; eggs are on diamond, and so on. 
Map:
As you can see, there are blocks 
After that, our agent is put at the right corner on the test map, which is a 27 by 27 concluding 81 groups of different blocks, and not every block has its assigned objects. Obsidian and apple are considered outliers here. The agent is using A-start search to evaluate four steps ahead of its current location, and return a potentially best direction. The agent ranks those blocks on various standards, including the worthy status of this block (visited, unvisited but not valuable, and valuable) and the path of this block (how many steps have to be made to move to this block). The challenge part is that the priority changes as every step it takes and items it finds. 

Part 2: Searching algorithm
1. Graph construction
We first construct a graph representation from the test map mentioned above. The graph representation is like this

<img src="docs/Photos/graphdata.png" alt="graph_repre" style="width: 45%;">

<img src="docs/Photos/node_sampe.png" alt="example" style="width: 45%;">

2. A-star heuristic search algorithm
the formular of A-star search is this: 
### F(n) = G(n) + H(n) ###
  - *For G(n)*: Since every block placed next to each other, so the edge weight is just 1, which means that G(n) is als 1 for each depth
  - *For H(n)*: We decided to use 3-depth heuristic cost evaluation: for each of the four possible direction our agent can make, it evaluates states in 3 steps. For each of these states, we evaluate four aspects:
  - whether the state has item that we are looking for
  - whether the state has item that we already found
  - whether the state has been visited

Also, in order to prevent agent from falling down the sky, we give H(n) = 1000 when it find a near by node state to be 0 (i.e. "air") at depth 1. What's more, for the nodes that next to current node, we give then 2 times heuristic value since they are more important for agent to consider. Now we calculate each state's G(n) and H(n) value, and add them up, which is the F(n) of one direction. Then we find the direction with the lowest F(n) value, and go towards that direction. The image below is a detailed illustration.
<img src="docs/Photos/hn_demo.png" alt="heuristic" style="width: 45%;">

- *Specific heuristc values*: We have done a lot of experiments to improve the performance of the agent. The initial values we used and the performance are shown blow in chart.
<img src="docs/Photos/h1.png" alt="h1" style="width: 45%;">

Along the process of heavily experimenting, we found that the agent has several things can be improved:
1. Add more cost for blocks that already visited: (Times of visit) times (heuristic value for visited)
  - solved dead loop
2. Add heuristic cost to "air" block at depth 2 and 3
  - improved the performace that the agent tends to search towards the boundary
3. Add more rewards (negative cost) to nodes that might have items on it
  - made the agent more "greedy"
4. Increased G(n) at depth 2 and 3
  - made the near by node lower F(n)
  
After a great amount of testing, we ended up with values like this:
<img src="docs/Photos/h2.png" alt="h2" style="width: 45%;">

Even though the algorithm is not perfect, guarenteed optimal solution, but we are satisfied with this performance considering agents limited sight. Ellaborate more in evaluations
Random	
[521, 61, 146, 38, 36, 439, 143, 240, 29, 93]
Max = 521 	Min = 29 	AVG = 174.6	SD = 165.718556595

DFS
[42, 14, 68, 67, 16, 69, 82, 55, 70, 42, 69]
Max = 82		Min = 14		AVG = 54.0	SD = 21.7171905097

A* method
[12, 14, 6, 14, 24, 22, 26, 22, 20, 19]
Max = 26 	Min = 6		AVG = 17.9	SD = 5.90677577025

