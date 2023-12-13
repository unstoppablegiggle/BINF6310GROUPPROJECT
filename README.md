#BINF6310 Ace Squad Group Project

#Introduction

Welcome to the BINF6310 Ace Squad group project, focused on conducting a reproducibility study of the workflow described in the paper titled "Genome-wide prediction of disease variant effects with a deep protein language model" published in Nature Genetics. This repository contains all the necessary code, data, and documentation to replicate the results of the original study.

Original Paper: [Link to Paper](https://www.nature.com/articles/s41588-023-01465-0)

GitHub Repository: [Link to Repository](https://github.com/ntranoslab/esm-variants)

We strongly recommend familiarizing yourself with the original work before exploring our repository.
Repository Contents
Scripts

The scripts directory contains all the code required to reproduce the study's results. This includes:

    Scripts for generating figures presented in the project. These scripts provide visual representations of the data and findings.

    A modified version of the "esm score" program, optimized for user-friendliness and memory efficiency. This modified program enables execution on standard desktop computers.

    A Conda environment YAML file, specifying the necessary Python environment and dependencies for running the modified "esm score" program.

    Bash scripts tailored for executing the program in a High-Performance Computing (HPC) environment, suitable for computationally intensive tasks.

##Figures

Inside the figures directory, you will find all the figures that have been reproduced as part of our project. These figures offer insights and visualizations derived from the analysis of the provided data.

##Data

The data directory houses all the raw data generated during our reproducibility study. Please note that the Uniprot primary isoform LLR scores file, which exceeds 15GB in size, is not included in this directory due to size constraints. However, it is available upon request. The data is an integral part of our study and serves as the foundation for our analysis.
