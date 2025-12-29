# yt-download

Download YouTube videos with quality selection and format options.

## Installation

```bash
pip install -e .
```

## Usage

### Download a single video

```bash
yt-download download "https://youtube.com/watch?v=abc123"
yt-download download "https://youtube.com/watch?v=abc123" -q 720p -o ~/Videos
yt-download download "https://youtube.com/watch?v=abc123" --format mp3
yt-download download "https://youtube.com/watch?v=abc123" --resume --retry 5
```

### Get video information

```bash
yt-download info "https://youtube.com/watch?v=abc123"
yt-download info "https://youtube.com/watch?v=abc123" --json
```

### Batch download

```bash
yt-download batch "https://youtube.com/playlist?list=PL123"
yt-download batch urls.txt -o ~/Videos -c 5
yt-download batch urls.txt --resume --retry 5
```

## Commands

| Command | Description |
|---------|-------------|
| `download` | Download a single video |
| `info` | Display video information |
| `batch` | Download multiple videos |

## Global Options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Show detailed progress |
| `-q, --quiet` | Suppress output except errors |
| `--version` | Show version |
| `--help` | Show help |

## License

MIT
