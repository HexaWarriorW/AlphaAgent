import pandas as pd                                                                                                                    
import numpy as np                                                                                                                     
import os                                                                                                                              
from alphaagent.components.coder.factor_coder.expr_parser import parse_expression, parse_symbol                                        
from alphaagent.components.coder.factor_coder.function_lib import *                                                                    


def calculate_factor(expr: str, name: str):                                                                                            
    # stock dataframe                                                                                                                  
    df = pd.read_hdf('git_ignore_folder/factor_implementation_source_data_debug/daily_pv.h5', key='data')                                                                                      
    df = df[:1000] # For testing, we only use the first 1000 rows of data. You can remove this line to use the full data.                                                                                                                                                                                                                                                                                            
                                                                                                                                       
    expr = parse_symbol(expr, df.columns)                                                                                              
    expr = parse_expression(expr)                                                                                                      

    # replace '$var' by 'df['var'] to extract var's actual values                                                                      
    for col in df.columns:                                                                                                             
        expr = expr.replace(col[1:], f"df[\'{col}\']")                                                                                                                                  
                                                                                                                                       
    df[name] = eval(expr)                                                                                                              
    result = df[name].astype(np.float64)                                                                                               

    if os.path.exists('result.h5'):                                                                                                    
        os.remove('result.h5')                                                                                                         
    result.to_hdf('result.h5', key='data')                                                                                             

if __name__ == '__main__':                                                                                                             
    # Input factor expression. Do NOT use the variable format like "df['$xxx']" in factor expressions. Instead, you should use "$xxx". 
    expr = "(TS_CORR(SIGN(return), SIGN(DELTA(volume, 1)), MAX(5, MIN(60, FLOOR(15 * 0.15 / (TS_STD(return, 20) + 1e-8))))))"
    # expr = "(TS_CORR(SIGN(return), SIGN(DELTA(volume, 1)), MAX(5, MIN(60, FLOOR(15 * 0.15 / (TS_STD(return, 20) + 1e-8) + 0.5)))) - TS_MEDIAN(TS_CORR(SIGN(return), SIGN(DELTA(volume, 1)), MAX(5, MIN(60, FLOOR(15 * 0.15 / (TS_STD(return, 20) + 1e-8) + 0.5)))), 60)) / (TS_MAD(TS_CORR(SIGN(return), SIGN(DELTA(volume, 1)), MAX(5, MIN(60, FLOOR(15 * 0.15 / (TS_STD(return, 20) + 1e-8) + 0.5)))), 60) + 1e-8)" # Your output factor expression will be filled in here                                                                                                     
    name = "Normalized_Volatility_Adjusted_Corr_8D" # Your output factor name will be filled in here                                   
    calculate_factor(expr, name) 