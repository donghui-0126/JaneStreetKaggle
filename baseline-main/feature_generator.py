import gc
import numpy as np
from function_wrappers import versioned_function
import polars as pl 

import gc
import numpy as np
import polars as pl
from function_wrappers import versioned_function

def get_representative_features():
    """
    각 클러스터에서 가장 작은 feature 번호를 대표값으로 반환하고
    제거할 feature 목록을 반환하는 하드코딩된 함수
    """
    representative_features = [
        'feature_73', 'feature_12', 'feature_15', 'feature_05', 
        'feature_32', 'feature_42', 'feature_39', 'feature_24',
        'feature_50', 'feature_09', 'feature_22', 'responder_4',
        'feature_48'
    ]
    
    features_to_remove = [
        'feature_74', 'feature_75', 'feature_76', 'feature_77', 'feature_78',
        'feature_13', 'feature_14', 'feature_67', 'feature_68', 'feature_69',
        'feature_70', 'feature_71', 'feature_72', 'feature_16', 'feature_17',
        'feature_06', 'feature_07', 'feature_08', 'feature_18', 'feature_19',
        'feature_37', 'feature_38', 'feature_45', 'feature_46', 'feature_56',
        'feature_57', 'feature_58', 'feature_65', 'feature_66', 'feature_34',
        'feature_35', 'feature_61', 'feature_44', 'feature_41', 'feature_25',
        'feature_52', 'feature_53', 'feature_55', 'feature_59', 'feature_60',
        'feature_11', 'feature_23', 'responder_7', 'feature_49'
    ]
    
    return representative_features, features_to_remove

def create_rolling_features(df: pl.DataFrame, rolling_window_size: list) -> pl.DataFrame:
    """
    Polars를 사용하여 rolling feature와 해당 변화율을 생성하는 함수
    
    Parameters:
    -----------
    df : pl.DataFrame
        입력 데이터프레임
    rolling_window_size : list
        rolling window 크기 리스트
    
    Returns:
    --------
    pl.DataFrame
        rolling feature와 변화율이 추가된 데이터프레임
    """
    # Feature 컬럼 필터링
    feature_cols = [col for col in df.columns 
                   if ('feature' in col or 'id' in col) 
                   and col not in ['date_id', 'time_id', 'symbol_id']
                   and not 'responder' in col]
    
    # Symbol별로 그룹화하여 rolling feature 계산
    result = df.clone()
    
    for window in rolling_window_size:
        # Rolling mean 계산
        rolling_exprs = [
            pl.col(feat).forward_fill().backward_fill()
            .rolling_mean(window_size=window)
            .forward_fill().backward_fill()
            .alias(f'{feat}_rolling_{window}')
            for feat in feature_cols
        ]
        result = result.with_columns(rolling_exprs)
        
        # Rolling mean의 변화율 계산
        pct_change_exprs = [
            pl.col(f'{feat}_rolling_{window}')
            .pct_change()
            .forward_fill()
            .backward_fill()
            .alias(f'{feat}_rolling_{window}_pct_change')
            for feat in feature_cols
        ]
        result = result.with_columns(pct_change_exprs)
    
    return result

@versioned_function("1.3.0", "Added percentage change features for rolling means")
def default_feature_generator(df: pl.DataFrame) -> pl.DataFrame:
    """Feature generation with time-based features, rolling features, and their percentage changes"""
    # Add time-based features using polars expressions
    result = df.with_columns([
        (2 * np.pi * pl.col('time_id') / 967).sin().alias('feature_sin_time_id'),
        (2 * np.pi * pl.col('time_id') / 967).cos().alias('feature_cos_time_id'),
        (2 * np.pi * pl.col('time_id') / 483).sin().alias('feature_sin_time_id_halfday'),
        (2 * np.pi * pl.col('time_id') / 483).cos().alias('feature_cos_time_id_halfday')
    ])

    # Fill NA values and rename columns
    result = (result
        .fill_null(-1)
        .rename({
            'symbol_id': 'feature_symbol_id',
            'weight': 'feature_weight'
        }))
    
    # Get representative features and features to remove
    rep_features, remove_features = get_representative_features()
    
    # Add rolling features and their percentage changes
    result = create_rolling_features(result, rolling_window_size=[2, 10, 30, 50, 200, 500, 1000])
    
    # Select columns for final output
    feature_cols = ['feature_symbol_id', 'feature_sin_time_id', 'feature_cos_time_id',
                   'feature_sin_time_id_halfday', 'feature_cos_time_id_halfday', 'feature_weight']
    
    # Add representative features and their variants
    for feat in rep_features:
        if feat in result.columns:
            feature_cols.append(feat)
            # Add rolling features and their pct changes if they exist
            rolling_cols = [col for col in result.columns 
                          if col.startswith(f'{feat}_rolling_')]
            feature_cols.extend(rolling_cols)
    
    # Add target column if it exists
    if 'responder_6' in result.columns:
        feature_cols.insert(0, 'responder_6')
        
    return result.select(feature_cols)