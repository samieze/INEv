# INEv: In-Network Evaluation for Event Stream Processing

## Overview

This repository contains the queries and realworld data sets used in our case study, the implementation of algorithms for the construction of INEv graphs and DCEP-Ambrosia - a light-weight implementation for distributed complex event processing using Microsoft Ambrosia.


#### INEv

The directory `INEv` contains the implementation of our algorithms and some of the scripts used to conduct the experiments presented in the paper.

#### DCEP_Engine

The directory `DCEP_Engine` contains the implementation of a light-weight distributed complex event processing engine. INEv graphs constructed in the INEv directory along with their network and query workload specification can be evaluated with the engine by passing the respective evaluation plan as parameter. The input files used to conduct our case study as well as input files for the execution of in-network evaluation based on INEv graphs constructed for synthetic data can be found in `DCEP_Ambrosia/inputexamples`.

#### CaseStudy

The directory contains a description of the queries used in our case study.

