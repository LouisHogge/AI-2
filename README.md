# Introduction to Artificial Intelligence Project 2

## Project Description
In Project 1, Pacman could wander peacefully in the maze. Now, he needs to avoid a walking ghost that would kill him if it reached his position. Pacman does not know what is the strategy of the ghost, but he has access to the ghost's legal actions through the API. In particular, a ghost can go forward, turn left or right, but cannot make a half-turn unless it has no other choice.

Your task is to design an intelligent agent based on adversarial search algorithms (see Lecture 3) for maximizing the score of Pacman. You are asked to implement the Minimax and H-Minimax algorithms where Pacman and the ghost are the two players. We recommend to implement the algorithms in this order. It is mandatory to use only the API to retrieve game information. Layouts with capsules will not be considered, but you may take them into account if you feel motivated. Your implementation of Minimax does not need to run on the medium\_adv and large\_adv layouts.

## How to Use the Project
For example, use the following command to run your Minimax implementation against the dumby ghost in the small layout:
```bash
python run.py --agent minimax --ghost dumby --layout small_adv
```
