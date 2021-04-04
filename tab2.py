# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 18:08:47 2021

@author: MOHAMED
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


df = pd.read_csv('movies.csv',encoding='latin1')