import pandas as pd
import numpy as np
from typing import List, Dict, Any

class TransformationService:
    @staticmethod
    def apply_transformations(df: pd.DataFrame, transformations: List[Dict[str, Any]]) -> pd.DataFrame:
        """Apply a sequence of transformations to a DataFrame"""
        for step in transformations:
            step_type = step.get("type")
            params = step.get("params", {})
            
            try:
                if step_type == "rename":
                    df = df.rename(columns=params.get("columns", {}))
                
                elif step_type == "drop":
                    cols_to_drop = [c for c in params.get("columns", []) if c in df.columns]
                    df = df.drop(columns=cols_to_drop)
                
                elif step_type == "type_convert":
                    column = params.get("column")
                    new_type = params.get("dtype")
                    if column in df.columns:
                        if new_type == "datetime":
                            df[column] = pd.to_datetime(df[column], errors='coerce')
                        elif new_type == "numeric":
                            df[column] = pd.to_numeric(df[column], errors='coerce')
                        else:
                            df[column] = df[column].astype(new_type)
                
                elif step_type == "filter":
                    column = params.get("column")
                    operator = params.get("operator")
                    value = params.get("value")
                    
                    if column in df.columns:
                        if operator == "eq":
                            df = df[df[column] == value]
                        elif operator == "ne":
                            df = df[df[column] != value]
                        elif operator == "gt":
                            df = df[df[column] > value]
                        elif operator == "lt":
                            df = df[df[column] < value]
                        elif operator == "contains":
                            df = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]
                
                elif step_type == "sort":
                    column = params.get("column")
                    ascending = params.get("ascending", True)
                    if column in df.columns:
                        df = df.sort_values(by=column, ascending=ascending)
                
                elif step_type == "derived_column":
                    name = params.get("name")
                    formula = params.get("formula") # Simple: "col1 + col2" or "col1 * 0.1"
                    
                    # Basic evaluation for simple arithmetic
                    # WARNING: eval can be dangerous, but for this POC we use a restricted environment
                    # in a real app, we'd use a proper parser
                    try:
                        # Only allow arithmetic and column names
                        df[name] = df.eval(formula)
                    except Exception as e:
                        print(f"Error in derived column {name}: {e}")
                        
            except Exception as e:
                print(f"Error applying transformation {step_type}: {e}")
                
        return df
