Limited steps before infinity; prompt the user if they want to continue finding the objext?

active objects? like a chicken that's constantly changing its location?

ultimate goal: user prompt a number of blocks or CEs to be gathered, the agent find them all in the MC world quick and fast

!!does the agent have VISIAL!???

we make a maze world (2d map at first), put stuffs on random places.

let the agent find them

input is a reciepe.

update: add traps along the way (neg. rewards)： randomly put lavas and water in to the map, if 

pot and and agent start at random position. 

algorithm: explore using BFS; go back to pot after gathering using Dijkstra
also, angent explore the world with vision: now using 2 blocks of vision. if find target in sight, change direction to grab the target instead of the original bfs search path, then go back.

BFS in n+2 
