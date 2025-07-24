"""
Path Configuration for Law Analysis System
Ensures proper import paths for all modules
"""
import os
import sys

def setup_paths():
    """Setup Python paths for the law analysis system"""
    # Get the base directory (where main.py is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add src and its subdirectories to Python path
    src_dir = os.path.join(base_dir, 'src')
    services_dir = os.path.join(src_dir, 'services')
    utils_dir = os.path.join(src_dir, 'utils')
    shared_dir = os.path.join(src_dir, 'shared')
    
    # Add all necessary paths
    paths_to_add = [src_dir, services_dir, utils_dir, shared_dir]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    return base_dir

# Auto-setup when imported
BASE_DIR = setup_paths()
