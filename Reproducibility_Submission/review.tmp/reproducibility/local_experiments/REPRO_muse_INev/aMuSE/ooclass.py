#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:11:44 2020

@author: samira
"""

class OperatorPlacementProblem:
    def __init__(self, network, event_rates, operator_inputs,central_costs, experiment_id, experiment_params):
        self.network = network
        self.event_rates = event_rates
        self.operator_inputs = operator_inputs
        self.central_costs = central_costs
        self.experiment_id = experiment_id
        self.experiment_params = experiment_params
