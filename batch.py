"""
Batch processing functionality for AIImageGen
"""

import json
import time
from pathlib import Path
from generators import OpenAIGenerator, StabilityGenerator

class BatchProcessor:
    def __init__(self, config):
        self.config = config
        self.generators = {
            'openai': OpenAIGenerator(config.get('api_keys.openai')),
            'stability': StabilityGenerator(config.get('api_keys.stability'))
        }
    
    def process_batch_file(self, batch_file, output_dir):
        """Process a batch file containing multiple prompts"""
        batch_path = Path(batch_file)
        
        if not batch_path.exists():
            print(f"Batch file not found: {batch_file}")
            return False
        
        try:
            with open(batch_path, 'r') as f:
                batch_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in batch file: {e}")
            return False
        
        if not isinstance(batch_data, dict) or 'jobs' not in batch_data:
            print("Batch file must contain a 'jobs' array")
            return False
        
        jobs = batch_data['jobs']
        total_jobs = len(jobs)
        print(f"Processing {total_jobs} batch jobs...")
        
        successful_jobs = 0
        failed_jobs = 0
        
        for i, job in enumerate(jobs, 1):
            print(f"\n--- Job {i}/{total_jobs} ---")
            
            if not self._validate_job(job):
                print(f"Skipping invalid job {i}")
                failed_jobs += 1
                continue
            
            try:
                result = self._process_single_job(job, output_dir)
                if result:
                    successful_jobs += 1
                    print(f"Job {i} completed successfully")
                else:
                    failed_jobs += 1
                    print(f"Job {i} failed")
                
                # Add delay between jobs to avoid rate limiting
                if i < total_jobs:
                    delay = job.get('delay', 2)
                    print(f"Waiting {delay} seconds before next job...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"Error processing job {i}: {e}")
                failed_jobs += 1
        
        print(f"\n=== Batch Processing Complete ===")
        print(f"Successful: {successful_jobs}")
        print(f"Failed: {failed_jobs}")
        print(f"Total: {total_jobs}")
        
        return successful_jobs > 0
    
    def _validate_job(self, job):
        """Validate a single job configuration"""
        required_fields = ['prompt']
        for field in required_fields:
            if field not in job:
                print(f"Missing required field: {field}")
                return False
        
        provider = job.get('provider', 'openai')
        if provider not in self.generators:
            print(f"Unknown provider: {provider}")
            return False
        
        return True
    
    def _process_single_job(self, job, output_dir):
        """Process a single job from the batch"""
        prompt = job['prompt']
        provider = job.get('provider', 'openai')
        size = job.get('size', '1024x1024')
        count = job.get('count', 1)
        
        # Create job-specific output directory
        job_output = Path(output_dir) / f"job_{hash(prompt) % 10000:04d}"
        
        print(f"Prompt: {prompt}")
        print(f"Provider: {provider}")
        print(f"Size: {size}, Count: {count}")
        print(f"Output: {job_output}")
        
        generator = self.generators[provider]
        generated_files = generator.generate(prompt, size, count, str(job_output))
        
        return len(generated_files) > 0
    
    def create_sample_batch_file(self, filename):
        """Create a sample batch configuration file"""
        sample_data = {
            "jobs": [
                {
                    "prompt": "a futuristic cityscape at sunset",
                    "provider": "openai",
                    "size": "1024x1024",
                    "count": 1,
                    "delay": 3
                },
                {
                    "prompt": "abstract geometric patterns in blue and gold",
                    "provider": "stability",
                    "size": "512x512",
                    "count": 2,
                    "delay": 2
                },
                {
                    "prompt": "a serene mountain lake with reflection",
                    "provider": "openai",
                    "size": "1024x1024",
                    "count": 1,
                    "delay": 3
                }
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"Sample batch file created: {filename}")
        print("Edit this file with your own prompts and run with:")
        print(f"python main.py --batch {filename}")