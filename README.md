# CS 175 Food Hunting Go!
UCI CS 175 Machine Learning Project in MineCraft
- Authors: Chongming Wang, Zeyang Li, Yifan Zhang

<a href="https://github.com/chicomy/CS_175_food_hunting_go/blob/master/docs/index.md">Index Page</a>
- We complete the searching algorithm and map generator. The agent now can discover and retrieve objects on any given map without dying. Moreover, the agent is capable of identifying and relating objects with the landscape. Therefore, on any new maps, the agent will look for places with the highest probability, and searching in a fastest route.
- The agent will firstly avoid lava. However, after exploring the whole map, if the agent has not found everything it is asked to, 
  it will use water to pave a path through lava to keep looking. 
- The agent will dump things that it does not need once in a while. 
- The agent search the map via depth-frist. 

- For future project, we are looking for a functioning agent that can handle a very complex and large-scale map with height and lava situation. That will be more likely to a real-life case.  Putting simply, this agent is capable of training itself on any map. It is training and searching on the same time. This will be the most difficult part of our project.
