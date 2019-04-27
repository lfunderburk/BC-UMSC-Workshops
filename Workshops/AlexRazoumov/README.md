### WORKSHOP DETAILS

In this workshop, participants will learn to perform (2D/3D) data visualization using Python 3 along with
Paraview. Participants will have an opportunity to familiarise themselves with a subset of the data they
will work with during the Data Visualisation competition, and perform a series of exercises to visualise
it.

### SOFTWARE INSTALLATION

1. For your OS install ParaView from http://www.paraview.org/download
1. For your OS install Python3.7 Miniconda distribution from http://conda.pydata.org/miniconda.html
1. Start the command-line shell (terminal in MacOS/Linux, Anaconda Powershell Prompt in Windows) and then install the
   required Python packages:

~~~
conda install numpy vtk pandas
~~~

<!-- These are likely not needed: -->
<!-- networkx gensim scikit-learn pandas jupyter plotly scipy -->

### Files to download

We will be using a subset of slides from a full-day ParaView workshop. Please download and unpack a
[ZIP file](http://bit.ly/paraviewzip) containing the slides, sample codes and datasets.

Please also download the following files from this directory:

* **ferryData.csv** is the dataset we will be visualizing,
* **writeNodesEdges.py** is a Python script to write points and graphs to a VTK file.

### Live code

* **scatter.py** is the live code
