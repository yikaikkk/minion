#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bluetooth scanning tool using bleak library
"""

import asyncio
from typing import List, Dict, Any
from .async_base_tool import AsyncBaseTool


class BluetoothScanTool(AsyncBaseTool):
    """
    A tool to scan for Bluetooth devices using the bleak library.
    
    This tool uses the bleak library to scan for nearby Bluetooth devices
    and returns a list of discovered devices with their details.
    """
    
    name: str = "bluetooth_scan"
    description: str = "Scan for nearby Bluetooth devices and return their details"
    inputs: Dict[str, Dict[str, Any]] = {
        "timeout": {
            "type": "float",
            "description": "Scan timeout in seconds (default: 5.0)",
            "default": 5.0
        }
    }
    output_type: str = "list"
    readonly: bool = True
    
    async def forward(self, timeout: float = 5.0) -> List[Dict[str, Any]]:
        """
        Scan for nearby Bluetooth devices.
        
        Args:
            timeout: Scan timeout in seconds
            
        Returns:
            List of dictionaries containing device information
        """
        try:
            from bleak import BleakScanner
            
            # Scan for devices
            devices = await BleakScanner.discover(timeout=timeout)
            
            # Format results
            result = []
            for device in devices:
                device_info = {
                    "name": device.name or "Unknown",
                    "address": device.address,
                    "rssi": getattr(device, 'rssi', 'N/A')
                }
                result.append(device_info)
            
            return result
        except ImportError:
            return [{"error": "bleak library is not installed. Please install it with 'pip install bleak'"}]
        except Exception as e:
            return [{"error": f"Error scanning for Bluetooth devices: {str(e)}"}]
    
    def format_for_observation(self, output: List[Dict[str, Any]]) -> str:
        """
        Format the tool output for LLM observation.
        
        Args:
            output: The raw output from forward() method
            
        Returns:
            Formatted string suitable for LLM observation
        """
        if not output:
            return "No Bluetooth devices found."
        
        if "error" in output[0]:
            return f"Error: {output[0]['error']}"
        
        formatted = "Found Bluetooth devices:\n"
        for i, device in enumerate(output, 1):
            formatted += f"{i}. Name: {device['name']}, Address: {device['address']}, RSSI: {device['rssi']} dBm\n"
        
        return formatted


class BluetoothToolset:
    """
    Toolset for Bluetooth-related tools.
    """
    
    def __init__(self):
        self.tools = [BluetoothScanTool()]
    
    async def setup(self):
        """
        Setup the toolset.
        """
        pass
    
    def get_tools(self):
        """
        Get the list of tools in this toolset.
        
        Returns:
            List of tools
        """
        return self.tools
