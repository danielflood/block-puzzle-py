# Tetris Puzzle

A puzzle game where players must fit Tetris pieces into a board with missing corners.

## Features

- 7 classic Tetris pieces
- Drag and drop interface
- Piece rotation
- Visual feedback for valid/invalid placements
- Win detection
- Reset functionality

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Clone this repository
3. Install dependencies:
```bash
pip install .
```

## Development Setup

Install development dependencies:

```bash
pip install -e .[dev]
```

## Controls

- Left Click: Select and drag pieces
- Right Click: Rotate selected piece
- Reset Button: Start over

## Project Structure

```
tetris_puzzle/
├── src/
│ ├── models/ # Game logic and data structures
│ ├── utils/ # Constants and utilities
│ └── ui/ # User interface and game loop
├── main.py # Entry point
└── pyproject.toml # Project configuration
```

## Contributing

1. Format code with Black: `black .`
2. Sort imports with isort: `isort .`
3. Run tests: `pytest`

## License

MIT
