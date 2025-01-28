#!/usr/bin/env python3
"""
AIImageGen - AI Image Generation Tool
A command-line tool for generating images using various AI APIs
"""

import argparse
import sys
from config import Config
from generators import OpenAIGenerator, StabilityGenerator

def create_parser():
    parser = argparse.ArgumentParser(description="AI Image Generation Tool")
    parser.add_argument('prompt', nargs='?', help='Text prompt for image generation')
    parser.add_argument('--output', '-o', 
                       help='Output directory for generated images')
    parser.add_argument('--size',
                       help='Image size (e.g., 1024x1024, 512x512)')
    parser.add_argument('--count', '-c', type=int,
                       help='Number of images to generate')
    parser.add_argument('--config', action='store_true',
                       help='Show configuration settings')
    parser.add_argument('--set-api-key', nargs=2, metavar=('PROVIDER', 'KEY'),
                       help='Set API key for provider (openai, stability)')
    parser.add_argument('--provider', choices=['openai', 'stability'], default='openai',
                       help='AI provider to use (default: openai)')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    config = Config()
    
    if args.set_api_key:
        provider, key = args.set_api_key
        if provider in ['openai', 'stability']:
            config.set(f'api_keys.{provider}', key)
            print(f"API key for {provider} has been saved.")
        else:
            print(f"Unknown provider: {provider}")
        return
    
    if args.config:
        print("Current configuration:")
        print(f"OpenAI API Key: {'Set' if config.get('api_keys.openai') else 'Not set'}")
        print(f"Stability API Key: {'Set' if config.get('api_keys.stability') else 'Not set'}")
        print(f"Default size: {config.get('defaults.size')}")
        print(f"Default output: {config.get('defaults.output_dir')}")
        print(f"Default count: {config.get('defaults.count')}")
        return
    
    if not args.prompt:
        parser.print_help()
        return
    
    output_dir = args.output or config.get('defaults.output_dir')
    size = args.size or config.get('defaults.size')
    count = args.count or config.get('defaults.count')
    
    print("AIImageGen - AI Image Generation Tool")
    print(f"Prompt: {args.prompt}")
    print(f"Output: {output_dir}")
    print(f"Size: {size}")
    print(f"Count: {count}")
    print(f"Provider: {args.provider}")
    
    try:
        if args.provider == 'openai':
            api_key = config.get('api_keys.openai')
            generator = OpenAIGenerator(api_key)
        elif args.provider == 'stability':
            api_key = config.get('api_keys.stability')
            generator = StabilityGenerator(api_key)
        
        generated_files = generator.generate(args.prompt, size, count, output_dir)
        if generated_files:
            print("Generation completed successfully!")
            print(f"Files saved to: {output_dir}")
        else:
            print("Generation failed or no files created")
        
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Please set your API key with: python main.py --set-api-key {args.provider} YOUR_API_KEY")

if __name__ == "__main__":
    main()