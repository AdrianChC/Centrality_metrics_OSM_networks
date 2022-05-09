

## load libraries
library(sf)
library(tidygraph)
library(igraph)
library(dplyr)
library(tibble)
library(ggplot2)


# opening data (geopackage to sf)----
edges_lima <- 
  st_read("edges_lima.gpkg")

#ggplot(data = edges_lima) + geom_sf()

head(edges_lima)

# creating derived nodes ----
# adding an explicit edgeID
edges_LIM <- 
  edges_lima %>% 
  mutate(
    edgeID =
      c(1:n())
  )

# creating nodes
nodes_LIM <- 
  edges_LIM %>%
  # extract all vertex
  st_coordinates() %>%
  # convert the class to a tibble
  as_tibble() %>%
  # rename the attribute L1 to refer to its origin edge 
  rename(
    edgeID = L1
  ) %>%
  # grouping by edges
  group_by(
    edgeID
  ) %>%
  # extract the first vertex and last vertex (aka n() vertex) by 'edgeID'
  slice(
    c(1, n())
  ) %>%
  # ungroup data
  ungroup() %>%
  mutate(
    # classifies the first and last vertex with 'start' or 'end' attribute by
    # relying that the data is previously arranged by edge so that
    # the 'start' and 'end' fit only once on each edge
    start_end = 
      rep(c('start','end'), times = n()/2)
  )

head(nodes_LIM)


# nodes unique index
nodes_LIM <- 
  nodes_LIM %>%
  mutate(
    # creates an attribute with X Y data
    xy = 
      paste(.$X, .$Y)
  ) %>% 
  mutate(
    # creates a node ID considering that most nodes are the starting vertex or
    # the ending vertex of some other edge
    # group_indices provides an index value based on the n_group value
    # factor creates factor values based on xy attribute
    # levels creates factor values based on an specific dat (i.e:vector)
    # unique() defines the vector as the unique values of xy attribute
    # so, this command creates a unique node ID
    nodeID = 
      group_indices(., factor(xy, levels = unique(xy)))
  ) %>%
  select(-xy)

head(nodes_LIM)


# combine node indices with edges ----
# splitting nodes with 'start' or 'end' values
source_nodes_LIM <- 
  nodes_LIM %>%
  filter(
    start_end == 'start'
  ) %>%
  pull(nodeID)

target_nodes_LIM <- 
  nodes_LIM %>%
  filter(
    start_end == 'end'
  ) %>%
  pull(nodeID)

edges_LIM <-  
  edges_LIM %>%
  mutate(
    from = source_nodes_LIM, 
    to = target_nodes_LIM)

head(edges_LIM)

# remove duplicate nodes
nodes_LIM <- 
  nodes_LIM %>%
  # deleting nodes by keeping one 'nodeID' and all attributes
  # until now there the points were made based on the edges so
  # it has nodes with same geometry but related to different edges
  distinct(
    nodeID, .keep_all = TRUE
  ) %>%
  # delete some of attributes
  select(
    -c(edgeID, start_end)
  ) %>%
  # converting the data into a sf object (simple feature)
  st_as_sf(
    coords = c('X', 'Y')
  ) %>%
  # setting the crs
  st_set_crs(
    st_crs(edges_LIM)
  )

head(nodes_LIM)


# converting to tbl_graph ----
# creates a undirected graph with nodes and edges data 
graph_LIM  <-  
  tbl_graph(
    nodes = nodes_LIM, 
    # because edges as sf would cause a duplication of geometry values
    # as a tibble it loses the geometry and works
    #edges = as_tibble(edges), 
    edges = as_tibble(edges_LIM),
    directed = FALSE
  )

head(graph_LIM)

# exploring the functionality of graph object ----
# adding length values to edges
graph_LIM <- 
  graph_LIM %>%
  activate(
    edges
  ) %>%
  mutate(
    length = 
      st_length(st_geometry(edges_LIM))
  )

# centrality measures ----
## calculate centrality of degree ----
graph_LIM <- 
  graph_LIM %>%
  # calling the nodes
  activate(
    nodes
  ) %>%
  mutate(
    # calculating the centrality of degree
    degree = 
      centrality_degree()
  ) 

## calculate centrality of betweeness ----
graph_LIM <- 
  graph_LIM %>%
  # calling the nodes
  activate(
    nodes
  ) %>%
  mutate(
    # calculating centrality of betweeness for nodes
    betweenness = 
      centrality_betweenness(
        directed = FALSE, 
        weights = length
      )
  )


# creating classes for each measure ----
# Centrality of betweeness and closeness
graph_LIM <- 
  graph_LIM %>%
  # calling the nodes
  activate(
    nodes
  ) %>%
  mutate(
    # calculating centrality of betweeness for nodes
    Cb = 
      case_when(
        betweenness == 0 ~ 0,
        betweenness == max(betweenness) ~ 7,
        betweenness <= mean(betweenness) - 2*sd(betweenness) ~ 1,
        betweenness > mean(betweenness) - 2*sd(betweenness) &
          betweenness <= mean(betweenness) - 1*sd(betweenness) ~ 2,
        betweenness > mean(betweenness) - 1*sd(betweenness) &
          betweenness <= mean(betweenness) - 0*sd(betweenness) ~ 3,
        betweenness > mean(betweenness) - 0*sd(betweenness) &
          betweenness <= mean(betweenness) + 1*sd(betweenness) ~ 4,
        betweenness > mean(betweenness) + 1*sd(betweenness) &
          betweenness <= mean(betweenness) + 2*sd(betweenness) ~ 5,
        betweenness > mean(betweenness) + 2*sd(betweenness) ~ 6
      )
  )


# calculate centrality of eigenvalue ----
graph_LIM <- 
  graph_LIM %>% 
  # calling the edges
  activate(
    nodes
  ) %>% 
  mutate(
    # calculating the eigenvalue for nodes
    # remember that this calculus is made with Tidygraph
    eigen =
      centrality_eigen(
        directed = FALSE,
        weights = length,
        scale = FALSE
      )
  )


# plotting it
ggplot() +
  geom_sf(
    data = graph_LIM %>% 
      activate(edges) %>% 
      as_tibble() %>% 
      st_as_sf(), 
    col = 'grey50') +
  geom_sf(
    data = graph_LIM %>% 
      activate(nodes) %>% 
      as_tibble() %>% 
      st_as_sf(), 
    aes(col = eigen)
  ) +
  scale_colour_viridis_c(
    option = 'viridis'
  )

# exporting sf objects ----
# the nodes
st_write(
  graph_LIM %>%
    # turning edges or nodes as the active layer 
    activate(
      nodes
    ) %>%
    # converting the edge's graph data into a tibble
    as_tibble() %>%
    # turning it into simple feature
    st_as_sf(),
  "nodes_LIM_eigen.gpkg", 
  driver = "GPKG"
)
  
  
