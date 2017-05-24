---
layout: default
title: Status
---

In this project, we designed an agent that can search for given objects in an open map, and craft objects based on recipe after retrieving those materials.

The agent will firstly avoid lava. However, after exploring the whole map, if the agent has not found everything it is asked for, it will use water to pave a path through lava to keep searching.

The agent will dump things that it does not need once in a while.

The agent search the map via depth-frist.

If the agent has not collected material it needs, it will go back in a shortest path order to retreive the rest. 
