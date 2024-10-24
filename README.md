# networks_and_data

[![PyPI - Version](https://img.shields.io/pypi/v/networks-and-data.svg)](https://pypi.org/project/networks-and-data)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/networks-and-data.svg)](https://pypi.org/project/networks-and-data)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)
-[Modules](#Modules)

## Installation

```console
pip install networks-and-data
```

## License

`networks-and-data` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Modules 
### network_functions 
This module just has a couple of network based functions. 

a. add_num(a,b)

   Input: Two numbers a and b. 

   Output: Sum of these numbers 

The purpose of this function is just to test that you have imported the package successfully. 

b. degree_distribution(G, number_of_bins=15, log_binning=True, density=True, directed=False)

   Input: 

   G = Networkx graph 

   number_of_bins = Number of bins can be adjusted by the user according to the graph 

   log_binning = if True, implements log binning. If False, implements linear binning 

   density = if True, returns probability density. If False, returns counts 

   directed = True if your network is directed and false if it isnt. 

   Output: 

   Array (probability densitiy/counts, bins)

c. plot_degree_distribution(G, number_of_bins=15, log_binning=True, density=True, directed=False)

   Input: 

   G = Networkx graph 
   
   Same as degree distribution
   Output:

   A matplotlib plot of degree distribution. 

d. configuration_model_from_degree_sequence(G, return_simple=True)

   Input: 

   G = Networkx Graph 

   Output: 

   Randomized graph based on configuration model

### Openalex_data
a. fetch_results_mini(url, p1, p2, mailto)

   url: API query from the OpenAlex website (remove the part page=1 if you want to access more than 1 pages)

   p1: Starting page number (25 results per page)

   p2: ENding page number 

   mailto: you email id (in double quotes)

   Output: 

   List of all the results. This function can only access upto first 75000 results in the API query. 

b. fetch_results_in_range(base_url, start, end, mailto):

   base_url = API query from the OpenAlex website (remove the part page=1 if you want to access more than 1 pages)

   start = Starting record number 

   end = ending record number (end - start =< 100000)

   mailto = you email id 

   Output: 

   List of all your results. 

c. save_to_json(data, filename)

   Input: 

   data = list (generated by above functions) containing all the results 
   from API 
   
   Output: 

   JSON data file 

d. institution_collaborations(all_data)

   Input: 

   all_data = List of all results from API query 

   Output:

   Dictionary of collaboration between universities i.e. University 1, University 2 : weight. 

e. load_from_json(filename)

   Input: 

   filename= JSON file 

   Output:
   
   Contents of the file imported in List format. 
   