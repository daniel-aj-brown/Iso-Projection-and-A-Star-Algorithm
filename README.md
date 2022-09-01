# Iso-Projection-and-A-Star-Algorithm

An Isometric Projection and A-Star Algorithm Demonstration. By pressing the Space key, the A-Star Algorithm is used to determine the shortest possible route from the start tile to the end tile. The start and end tile begin at point (0, 0) and (3, 3) respectively, but can be changed by the user.

A 2D array is initilised using the number of rows and collums designated by the user, which acts as a tile map. The values of the 2D array indicated the height of the tile at that location, defaulting to zero. Some tiles are then raised to create a basic maze to start with. Coordinates are transferred back and forth between screen space for drawing to the screen and world space for calculations in the algorithm.

The controls are as follows:

- Pan the camera with the direction keys
- Select a tile by moving the mouse.
- Raise and lower the currently selected tile by left and right clicking respectively
- Move the tile to start the algorithm from to the highlighted tile by pressing the 'S' key.
- Move the tile to end the algorithm at to the highlighted tile by pressing the 'E' key.

Please ensure you have the Pygame module installed on your system before running this project.
