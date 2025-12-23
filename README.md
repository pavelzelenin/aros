# aros

Agent Runtime OS

This repository contains a lightweight checker that verifies a few basics of the
runtime environment (Python version, documentation presence, and ability to
write temporary files). Run it locally to surface potential issues early.

## Usage

Run the checker from the project root:

```
python -m aros
```

Use `--project-root` to target a different directory if needed.

## Development

Install development dependencies and run the tests:

```
pip install -r requirements-dev.txt
pytest
```
