# Computational Analysis of Functional Guilds

## Description

This repository contains notebooks in `notebooks/` for performing NMF decomposition on functional and taxonomic data, with downstream analysis. Helper functions are located in `scripts/`.

Functional and taxonomic data were obtained from CuratedMetagenomicData through the Bioconductor package in R (see `R_scripts/upload.Rmd`) and subsequently processed as described in `notebooks/4.2_data_preprocessing.ipynb`.

The resulting H and W matrices for both functional (`k = 7`) and taxonomic (`k = 5`) data are located in `results/`.


## Getting Started

#### a) Download version controlled repository
```bash
git clone https://github.com/plantazja/Computational_analysis_of_functional_guilds
cd Computational_analysis_of_functional_guilds
```

#### b) Create virtual environment from requirements.txt
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt 
```

## Acknowledgments

The nine-fold bi-cross-validation and NMF procedures were adapted from Frioux et al. (2023).

* [Enterosignature Paper](https://gitlab.inria.fr/cfrioux/enterosignature-paper)