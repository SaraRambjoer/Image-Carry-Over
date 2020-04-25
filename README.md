# Image-Carry-Over
A small experiment for implementing an echo state reservoir and using previous image inputs to influence the new image input for purposes of generating cool art. 

The implementation attempts to use sparse numpy adjacency matrices to carry data from the previous timestep over to the new one. The algorithm basically does 
 U = dot(Node_Value_Matrix, Adjacency_Matrix)
 Map U to values between 0 and 1
 Node_Value_Matrix = Input_Node_Values + self.chaos_factor * U * (1 - U) 
 Map Node_Value_Matrix to values between 0 and 1
 
 The code also contains an older algorithm which did not map U to values between 0 and 1 but instead divided it by the amount of elements in the adjacency matrix. The newer version allows for far lower values of alpha while still giving interesting output. 
 
 
There are a couple of hyperparameters: 
alpha: percentage of fields in adjacency matrix that should have non-zero values 
min_connection: minimum connection strength in adjacency matrix
max_connection: max connection strength in adjacency matrix

Generally for connection values between 0 and 1 a lower value of alpha (above 0.0005) corresponds to higher connection value bounds, which means that one should pick a low alpha and instead adjust min and max connection strength, because lower alphas make the math run far quicker because the implementation uses sparse matrixes. This is likely due to the large amount of values involved in a adjacency matrix (which is of the size (width x height, width x height))

height and width each image should be mapped to

chaos_factor = parameter for the logistic function (or more specifically, a derivative of it used in population modeling dn/dr = n(1-n) where n is population size and r is timestep). Parameter can also be viewed as a weighting between the data in the new input image and the reservoir output when producing the new output image. 

There are four image files included. Their naming convention is 
alpha-min_connection-max_connection-timestamp.png

If chaos_factor is not given it's value is 3.89321543123134709238745. IMO this value produced the most interesting results. 

One limitation to how interesting images the images produced is that by the law of large numbers the random values in the adjacency matrix actually gives similar outputs for any input image each time for the same parameters. If one were to divide up the image into smaller areas and handle each of these seperately one may be able to generate more interesting results. For example, instead of having one large adjacency matrix, an idea could be to instead randomly select some points when initializing the reservoir and dividing the image up into a Voroni diagram depending on the connection values and the distance from the points and handling each Voroni region seperately. 

