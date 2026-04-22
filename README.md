



Django Machine Test – Flight Routes System

This project is a Django-based web application developed to manage airport routes using a structured tree/graph model. It enables users to create and manage airport connections by adding routes with details such as source airport, destination airport, positional relationship (left or right), and duration or distance between them, forming the core dataset for route calculations. The application includes a feature to find the Nth left or right node, where users can start from a selected airport and traverse in a specified direction to reach a target node, with the system displaying the final node along with the complete path and total distance covered. It also provides functionality to determine the longest node based on duration by evaluating all possible paths from the root airport and identifying the route with the maximum cumulative distance, displaying the destination node, path, and total duration. Additionally, the system supports finding the shortest path between two airports by allowing users to input a source and destination, automatically computing the optimal route and presenting a step-by-step breakdown of distances between intermediate nodes, such as C → K = 22 km and K → R = 19 km, while also highlighting the shortest segment. The project is built using Python and the Django framework for backend development, along with HTML and CSS for frontend rendering, and demonstrates the practical application of data structures and algorithms such as BFS and DFS in solving real-world routing problems within a clean and user-friendly web interface.


https://github.com/user-attachments/assets/2fd1b71a-4753-4f61-ab22-430634d283fd

