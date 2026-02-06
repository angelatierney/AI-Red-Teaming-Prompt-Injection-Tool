#!/usr/bin/env python3
"""
Pre-flight Configuration Validator
Validates JSON/YAML syntax before Ansible runs to ensure configuration integrity.
"""

import json
import yaml
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple


class ConfigValidator:
    """Validates load balancer configuration files."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_file_exists(self) -> bool:
        """Check if configuration file exists."""
        if not self.config_path.exists():
            self.errors.append(f"Configuration file not found: {self.config_path}")
            return False
        return True
    
    def validate_json(self) -> Tuple[bool, Dict]:
        """Validate JSON syntax and structure."""
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
            
            # Validate required top-level keys
            required_keys = ['frontend', 'backend_pools', 'health_checks']
            for key in required_keys:
                if key not in data:
                    self.errors.append(f"Missing required key: {key}")
            
            # Validate frontend configuration
            if 'frontend' in data:
                if 'port' not in data['frontend']:
                    self.errors.append("Frontend missing 'port' configuration")
                if 'protocol' not in data['frontend']:
                    self.errors.append("Frontend missing 'protocol' configuration")
            
            # Validate backend pools
            if 'backend_pools' in data:
                if not isinstance(data['backend_pools'], list):
                    self.errors.append("'backend_pools' must be a list")
                else:
                    for i, pool in enumerate(data['backend_pools']):
                        if 'name' not in pool:
                            self.errors.append(f"Backend pool {i} missing 'name'")
                        if 'servers' not in pool:
                            self.errors.append(f"Backend pool {i} missing 'servers'")
                        elif not isinstance(pool['servers'], list):
                            self.errors.append(f"Backend pool {i} 'servers' must be a list")
            
            # Validate health checks
            if 'health_checks' in data:
                if 'interval' not in data['health_checks']:
                    self.warnings.append("Health checks missing 'interval', using default")
                if 'timeout' not in data['health_checks']:
                    self.warnings.append("Health checks missing 'timeout', using default")
            
            return len(self.errors) == 0, data
            
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON syntax error: {str(e)}")
            return False, {}
        except Exception as e:
            self.errors.append(f"Error reading JSON file: {str(e)}")
            return False, {}
    
    def validate_yaml(self) -> Tuple[bool, Dict]:
        """Validate YAML syntax and structure."""
        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
            
            if data is None:
                self.errors.append("YAML file is empty or invalid")
                return False, {}
            
            # Validate required top-level keys
            required_keys = ['frontend', 'backend_pools', 'health_checks']
            for key in required_keys:
                if key not in data:
                    self.errors.append(f"Missing required key: {key}")
            
            # Validate frontend configuration
            if 'frontend' in data:
                if 'port' not in data['frontend']:
                    self.errors.append("Frontend missing 'port' configuration")
                if 'protocol' not in data['frontend']:
                    self.errors.append("Frontend missing 'protocol' configuration")
            
            # Validate backend pools
            if 'backend_pools' in data:
                if not isinstance(data['backend_pools'], list):
                    self.errors.append("'backend_pools' must be a list")
                else:
                    for i, pool in enumerate(data['backend_pools']):
                        if 'name' not in pool:
                            self.errors.append(f"Backend pool {i} missing 'name'")
                        if 'servers' not in pool:
                            self.errors.append(f"Backend pool {i} missing 'servers'")
                        elif not isinstance(pool['servers'], list):
                            self.errors.append(f"Backend pool {i} 'servers' must be a list")
            
            # Validate health checks
            if 'health_checks' in data:
                if 'interval' not in data['health_checks']:
                    self.warnings.append("Health checks missing 'interval', using default")
                if 'timeout' not in data['health_checks']:
                    self.warnings.append("Health checks missing 'timeout', using default")
            
            return len(self.errors) == 0, data
            
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error: {str(e)}")
            return False, {}
        except Exception as e:
            self.errors.append(f"Error reading YAML file: {str(e)}")
            return False, {}
    
    def validate(self) -> bool:
        """Main validation method that detects file type and validates accordingly."""
        if not self.validate_file_exists():
            return False
        
        file_ext = self.config_path.suffix.lower()
        
        if file_ext == '.json':
            is_valid, _ = self.validate_json()
        elif file_ext in ['.yaml', '.yml']:
            is_valid, _ = self.validate_yaml()
        else:
            self.errors.append(f"Unsupported file type: {file_ext}. Use .json, .yaml, or .yml")
            return False
        
        return is_valid
    
    def print_report(self):
        """Print validation report."""
        print("=" * 60)
        print("Pre-flight Configuration Validation Report")
        print("=" * 60)
        print(f"File: {self.config_path}")
        print()
        
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  • {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ Configuration is valid!")
        elif not self.errors:
            print("✅ Configuration is valid (with warnings)")
        else:
            print("❌ Configuration validation failed!")
        
        print("=" * 60)


def main():
    """Main entry point for the validator script."""
    if len(sys.argv) < 2:
        print("Usage: python3 preflight_validator.py <config_file>")
        print("Example: python3 preflight_validator.py configs/load_balancer.yaml")
        sys.exit(1)
    
    config_file = sys.argv[1]
    validator = ConfigValidator(config_file)
    
    is_valid = validator.validate()
    validator.print_report()
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
