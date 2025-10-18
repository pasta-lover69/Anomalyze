"""
Anomalyze Preprocessing
"""

from __future__ import annotations
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from pathlib import Path
from typing import Union, Tuple

class InvalidNetworkLogError(Exception):
    """Custom exception for invalid network traffic logs"""
    pass


def validate_network_traffic_log(df: pd.DataFrame, expected_columns: int = 42) -> Tuple[bool, str]:
    """
    Validates if the uploaded file appears to be a network traffic log.
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Check 1: Column count (NSL-KDD can have 41, 42, or 43 columns)
    # 41 = without label, 42 = with label, 43 = with label and difficulty
    actual_columns = len(df.columns)
    valid_column_counts = [41, 42, 43]
    
    if actual_columns not in valid_column_counts:
        return False, (
            f"Invalid file format: Expected 41-43 columns for NSL-KDD network traffic logs, "
            f"but found {actual_columns} columns. "
            f"Please upload a valid NSL-KDD format network traffic log file."
        )
    
    # Check 2: Verify first few columns contain numeric data (common in network logs)
    # NSL-KDD starts with: duration, protocol_type, service, flag, src_bytes, dst_bytes...
    if len(df) > 0:
        # Check if first column (duration) is mostly numeric
        first_col = df.iloc[:, 0]
        try:
            numeric_vals = pd.to_numeric(first_col, errors='coerce')
            numeric_ratio = numeric_vals.notna().sum() / len(first_col)
            
            if numeric_ratio < 0.5:  # Less than 50% numeric
                return False, (
                    "Invalid file format: The file doesn't appear to contain network traffic data. "
                    "Expected numeric values in duration column. "
                    "Please upload a valid NSL-KDD format network traffic log file."
                )
        except Exception:
            return False, (
                "Invalid file format: Unable to parse network traffic data. "
                "Please ensure the file is in NSL-KDD format (CSV with no headers)."
            )
        
        # Check 3: Validate protocol_type column (should have typical network protocols)
        protocol_col = df.iloc[:, 1]
        unique_protocols = protocol_col.unique()
        
        # Common NSL-KDD protocols: tcp, udp, icmp
        valid_protocols = {'tcp', 'udp', 'icmp'}
        found_valid_protocol = any(
            str(proto).lower() in valid_protocols 
            for proto in unique_protocols[:10]  # Check first 10 unique values
        )
        
        if not found_valid_protocol and len(unique_protocols) < 20:
            # If we don't find common protocols and there's low variety, it's suspicious
            return False, (
                "Invalid file format: Protocol types don't match expected network traffic patterns. "
                "Expected protocols like 'tcp', 'udp', or 'icmp'. "
                "Please upload a valid NSL-KDD format network traffic log file."
            )
        
        # Check 4: Verify byte columns (4th and 5th columns) are numeric
        if len(df.columns) >= 6:
            src_bytes = pd.to_numeric(df.iloc[:, 4], errors='coerce')
            dst_bytes = pd.to_numeric(df.iloc[:, 5], errors='coerce')
            
            src_valid = src_bytes.notna().sum() / len(df) > 0.7
            dst_valid = dst_bytes.notna().sum() / len(df) > 0.7
            
            if not (src_valid and dst_valid):
                return False, (
                    "Invalid file format: Source and destination byte columns contain invalid data. "
                    "Please upload a valid NSL-KDD format network traffic log file."
                )
    
    # Check 5: Minimum rows check
    if len(df) < 1:
        return False, (
            "Invalid file: The file is empty or contains no data rows. "
            "Please upload a file with network traffic data."
        )
    
    return True, ""


def load_and_preprocess_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Loads the NSL-KDD dataset, assigns column names, and handles categorical features.
    Validates that the input is a proper network traffic log.
    """

    columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
        'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
        'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
        'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
        'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count',
        'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
        'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
        'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
        'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
        'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
        'dst_host_serror_rate', 'dst_host_srv_serror_rate',
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate',
        'label', 'difficulty'
    ]

    try:
        # Load the CSV file without assigning column names first (for validation)
        if hasattr(file_path, 'read'):
            df_raw = pd.read_csv(file_path, header=None)
        else:
            df_raw = pd.read_csv(file_path, header=None)
        
        # Validate that this is a network traffic log
        is_valid, error_message = validate_network_traffic_log(df_raw, expected_columns=len(columns))
        if not is_valid:
            raise InvalidNetworkLogError(error_message)
        
        # Assign column names after validation
        df = df_raw.copy()
        df.columns = columns[:len(df.columns)]  # Assign only as many names as we have columns
        
        if 'difficulty' in df.columns:
            df = df.drop('difficulty', axis = 1)

        # Handle missing values
        df = df.fillna(0)

        # Encode categorical variables
        categorical_columns = ['protocol_type', 'service', 'flag']

        for col in categorical_columns:
            if col in df.columns:
                try:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                except Exception as e:
                    raise InvalidNetworkLogError(
                        f"Failed to encode categorical column '{col}'. "
                        f"This may not be a valid network traffic log. Error: {str(e)}"
                    )

        # Focus on the most important features for anomaly tdetection
        important_features = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
            'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
            'same_srv_rate', 'diff_srv_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_serror_rate'
        ]

        # Keep only the important features
        features_to_keep = important_features.copy()
        if 'label' in df.columns:
            features_to_keep.append('label')

        # Filter to only the important features that exist in the DataFrame
        features_to_keep = [f for f in features_to_keep if f in df.columns]
        df =df[features_to_keep]

        # Ensure all remaining columns are numeric
        for col in df.columns:
            if col != 'label':
                # Force conversion to numeric, replacing any non-numeric values with 0
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                # Ensure the column is float type for consistency
                df[col] = df[col].astype(float)

                # Apply log transformation to highly skewed features
                if col in ['src_bytes', 'dst_bytes', 'count', 'srv_count']:
                    df[col] = np.log1p(df[col])

        return df
    
    except InvalidNetworkLogError:
        # Re-raise our custom validation errors
        raise
    except pd.errors.EmptyDataError:
        raise InvalidNetworkLogError(
            "The uploaded file is empty. Please upload a valid network traffic log file."
        )
    except pd.errors.ParserError as e:
        raise InvalidNetworkLogError(
            f"Failed to parse the file. Please ensure it's a valid CSV file in NSL-KDD format. Error: {str(e)}"
        )
    except Exception as e:
        # Check if it's a file reading error
        if "No such file" in str(e) or "cannot find" in str(e).lower():
            raise
        # Otherwise, treat as invalid format
        raise InvalidNetworkLogError(
            f"Unable to process the file as a network traffic log. "
            f"Please ensure you're uploading a valid NSL-KDD format file. Error: {str(e)}"
        )

def create_advanced_network_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create advance network-specific features optimized for K-means clustering"""
    df_enhanced = df.copy()
    
    # Ensure all numeric columns are actually numeric before operations
    for col in df_enhanced.columns:
        if col != 'label':
            df_enhanced[col] = pd.to_numeric(df_enhanced[col], errors='coerce').fillna(0).astype(float)

    # Traffic intensity ratios (check if columns exist first)
    if 'src_bytes' in df_enhanced.columns and 'dst_bytes' in df_enhanced.columns:
        df_enhanced['bytes_ratio'] = df_enhanced['src_bytes'] / (df_enhanced['dst_bytes'] + 1)
        df_enhanced['total_bytes'] = df_enhanced['src_bytes'] + df_enhanced['dst_bytes']

    # Connection pattern features
    if 'srv_count' in df_enhanced.columns and 'count' in df_enhanced.columns:
        df_enhanced['srv_rate'] = df_enhanced['srv_count'] / (df_enhanced['count'] + 1)
    
    if 'serror_rate' in df_enhanced.columns and 'srv_serror_rate' in df_enhanced.columns:
        df_enhanced['error_density'] = (df_enhanced['serror_rate'] + df_enhanced['srv_serror_rate']) / 2

    # Protocol behavior patterns
    if 'duration' in df_enhanced.columns and 'total_bytes' in df_enhanced.columns:
        df_enhanced['bytes_per_second'] = df_enhanced['total_bytes'] / (df_enhanced['duration'] + 0.001)
        df_enhanced['duration_category'] = pd.cut(df_enhanced['duration'],
                                                  bins = [0, 1,10, 100, float('inf')],
                                                  labels = [0, 1, 2, 3])
        
    # Host behavior clustering features
    if 'dst_host_diff_srv_rate' in df_enhanced.columns and 'dst_host_srv_count' in df_enhanced.columns:
        df_enhanced['host_diversity'] = (df_enhanced['dst_host_diff_srv_rate'] *
                                       df_enhanced['dst_host_srv_count'])
    
    # Attack pattern indicator
    if 'su_attempted' in df_enhanced.columns and 'root_shell' in df_enhanced.columns:
        df_enhanced['sus_flag_ratio'] = (df_enhanced['su_attempted'] + df_enhanced['root_shell']) / 2
    
    if 'land' in df_enhanced.columns:
        df_enhanced['land_flag'] = df_enhanced['land']

    # Network flow characteristics
    if 'same_srv_rate' in df_enhanced.columns:
        # Ensure numeric type before comparison
        df_enhanced['same_srv_rate'] = pd.to_numeric(df_enhanced['same_srv_rate'], errors='coerce').fillna(0).astype(float)
        df_enhanced['same_srv_rate_high'] = (df_enhanced['same_srv_rate'] > 0.8).astype(int)
    if 'diff_srv_rate' in df_enhanced.columns:
        # Ensure numeric type before comparison
        df_enhanced['diff_srv_rate'] = pd.to_numeric(df_enhanced['diff_srv_rate'], errors='coerce').fillna(0).astype(float)
        df_enhanced['diff_srv_rate_high'] = (df_enhanced['diff_srv_rate'] > 0.8).astype(int)

    return df_enhanced

def enhanced_preprocessing_for_kmeans(df: pd.DataFrame) -> pd.DataFrame:
    """Enhanced preprocessing specifically optimized for K-means clustering"""
    
    try:
        # Apply feature engineering only if we have the required columns
        df = create_advanced_network_features(df)

        # Handle categorical variables better for clustering
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col != 'label':
                # Use frequency encoding for high cardinality categoricals
                freq_encoding = df[col].value_counts().to_dict()
                df[f'{col}_freq'] = df[col].map(freq_encoding)
                df = df.drop(col, axis=1)
        
        return df
        
    except Exception as e:
        print(f"Error in enhanced preprocessing: {e}")
        # Return original dataframe if enhancement fails
        return df