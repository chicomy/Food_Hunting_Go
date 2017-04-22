---
layout: default
title:  Proposal
---

## 2.2 Summary of the Project (30 points)
The main idea of this project is to build an AI that can find a target object, (i.e. a certain block) and the fastest way to travel back to the original position. The input will be the whole MC world, and the name of an object, i.e. chicken, Redstone and such. It will return if the agent is able to find the object and the fastest route if it does find something. The fastest route does not mean the same as the shortest route. Walking in water and jumping up a block may delay the speed of traveling, so the fastest route can be different from shortest. 

Application could be to locate NPC or find quest destination in MMORPG games.

## 2.3 AI/ML Algorithms (10 points) 
AI:Using Dijkstra Algorithm to find routes. 
ML:Learning the routine of where these objects might be (i.e. chicken tends to be in pond)

## 2.4 Evaluation Plan (30 points) 
As described in class, mention how you will evaluate the success of your project. 
In a paragraph, focus on the quantitative evaluation: what are the metrics, what are the baselines, how much you expect your approach to improve the metric by, what data will you evaluate on, etc. 

To verify the algorithm, first we can randomly assign objects that exist to test if the agent can find those. Next, we can compare it to the shortest path to see which one takes less time. It is interesting to see an AI searching around an open map and return with information it observes along the way. We want it to be more sensible later, for example, to know that there are likely to have trees on grass rather than sand. In other word, it will choose which part of the map may contain the target object to begin search with. 
