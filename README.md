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
There are also examples in this twitter thread: 
https://twitter.com/JonRambj/status/1254033803137503232

If chaos_factor is not given it's value is 3.89321543123134709238745. IMO this value produced the most interesting results. 

One limitation to how interesting images the images produced is that by the law of large numbers the random values in the adjacency matrix actually gives similar outputs for any input image each time for the same parameters. If one were to divide up the image into smaller areas and handle each of these seperately one may be able to generate more interesting results. For example, instead of having one large adjacency matrix, an idea could be to instead randomly select some points when initializing the reservoir and dividing the image up into a Voroni diagram depending on the connection values and the distance from the points and handling each Voroni region seperately. 

Using an adjacency matrix was inspired by reading the following paper: 
Pontes-Filho, Sidney; Yazidi, Anis; Zhang, Jianhua; Hammer, Hugo Lewi; Mello, Gustavo; Sandvig, Ioanna; Nichele, Stefano; Tufte, Gunnar.
A general representation of dynamical systems for reservoir computing. I: Proceedings of the 9th Joint IEEE International Conference on Development and Learning and on Epigenetic Robotics. IEEE 2019 ISBN 978-1-5386-8129-9. s. -
OSLOMET NTNU 
link: https://wo.cristin.no/as/WebObjects/cristin.woa/wo/0.Profil.29.25.2.3.15.1.1.3


The program also includes a basic python command line interface which in image_shower.py:
exit - leave program 
reload - reload last loaded image, all of its colorbands
reload R - reload the red color band on the last loaded image
reload B - ...
reload G - ...
step - Do a timestep in the reservoir and output the combination of the reservoir values and the input image if any were loaded on this timestep before calling step. 
load - say that you want to load an image. Will be prompted to write in path to image. Type in the relative path name of the image file. (easiest if image file is in same folder as the code, then you just write ex. "cat.png")
stepseveral - say that you want several timesteps to be done. you will be prompted for how many. Input an integer number above or equal to 0. (nothing happens if you input 0)
reloadstepseveral - same as above, except last loaded image is reloaded before each timestep. 
