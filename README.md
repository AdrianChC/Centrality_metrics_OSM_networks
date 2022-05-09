# Centrality Metrics based on OSM networks
This is a working progress of centrality metrics calculated from OSM data.
It is based primarily on Qgis, GDAL and GRASS algorithms organized on a series of processing models.
Later on, some other libraries and languages will be included.
There is a metric on each folder. First one is Degree of Centrality (Cd)
Each metrics has its code, some example.
Gradually I will upload the data and other things relevant.

## Degree of Centrality
It’s a measure that express local relevancy.
It measures how many edges are connected directly to a node. 
Which is an expression of immediate opportunity to go other places on the network.
If a node has a Cd equal to 4 that means that you might go from that place to other 4 places.
Which is a quality mentioned by Jane Jacobs on his famous work The Death and Life of Great American Cities (1961), as a desirable quality on neighborhoods. 
Also a quality that influence on the diversity of uses and richness of public life.
The figure expresses the mean value of Cd on a grid of pixels with 500x500m².
This enables the comparisson on the extension of network.
In the case of Lima (PE), it is evident that some large patches have a value between 3 - 4.
Which are mainly in the Historic Centre of the city and some foundational areas of other districts.
Because urbanization processes increments the network and are expression of design.
The Cd value are useful to identify tipologies of urban processes.
For example, patches with a Cd in the range of 3 - 4 might be associated with regular grids and patches with a Cd value in the range of 2 -3 might be associated to other desiging traditions.

<img src="/Degree of Centrality/figs/03 meanCd_Lima.gif" alt="meanCd_Lima" width="50%"/>




