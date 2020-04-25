# Reservoir-computing-image-manipulation
A small experiment for implementing an echo state reservoir and using previous image inputs to influence the new image input. 

The implementation attempts to use sparse numpy adjacency matrices to carry data from the previous timestep over to the new one. The algorithm basically does 
 U = dot(Node_Value_Matrix, Adjacency_Matrix)
 Node_Value_Matrix = MapToInterval0To1(Input_Node_Values + self.chaos_factor * U * (1 - U) 
