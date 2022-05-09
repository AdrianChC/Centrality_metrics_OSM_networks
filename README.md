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
This enables the comparison on the extension of network.
In the case of Lima (PE), it is evident that some large patches have a value around 3 - 4.
Which are mainly in the Historic Centre of the city and some foundational areas of other districts.
Because urbanization processes increments the network and are expression of design.
The Cd value are useful to identify typologies of urban processes.
For example, patches with a Cd in the range of 3 - 4 might be associated with regular grids and patches with a Cd value in the range of 2 -3 might be associated to other designing traditions.

<img src="/Degree of Centrality/figs/03 meanCd_Lima.gif" alt="meanCd_Lima" width="50%"/>

# Closeness Centrality
It’s a measure of centrality derived from the notion that a node relevancy relies on its distance to all network.
That is, if a node is close to all of the network that means that it is central.
Its calculus comes after the mean value of the shortest paths to all other nodes on the network.
Some version of this measure considers the inverse value x^-1.
Since it is easier to understand the Cc value as the mean distance, here it is used in that way.
I believed this version is called Farness. Here is called Cc anyway because the scores are more relatable.
It might be intuitively associated with the geometry of the network.
But that is not precise.
It heavily relies on the distance between nodes.
In a similar fashion that Cd, it is expressed on a grid made of pixels with 500x500m².
Classes are derived from the statistical values (mean and standard deviation).
The less central areas are located on the periphery of the city.
That is a result of this areas being far from the whole city despite being strongly close to one side of it.
In the case of Lima (PE), the Historic Centre is also the most central place.
Not because it is at the geometric center of the network.
Instead, because it is well connected to the whole network and their shortest paths are less than 19 km.
Of course, a trip of 19 km seems extremely long but in the scale of a city as big as Lima. That is not so long compared to an average distance of 42 km which is the case for the less central values on this city.

<img src="/Closeness centrality/figs/01 meanCc_Lima.png" alt="meanCc_Lima" width="50%"/>

