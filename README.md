# Hypergraph Calculator

A simple Python program with a graphical user interface (Tkinter) for creating, iteratively evolving, and visualizing hypergraphs.

## Features

* Graphical user interface (GUI) for easy control.
* Definition of vertices using a text field and button.
* Creation of hyperedges by selecting vertices from a list.
* Application of a predefined evolution rule to the hypergraph.
* Setting the number of evolution rule iterations.
* Visualization of the resulting hypergraph (vertices as points, hyperedges as circles surrounding the vertices).
* Display of basic hypergraph information (list of hyperedges, vertex degrees, hyperedge degrees, connected components).
* Option to clear input data and output.

## Requirements

* Python 3.x
* Tkinter (usually included with standard Python installations)
* NetworkX
* Matplotlib
* NumPy

Running the Program

Ensure you have all the files (gui.py, main.py - if using two files) in the same directory. Without installation, just Run the main GUI file:
Bash - python gui.py


Usage

    Adding Vertices: Enter the vertex name in the "Vrchol" (Vertex) field and click "Přidat vrchol" (Add Vertex). Repeat for all desired vertices.
    Adding Hyperedges: Select the desired vertices in the "Vrcholy" (Vertices) list (Ctrl+click or Shift+click for multiple selection) and click "Přidat hyperhranu" (Add Hyperedge). Repeat for all desired hyperedges.
    Number of Iterations: Enter the desired number of rule iterations in the "Počet iterací" (Number of Iterations) field.
    Generate Hypergraph: Click "Generuj hypergraf" (Generate Hypergraph). This creates the internal representation of the hypergraph based on the defined hyperedges. Information will be displayed in the output field.
    Apply Rule: Click "Aplikuj pravidlo" (Apply Rule). The program applies the predefined evolution rule for the specified number of iterations. The output field will be updated.
    Visualize: Click "Vizualizuj" (Visualize). A new window will appear with the graphical representation of the hypergraph.
    Clear: Click "Vyčistit" (Clear) to delete all entered data and reset the interface.

Note on the Evolution Rule

The currently implemented rule (pravidlo in the code) creates new hyperedges by taking all existing vertices and creating a hyperedge for each pair of vertices (including pairs of the same vertex).
Note on Visualization

The visualization displays vertices as points and hyperedges as circles surrounding these points. This is a basic representation and might not be ideal for all types of hypergraphs.
