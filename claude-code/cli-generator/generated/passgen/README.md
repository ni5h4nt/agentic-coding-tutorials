# passgen

A secure password generator with configurable length and character sets.

## Installation

```bash
pip install -e .
```

Or with uv:

```bash
uv pip install -e .
```

## Usage

### Generate Passwords

```bash
# Generate a default 16-character password
passgen generate

# Generate a 24-character password with symbols
passgen generate -l 24 -s

# Generate 5 passwords
passgen generate -n 5

# Exclude ambiguous characters
passgen generate --no-ambiguous

# Exclude specific characters
passgen generate -x "0O1l"
```

### Analyze Password Strength

```bash
# Basic strength check
passgen strength "MyP@ssw0rd123"

# Detailed analysis
passgen strength "MyP@ssw0rd123" --verbose

# Check against minimum length requirement
passgen strength "short" --min-length 12
```

### Use Presets

```bash
# List available presets
passgen presets --list

# Generate using a preset
passgen presets --use strong
passgen presets -u paranoid
```

### Available Presets

| Preset | Length | Description |
|--------|--------|-------------|
| pin | 4 | 4-digit PIN code |
| memorable | 12 | Easy to remember, moderate security |
| strong | 16 | Strong password for most uses |
| paranoid | 32 | Maximum security password |

## Global Options

- `--version` - Show version number
- `--verbose, -v` - Enable verbose output
- `--quiet, -q` - Suppress non-essential output
- `--no-color` - Disable colored output

## License

MIT
