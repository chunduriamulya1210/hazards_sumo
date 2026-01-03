"""
CSV WRITER - Mumbai Traffic Simulation
Writes simulation data and hazard events to CSV files
"""

import csv
import os
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

class CSVWriter:
    """
    Handles writing simulation data to CSV files
    """
    
    def __init__(self, config: Dict):
        """
        Initialize CSV writer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.output_dir = "output_data"
        self.data_file = "simulation_data.csv"
        self.hazard_file = "hazard_events.csv"
        
        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self.data_path = os.path.join(self.output_dir, self.data_file)
        self.hazard_path = os.path.join(self.output_dir, self.hazard_file)
        
        self.append_mode = config["simulation"].get("csv_append_mode", True)
        self.write_header_data = True
        self.write_header_hazard = True
        
    def initialize_files(self) -> bool:
        """
        Initialize CSV files (write headers)
        
        Returns:
            bool: True if successful
        """
        try:
            mode = 'a' if self.append_mode else 'w'
            
            # Check if files exist to decide on header
            if self.append_mode and os.path.exists(self.data_path):
                self.write_header_data = False
            if self.append_mode and os.path.exists(self.hazard_path):
                self.write_header_hazard = False
            
            # Initialize data file
            if not self.append_mode or self.write_header_data:
                with open(self.data_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "timestamp", "step", "vehicle_id", "type", 
                        "x", "y", "speed", "acceleration", "angle", "lane_id", "hazard_active"
                    ])
            
            # Initialize hazard file
            if not self.append_mode or self.write_header_hazard:
                with open(self.hazard_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "timestamp", "hazard_name", "metadata"
                    ])
                    
            return True
        except Exception as e:
            print(f"Failed to initialize CSV files: {e}")
            return False

    def write_data(self, sensor_data: List[Dict], simulation_state: Dict):
        """
        Write vehicle sensor data to CSV
        """
        if not sensor_data:
            return
            
        try:
            timestamp = simulation_state.get("simulation_time", 0)
            step = simulation_state.get("step", 0)
            
            with open(self.data_path, 'a', newline='') as f:
                writer = csv.writer(f)
                for data in sensor_data:
                    writer.writerow([
                        timestamp,
                        step,
                        data.get("id", ""),
                        data.get("type", ""),
                        f"{data.get('x', 0):.2f}",
                        f"{data.get('y', 0):.2f}",
                        f"{data.get('speed', 0):.2f}",
                        f"{data.get('acceleration', 0):.2f}",
                        f"{data.get('angle', 0):.2f}",
                        data.get("lane", ""),
                        data.get("hazard_active", False)
                    ])
        except Exception as e:
            print(f"Error writing data: {e}")

    def write_hazard_event(self, hazard_event: Dict):
        """
        Write hazard event to CSV
        """
        try:
            with open(self.hazard_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    hazard_event.get("timestamp", 0),
                    hazard_event.get("hazard_name", "unknown"),
                    str(hazard_event.get("metadata", {}))
                ])
        except Exception as e:
            print(f"Error writing hazard event: {e}")
