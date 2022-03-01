# INEv: In-Network Evaluation for Event Stream Processing

## Overview

This repository contains the queries and realworld data sets used in our case study, the implementation of algorithms for the construction of INEv graphs and DCEP-Ambrosia - a light-weight implementation for distributed complex event processing using Microsoft Ambrosia.


#### INEv

The directory `INEv` contains the implementation of our algorithms and the scripts used to conduct the experiments presented in the paper.

#### DCEP_Ambrosia

The directory `DCEP_Ambrosia` contains the implementation of light-weight distributed complex event processing engine using Microsoft Ambrosia for fault-tolerant communication. The query processor can alternatively be started as a simulation which does not require to locally set up Ambrosia.
The input files used to conduct our case study as well as input files for the execution of in-network evaluation based on INEv graphs constructed for synthetic data can be found in `DCEP_Ambrosia/inputexamples`.

#### CaseStudy

The directory contains a description of the queries used in our case study.

