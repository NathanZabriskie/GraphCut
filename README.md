# GraphCut

An implementation of the graph cut algorithm with a custom GUI written in PyQt. 
Using the interface users mark the foreground and background of the image. Using this information,
the program builds a graph from the image pixels where the weights between pixels
represent the difference between them. To segment the image a minimum cut is performed on the graph.

The interface:
![GUI](https://github.com/NathanZabriskie/GraphCut/blob/master/images/graphCut.png "Custom PyQT interface")

And an example result:

![before](https://github.com/NathanZabriskie/GraphCut/blob/master/resource/dood.jpg "Before")
![after](https://github.com/NathanZabriskie/GraphCut/blob/master/images/segmented.png "After")

To run the program start up NewCutUI.py
