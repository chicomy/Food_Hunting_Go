Our agent is designed to learn about corresponding relationship between terrain blocks and objects on it, and it will apply what it has learnt in a more complex map to find objects it is asked for. It is like an auto-robot for searching required objects in places that human cannot reach, such as deep forest or seafloor. It will optimize its path while it is searching. 
On the right side is a training map, which is divided into four pieces with objects on it. Most objects are bind onto a certain type of block, but there are outliers just to confuse our agent. Expect some unexpected. 
Our agent traverses the training map via depth-first algorithm. It will learn that pumpkins are on sandstone; eggs are on diamond, and so on. 
Map:
As you can see, there are blocks 
After that, our agent is put at the right corner on the test map, which is a 27 by 27 concluding 81 groups of different blocks, and not every block has its assigned objects. Obsidian and apple are considered outliers here. The agent is using A-start search to evaluate four steps ahead of its current location, and return a potentially best direction. The agent ranks those blocks on various standards, including the worthy status of this block (visited, unvisited but not valuable, and valuable) and the path of this block (how many steps have to be made to move to this block). The challenge part is that the priority changes as every step it takes and items it finds. 



Random	
[521, 61, 146, 38, 36, 439, 143, 240, 29, 93]
Max = 521 	Min = 29 	AVG = 174.6	SD = 165.718556595

DFS
[42, 14, 68, 67, 16, 69, 82, 55, 70, 42, 69]
Max = 82		Min = 14		AVG = 54.0	SD = 21.7171905097

A* method
[12, 14, 6, 14, 24, 22, 26, 22, 20, 19]
Max = 26 	Min = 6		AVG = 17.9	SD = 5.90677577025

