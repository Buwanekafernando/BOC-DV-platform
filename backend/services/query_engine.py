import pandas as pd
from typing import List, Dict, Any
from models.schemas import QueryRequest, AggregationType, FilterCondition
from utils.validators import apply_filters, validate_columns
from services.transformation_service import TransformationService
from services.modeling_service import ModelingService
import json

class QueryEngine:
    """Service for executing queries on CSV datasets"""
    
    @staticmethod
    def execute_query(
        file_path: str,
        query: QueryRequest,
        transformations: List[Dict[str, Any]] = None,
        measures: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a query on a dataset"""
        # Load data
        df = pd.read_csv(file_path)
        
        # Apply data transformations (Data Prep)
        if transformations:
            df = TransformationService.apply_transformations(df, transformations)
            
        # Apply measures (Data Modeling)
        if measures:
            df = ModelingService.apply_measures(df, measures)
            
        # Apply filters
        if query.filters:
            df = apply_filters(df, query.filters)
        
        # Apply grouping and aggregations
        if query.group_by and query.aggregations:
            df = QueryEngine._apply_aggregations(df, query.group_by, query.aggregations)
        elif query.aggregations:
            # Aggregations without grouping
            df = QueryEngine._apply_global_aggregations(df, query.aggregations)
        
        # Apply sorting
        if query.sort_by:
            sort_cols = [s.column for s in query.sort_by]
            ascending = [s.order == "asc" for s in query.sort_by]
            # Ensure columns exist
            valid_cols = [c for c in sort_cols if c in df.columns]
            if valid_cols:
                # Adjust ascending list to match valid_cols length if some were invalid (though we should probably validate earlier)
                # But for safety, let's just zip and filter
                sort_params = [(c, a) for c, a in zip(sort_cols, ascending) if c in df.columns]
                if sort_params:
                     df = df.sort_values(
                         by=[p[0] for p in sort_params],
                         ascending=[p[1] for p in sort_params]
                     )

        # Apply limit
        if query.limit:
            df = df.head(query.limit)
        
        # Convert to response format
        return {
            "data": df.to_dict(orient="records"),
            "total_rows": len(df),
            "columns": df.columns.tolist()
        }
    
    @staticmethod
    def _apply_aggregations(
        df: pd.DataFrame,
        group_by: List[str],
        aggregations: List[Any]
    ) -> pd.DataFrame:
        """Apply aggregations with grouping"""
        validate_columns(df, group_by)
        
        # Build aggregation dictionary
        agg_dict = {}
        for agg in aggregations:
            column = agg.column
            function = agg.function.value
            
            if column not in df.columns:
                continue
            
            if function == "sum":
                agg_dict[column] = "sum"
            elif function == "avg":
                agg_dict[column] = "mean"
            elif function == "count":
                agg_dict[column] = "count"
            elif function == "min":
                agg_dict[column] = "min"
            elif function == "max":
                agg_dict[column] = "max"
            elif function == "median":
                agg_dict[column] = "median"
            elif function == "std":
                agg_dict[column] = "std"
        
        # Group and aggregate
        grouped = df.groupby(group_by).agg(agg_dict).reset_index()
        
        # Rename columns to include aggregation function
        for agg in aggregations:
            column = agg.column
            function = agg.function.value
            if column in grouped.columns and column not in group_by:
                grouped.rename(columns={column: f"{column}_{function}"}, inplace=True)
        
        return grouped
    
    @staticmethod
    def _apply_global_aggregations(
        df: pd.DataFrame,
        aggregations: List[Any]
    ) -> pd.DataFrame:
        """Apply aggregations without grouping (global aggregations)"""
        results = {}
        
        for agg in aggregations:
            column = agg.column
            function = agg.function.value
            
            if column not in df.columns:
                continue
            
            if function == "sum":
                results[f"{column}_sum"] = [df[column].sum()]
            elif function == "avg":
                results[f"{column}_avg"] = [df[column].mean()]
            elif function == "count":
                results[f"{column}_count"] = [df[column].count()]
            elif function == "min":
                results[f"{column}_min"] = [df[column].min()]
            elif function == "max":
                results[f"{column}_max"] = [df[column].max()]
            elif function == "median":
                results[f"{column}_median"] = [df[column].median()]
            elif function == "std":
                results[f"{column}_std"] = [df[column].std()]
        
        return pd.DataFrame(results)
    
    @staticmethod
    def preview_data(
        file_path: str,
        limit: int = 100,
        transformations: List[Dict[str, Any]] = None,
        measures: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Preview first N rows of a dataset"""
        df = pd.read_csv(file_path) # Need full lead if transformations depend on all rows, but head(limit) for performance
        
        if transformations:
            df = TransformationService.apply_transformations(df, transformations)
        
        if measures:
            df = ModelingService.apply_measures(df, measures)
            
        df = df.head(limit)
        
        return {
            "data": df.to_dict(orient="records"),
            "total_rows": len(df),
            "columns": df.columns.tolist()
        }
