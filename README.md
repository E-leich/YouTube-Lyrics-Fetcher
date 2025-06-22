# 🎵 YouTube Lyrics Fetcher

A simple GUI application that detects a YouTube song URL from your clipboard, fetches its title, artist, and lyrics using the Genius API, and displays the lyrics in a clean interface.

## ✨ Features

- Detects YouTube song URLs from clipboard (Wayland-compatible using `wl-paste`)
- Cleans and parses video titles to extract artist and song name
- Fetches lyrics from Genius using `lyricsgenius`
- Displays lyrics in a themed Tkinter GUI
- Automatically updates when a new valid YouTube URL is copied
- Formats lyrics to remove extra metadata (like "Contributors", etc.)

## 📦 Dependencies

Install all dependencies using pip:

```bash
pip install lyricsgenius yt-dlp
```

Additionally, ensure the following are installed on your system:

- `tk` / `tkinter` (often included in Python but may need `tk` package via package manager)
- `wl-clipboard` (provides `wl-paste` for Wayland clipboard access)

Example for Arch Linux:
```bash
sudo pacman -S tk wl-clipboard
```

## 🔑 Setup Genius API

1. Create an account on [https://genius.com/](https://genius.com/)
2. Go to [https://genius.com/api-clients](https://genius.com/api-clients) and create an API client
3. Copy your Genius access token
4. Replace `"your_genius_api_token_here"` in the script with your token

## 🚀 Running the App

1. Run the script:

```bash
python youtube-lyric-fetcher.py
```

2. Copy a YouTube song URL to clipboard — lyrics will appear!

## 📝 Notes

- Lyrics may not always be found, especially for obscure remixes or mislabeled videos.
- If the artist name is missing from the title, the script attempts to use the channel name instead.

## 📷 Screenshot

*(You can add a screenshot or GIF here)*

## 🛠️ License

MIT License. Contributions welcome!
