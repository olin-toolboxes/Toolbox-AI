To use this astar GUI/toy, hit the 'l' key to switch to the 'add lava tiles' mode. Then you can click on any cell to add or remove a lava tile from that cell. Hit the spacebar at any time to have Paul plan (or replan) his path, and highlight that path. To see the f,g, and h values that astar calculates, take a look at the instructions in question 1. Feel free to reach out at any time about problems.

0. Read up on astar [here](http://web.mit.edu/eranki/www/tutorials/search/) and [here](http://www.raywenderlich.com/4946/introduction-to-a-pathfinding). Do your best to understand what the pseudocode in the links mean. What are the advantages that A star has over breadth-first search? What advantages does A star have over depth-first search?

Breadth-first is already better than depth-first because it searches its surroundings in a rudimentary way instead of visiting every node randomly, but Astar is better because of the way it utilizes the g and h values over just checking surrounding tiles blindly. This means Astar will be faster than either breath or depth first.



1. Take a look at lines 124-127 of the code. Try commenting and uncommenting lines and running python astar.py to see what values are printed in each cell. Take a screenshot of each example with some lava tiles placed down, and in your own words, explain what f_score, g_score, and h_score are, and why you see those specific values in the screenshot.

g_score is the distance or cost it took to get to the node. For the tile example, the cost for travelling between tiles is one. Between two tiles, it is 2 and so on.
h_score is the estimated cost to the node.
f_score is the combination of g and h. This combination is what makes Astar work better than other searches because it shows the cost relative to how much it should approximately cost and looks for a combination of the lowest h and g values.
The screenshots are located in the f_g_h file.



For questions 2, 3, and 4, you should implement the code to get the specified behavior, but also place tiles and set up a scenario/path where that newly implemented behavior is demonstrated (ex. Paul moving diagonally or moving through a swamp.) Then include a screenshot and explanation. Quoting Paul, "Once you make a change, you should include a screenshot of the pygame window that shows the generated path for a given set of obstacles. You should be ready to explain why the shown path is actually the shortest (for instance… “the diagonal move while costly, is necessary in order to reach the goal, paths consisting of just up, down, left, or right would not be able to reach the goal”)."




2. Read the get_open_adj_coords() function and lines 204 to 210 to get an idea of how valid adjacent cells are found. In the current code, valid adjacent cells only include the surrounding cells in the 4 cardinal directions, and moving to any of these cells costs 1 movement point. Add code changing the get_open_adj_coords() function so that surrounding diagonal cells are considered valid adjacent cells and moving to any of these cells costs 3 movement points. This will allow Paul to move diagonally.

Screenshot is in the modImg folder.
This screenshot shows that diagonal movement is possible. However, whenever Paul can avoid
moving diagonally he does (as shown by the top left and bottom right of the window) because moving diagonally is more costly.



3. Change the program so that pressing 's' allows you to add swamp tiles. Paul should be able to move through swamp tiles, but they will slow him down! Moving into a swamp tile will cost 3 movement points, so Paul should really avoid moving through swamp tiles unless he has to. A swamp.jpg file has been provided for you in the /images folder. You will probably have to make some changes to the costs in get_open_adj_coords and write your own _add_swamp()_ function to get swamp tiles to behave correctly.

Screenshot is in the modImg folder.
This screenshot shows that hopping is now possible. Paul will avoid this when possible because the cost is so high.



4. Evolve Paul and allow him to jump over lava! Add the ability for Paul to jump one square. This should cost 8 movement points, however. This will involve changing get_open_adj_coords().

Screenshot is in the modImg folder.
The image shows that Paul can cross swamps and the cost is increased (looking at the f value).
