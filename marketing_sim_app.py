#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:55:10 2024

@author: robnew
"""

## viral behaviour
# external conversion of individuals in a scope (i.e. marketing push)
# continues over n periods
# in a period:
# a cell changes from 0 to 1 if count(neighbours==1)>= 4
# a cell changes from 1 to 0 if count(neighbours==1)<= 1
# else no change

import numpy as np
import time
from random import randint, random
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import streamlit as st

# Create a color map for 0 and 1
cmap = mcolors.ListedColormap(['white', 'black'])

class Pop:
    
    def __init__(self, rows_cols=100):
        self.data = [np.zeros((rows_cols, rows_cols))]
        # self.fig, self.axes = plt.subplots(nrows = 1, ncols = 2)
        # self.axes[0].imshow(self.data[-1], interpolation='nearest', cmap=cmap)
        # self.axes[0].set_title = 'Population coverage'
        # self.axes[1].plot(range(len(self.data)), [y.sum() for y in self.data])
        # self.axes[1].set_title = 'Total coverage over time'
        # plt.show()
    
    def inject(self, injection_perc = 10, scope_perc = 50):
        ## injection_perc is the % of total population that will be converted
        ## scope_perc is the size of the area where the injection_perc is applied
        ## if injection_perc > scope_perc, 100% of the scope_perc will be converted
        pop = self.data[-1]
        
        scope_perc = min(scope_perc, 99)
        
        scope_size = scope_perc/100*pop.size
        square_size = int(scope_size **0.5) ## find sqrt
        
        max_cell_start = int(pop.shape[0]-(square_size+1))
        injection_size = pop.size * (injection_perc/100)
        
        cell_start_row = randint(0,max_cell_start)
        cell_start_col = randint(0,max_cell_start)
        
        prob_within_scope = injection_size/scope_size
        
        for i in range(cell_start_row, cell_start_row + square_size):
            for j in range(cell_start_col, cell_start_col + square_size):
                if random() <= prob_within_scope:
                    pop[i,j] = 1
        
        self.data.append(pop)
        # self.fig, self.axes = plt.subplots(nrows = 1, ncols = 2)
        # self.axes[0].imshow(self.data[-1], interpolation='nearest', cmap=cmap)
        # self.axes[0].set_title = 'Population coverage'
        # self.axes[1].plot(range(len(self.data)), [y.sum() for y in self.data])
        # self.axes[1].set_title = 'Total coverage over time'
        # plt.show()
        
    
    def evolve(self, distance = 1, thresholds = (1,4), iterate = 1, sleep = 0):
        for iteration in range(iterate):
            pop = self.data[-1]
            pop_1 = deepcopy(pop)
            
            # Dimensions of the matrix
            rows, cols = pop.shape
            
            # Iterate over the matrix
            for i in range(rows):
                for j in range(cols):
                    # Count of neighbors meeting the condition
                    
                    sub = pop[max(i-distance,0):min(i+(distance+1),rows-1), max(j-distance,0):min(j+(distance+1),cols-1)]
                    
                    count = sub.sum()-pop[i,j]
            
                    # Update the cell value based on neighbors
                    # Here, I increase value by 1 if at least 2 neighbors are greater than 3
                    if count >= thresholds[1]:
                        pop_1[i, j] = 1
                    elif count <= thresholds[0]:
                        pop_1[i, j] = 0
                    else:
                        pop_1[i, j] = pop[i, j]
                        
            self.data.append(pop_1)
            # self.fig, self.axes = plt.subplots(nrows = 1, ncols = 2)
            # self.axes[0].imshow(self.data[-1], interpolation='nearest', cmap=cmap)
            # self.axes[0].set_title = 'Population coverage'
            # self.axes[1].plot(range(len(self.data)), [y.sum() for y in self.data])
            # self.axes[1].set_title = 'Total coverage over time'
            # plt.show()
                
            if len(self.data)>1:
                if self.data[-1].sum() == self.data[-2].sum():
                    print(f'Stabised after {str(iteration)} iterations')
                    break
            
            time.sleep(sleep)
     
def spend(budget = 10, spend_per_iteration = 1, scope_target_per_iteration = 50):
    x = Pop()
    while budget > 0:
        x.inject(spend_per_iteration, scope_target_per_iteration)
        budget -= spend_per_iteration
        x.evolve(iterate = 1000000)    

box_size = 100

if 'pop' not in st.session_state:
    st.session_state['pop'] = Pop(rows_cols = box_size)

budget = st.sidebar.number_input('Budget', min_value = 1, max_value = 100, value = 10, step = 1, help = "The percentage of the population that you can afford to reach in total")
spend_per_iteration = st.sidebar.number_input('Spend per iteration', min_value = 1, max_value = 100, value = 1, help = "How much of your budget to spend in one hit")
scope_target_per_iteration = st.sidebar.number_input('Target perc', min_value = 0, max_value = 100, value = 50, step = 1, help = "How wide an area should you spend the amount allotted from your spend this iteration")
pl = st.empty()
if st.sidebar.button("Reset"):
    st.session_state['pop'] = Pop()
if st.sidebar.button("Inject"):
    st.session_state['pop'].inject(injection_perc = spend_per_iteration, scope_perc = scope_target_per_iteration)
    
if st.sidebar.button("Evolve"):
    st.session_state['pop'].evolve()
# if st.button('Spend'):
#     while budget > 0:
#         st.session_state['pop'].inject(spend_per_iteration, scope_target_per_iteration)
#         budget -= spend_per_iteration
#         st.session_state['pop'].evolve(iterate = 1000000) 
        
#         fig, axes = plt.subplots(nrows = 1, ncols = 2)
#         axes[0].imshow(st.session_state['pop'].data[-1], interpolation='nearest', cmap=cmap)
#         axes[0].set_title = 'Population coverage'
#         axes[1].plot(range(len(st.session_state['pop'].data)), [y.sum() for y in st.session_state['pop'].data])
#         axes[1].set_title = 'Total coverage over time'
#         pl.pyplot(fig)

if st.sidebar.button('Spend'):
    iterate = 1000000
    thresholds = (1,4)
    sleep = 0
    distance = 1
    while budget > 0:
        st.session_state['pop'].inject(spend_per_iteration, scope_target_per_iteration)
        budget -= spend_per_iteration
        for iteration in range(iterate):
            pop = st.session_state['pop'].data[-1]
            pop_1 = deepcopy(pop)
            
            # Dimensions of the matrix
            rows, cols = pop.shape
            
            # Iterate over the matrix
            for i in range(rows):
                for j in range(cols):
                    # Count of neighbors meeting the condition
                    
                    sub = pop[max(i-distance,0):min(i+(distance+1),rows-1), max(j-distance,0):min(j+(distance+1),cols-1)]
                    
                    count = sub.sum()-pop[i,j]
            
                    # Update the cell value based on neighbors
                    # Here, I increase value by 1 if at least 2 neighbors are greater than 3
                    if count >= thresholds[1]:
                        pop_1[i, j] = 1
                    elif count <= thresholds[0]:
                        pop_1[i, j] = 0
                    else:
                        pop_1[i, j] = pop[i, j]
                        
            st.session_state['pop'].data.append(pop_1)
            # self.fig, self.axes = plt.subplots(nrows = 1, ncols = 2)
            # self.axes[0].imshow(self.data[-1], interpolation='nearest', cmap=cmap)
            # self.axes[0].set_title = 'Population coverage'
            # self.axes[1].plot(range(len(self.data)), [y.sum() for y in self.data])
            # self.axes[1].set_title = 'Total coverage over time'
            # plt.show()
                
            if len(st.session_state['pop'].data)>1:
                if st.session_state['pop'].data[-1].sum() == st.session_state['pop'].data[-2].sum():
                    print(f'Stabised after {str(iteration)} iterations')
                    break
                
            fig, axes = plt.subplots(nrows = 1, ncols = 2)
            axes[0].imshow(st.session_state['pop'].data[-1], interpolation='nearest', cmap=cmap)
            axes[0].set_title = 'Population coverage'
            axes[1].plot(range(len(st.session_state['pop'].data)), [(y.sum()/(box_size**2))*100 for y in st.session_state['pop'].data])
            axes[1].set_title = 'Total coverage over time'
            pl.pyplot(fig)

fig, axes = plt.subplots(nrows = 1, ncols = 2)
axes[0].imshow(st.session_state['pop'].data[-1], interpolation='nearest', cmap=cmap)
axes[0].set_title = 'Population coverage'
axes[1].plot(range(len(st.session_state['pop'].data)), [(y.sum()/(box_size**2))*100 for y in st.session_state['pop'].data])
axes[1].set_title = 'Total coverage over time'

pl.pyplot(fig)


