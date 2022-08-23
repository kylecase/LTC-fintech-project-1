# Initial imports
import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
from MCForecastTools import MCSimulation
import hvplot.pandas
from pathlib import Path
import seaborn as sns
%matplotlib inline
import numpy as np

# Load .env environment variables
load_dotenv()

#Set CovalentHQ API Key and check length = 32
covalenthq_api_key = os.getenv("COVALENTHQ_API_KEY")
len(covalenthq_api_key)


class uniswap_lookup:
    
    def symbol_check(symbol_weight):
        
    
    