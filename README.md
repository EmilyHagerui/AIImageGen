# AIImageGen

A command-line tool for generating images using various AI APIs.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Before using the tool, set your API keys:

```bash
# For OpenAI DALL-E
python main.py --set-api-key openai YOUR_OPENAI_API_KEY

# For Stability AI
python main.py --set-api-key stability YOUR_STABILITY_API_KEY
```

Check your configuration:

```bash
python main.py --config
```

## Usage

Generate images with a text prompt:

```bash
python main.py "a beautiful sunset over mountains"
```

Options:

- `--provider`: Choose AI provider (openai, stability)
- `--output`: Output directory for images
- `--size`: Image size (1024x1024, 512x512, etc.)
- `--count`: Number of images to generate

Examples:

```bash
# Generate 3 images using Stability AI
python main.py "cyberpunk city" --provider stability --count 3

# Custom output directory and size
python main.py "abstract art" --output ./my_images --size 512x512
```

## Batch Processing

Generate multiple images from a configuration file:

```bash
# Create a sample batch file
python main.py --create-batch my_batch.json

# Process the batch file
python main.py --batch my_batch.json --output ./batch_results
```

Sample batch file format:

```json
{
  "jobs": [
    {
      "prompt": "a futuristic cityscape at sunset",
      "provider": "openai",
      "size": "1024x1024",
      "count": 1,
      "delay": 3
    },
    {
      "prompt": "abstract geometric patterns",
      "provider": "stability",
      "size": "512x512",
      "count": 2,
      "delay": 2
    }
  ]
}
```

## Features

- Multiple AI provider support (OpenAI DALL-E, Stability AI)
- Configurable output directory and image parameters
- Local configuration management
- Batch processing for multiple prompts
- Rate limiting and error handling
- Command-line interface with helpful options