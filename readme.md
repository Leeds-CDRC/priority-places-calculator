# Priority Places for Food Index Calculator

The Priority Places for Food Index has been developed by the [CDRC](https://cdrc.ac.uk) in partnership with [Which?](https://which.co.uk) to help identify local areas that are most at risk of food insecurity in the context of increases in the cost of living. 

This repository contains all the required code and data sources to build the index data.

## Attribution 

The Priority Places for Food Index is developed by:
- Peter Baudains
- Francesca Pontin

With support from: 

- Emily Ennis
- Michelle Morris
- Robyn Naisbitt
- The team at Which?

The Priority Places for Food Index has been developed by the Consumer Data Research Centre at the University of Leeds in collaboration with Which?. Data used in the development of the index is released under [Open Government License v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). We also acknowledge data provided by the Consumer Data Research Centre, an ESRC Data Investment ES/L011840/1; ES/L011891/1. [Internet User Classification](https://data.cdrc.ac.uk/dataset/internet-user-classification) data by Alexiou, A. and Singleton, A. (2018) contains Ofcom data (2016) and CDRC data from Data Partners (2017). We also acknowledge the [E-Food Desert Index](https://data.cdrc.ac.uk/dataset/e-food-desert-index/), developed by Newing and Videira (2020).

## Setup (using VSCode devcontainer)

To build the index from this repository, you will need to clone the repository and set up a jupyter server with the relevant dependencies installed. We have included a devcontainer within the repository, which can be used with [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [VSCode](https://code.visualstudio.com/) to create an environment and jupyter server within which the index can be constructed. To do this, first clone the repository:

```bash 
# Using github ClI clone the repository locally
$ gh repo clone Leeds-CDRC/priority-places-calculator
```

Then open the directory in VSCode with the relevant [prerequisites](https://code.visualstudio.com/docs/devcontainers/tutorial) installed.

Within VSCode, run the 'Dev Containers: Reopen in Container' command, as shown [here](https://code.visualstudio.com/docs/devcontainers/create-dev-container). 

It may take some time to build, but eventually the repository will re-open inside a container with all requirements for building the index installed. Within a terminal window inside the container, run

```bash 
$ conda init
```

Close and re-open the terminal and then run:

```bash
# Active the priority places conda environment
$conda activate pp-env

# Start the jupyter server and redirect to jupyter lab
jupyter lab
```

This will open a browser window ready to run the following two notebooks, which will create the index data: 

1. data_prep.ipynb
2. index_construction.ipynb

