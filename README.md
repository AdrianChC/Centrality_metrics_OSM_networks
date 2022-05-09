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

# Betweenness Centrality
It is a measure of centrality based on participation of each part on the whole.
That is, roughly speaking, the more a node participates on the shortest path between any pair of nodes the more its betweenness centrality.
This metric is different than those two previously review.
This is different because it is not a local value like Degree of Centrality nor a statistical value derived from the shortest paths.
This is a value that is related to the structure of the network. Because it builds in its relevancy among others places. So it is a global value.
Because the value of a node is related to the value of other nodes.
That is also the reason why high ranked values form a chain of edges. Which is not the case for Cd or Cc metrics.
The distribution of scores seems to be exponential distribution regards of the network.
That is the case of Bhopal (IN) where the highly valuable nodes are arranged in a radial way mostly.

<img src="/Betweenness centrality/figs/01 Cb_Bhopal.png" alt="Cb_Bhopal" width="50%"/>

That is also the case of Lima (PE) which is a network 3 times bigger than Bhopal (IN).

<img src="/Betweenness centrality/figs/04 Cb_Lima.png" alt="Cb_Lima" width="50%"/>

It is evident that their ranges are different but the arrangement is different.
In the case of Bhopal (IN) the highest valuable nodes are the 3% of the network while the same class in Lima (PE) are just 1% of its whole network.
Because Cb shows the opportunity of location and shows a hierarchy passed between edges, it is comparable to the network coding from its urban planning.
Traditional planning classify networks in primary, secondary, tertiary and others.
Comparison between this two are relevant to further understand and manage transport.

<img src="/Betweenness centrality/figs/06 Lima_comparisson.gif" alt="Comparisson_Lima" width="50%"/>

Part of the Cb scores comes from planning itself and the several projects of urban expansion.
However, as cities grows and its network densify, unexpected relevancies appears.
That were opportunity is for planning.
Since Cb offers knowledge to capitalize on the implicit tendency of the network structure.
Which might be convenient or not depending on the case.

# About processing
Both Cd and Cc metrics were made exclusively with Python Qgis algorithms and the GrassGis library for network analysis.
Raster creation was made with the GDAL library which is quite easy to understand.
Both are also quite fast.
However Cb was calculated with R libraries based on igraph.
That was necessary since the GrassGis algorithm produced unreliable results.
Which scores didn’t match with any theory of Betweenness centrality.
So that it is the only one up until know that requires some programming skills.
It also requires heavy computational power.
That is why, it depends on the Brandes Algorithm for an efficient calculus. That is also why it is hard to reproduce manually in a GIU environment. Which is not the case for Cc or Cd metrics.

# More on centrality measures
With easy access to metrics on programming environments it is easy to calculate several other metrics of centrality.
There are four main centrality metrics, 3 of them has been covered.
The last one is the Eigenvalue centrality.
Which will be the last centrality measure on this repository.
However, since there are two other alike measures, next time will be convenient to cover Eigenvalue, PageRank and Katz centrality.
Those three has the same purpose both different calculation.

## Pending issues
- Bibliography
- History of development of Network Metrics (aka Fredman, Social Sciences, etc).
- Next steps: correlation between metrics, real time measurement, mobile data, large scale measurement (i.e country level)
