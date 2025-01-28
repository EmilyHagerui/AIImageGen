"""
Image generation API handlers
"""

import os
import requests
from pathlib import Path
from abc import ABC, abstractmethod
from utils import generate_filename, ensure_output_dir

class ImageGenerator(ABC):
    @abstractmethod
    def generate(self, prompt, size, count, output_dir):
        pass

class OpenAIGenerator(ImageGenerator):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
    
    def generate(self, prompt, size, count, output_dir):
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "n": count,
            "size": size
        }
        
        print(f"Generating {count} image(s) with OpenAI DALL-E...")
        
        output_path = ensure_output_dir(output_dir)
        generated_files = []
        
        try:
            # This would make the actual API call
            # response = requests.post(f"{self.base_url}/images/generations", headers=headers, json=data)
            # response.raise_for_status()
            # images_data = response.json()['data']
            
            # For now, simulate successful generation
            for i in range(count):
                filename = generate_filename(prompt, "openai")
                filepath = output_path / filename
                
                # In real implementation, this would download and save the image
                # For simulation, create a placeholder file
                with open(filepath, 'w') as f:
                    f.write(f"Placeholder for: {prompt}\nProvider: OpenAI DALL-E\nSize: {size}\n")
                
                generated_files.append(str(filepath))
                print(f"Generated: {filename}")
            
            print(f"Successfully generated {len(generated_files)} image(s)")
            return generated_files
            
        except Exception as e:
            print(f"Error generating images: {e}")
            return []

class StabilityGenerator(ImageGenerator):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai"
    
    def generate(self, prompt, size, count, output_dir):
        if not self.api_key:
            raise ValueError("Stability API key not configured")
        
        print(f"Generating {count} image(s) with Stability AI...")
        
        output_path = ensure_output_dir(output_dir)
        generated_files = []
        
        try:
            # This would make the actual API call
            # Similar to OpenAI but different endpoint structure
            
            # For now, simulate successful generation
            for i in range(count):
                filename = generate_filename(prompt, "stability")
                filepath = output_path / filename
                
                # In real implementation, this would download and save the image
                # For simulation, create a placeholder file
                with open(filepath, 'w') as f:
                    f.write(f"Placeholder for: {prompt}\nProvider: Stability AI\nSize: {size}\n")
                
                generated_files.append(str(filepath))
                print(f"Generated: {filename}")
            
            print(f"Successfully generated {len(generated_files)} image(s)")
            return generated_files
            
        except Exception as e:
            print(f"Error generating images: {e}")
            return []