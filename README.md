# How do rumour and non-rumour travel beyond their echo chamber?
Author: Yu-Hung, Chiang  
Code Language: Python 3

The codes were written in conjunction with my bachelor thesis at the University of Groningen. The following are descriptions and notices on implementing and interpreting my code.


## General Structure
The codes are built directly upon the PHEME data-set itself(https://figshare.com/articles/dataset/PHEME_rumour_scheme_dataset_journalism_use_case/2068650). Therefore, all the original data can be found in their original directories. 

Each directory contains a header file and a Jupyter Notebook file. The header file contains functions that are applied in the Jupyter Notebook. Above each function has code annotations that describe the purpose of the function and its inputs and outputs. The process of analysis is documented in each Jupyter Notebook. Descriptions are either above the code block or commented within the code block itself. 

The main Jupyter Notebook file and header file that resides at the root of this directory are mostly for data preprocessing. Other analyses, such as bridge identification and centrality analysis, are organized into their corresponding folders. Figures folder contains all images that are generated during my research process. 

## Side Notes
All types of input graphs are based on the graph type defined by NetworkX. It is recommended to read into NetworkX graph visualization algorithms for a better understanding of the graph construction and other possible methods of graph visualization. For the Latex table generator, I used an extended library from texttable (https://pypi.org/project/texttable/).

