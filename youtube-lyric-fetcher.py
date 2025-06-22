import subprocess
import re
import time
from urllib.parse import urlparse, parse_qs
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

import lyricsgenius
from yt_dlp import YoutubeDL

GENIUS_ACCESS_TOKEN = "dXfWn_Tg18IVJMEjkJoAT9edQMFuBEBhwiihdXaK5O8gUsY9cDN_eLaSj-m3eZnu"
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

def get_clipboard_url():
    try:
        clipboard = subprocess.check_output(["wl-paste"]).decode().strip()
        parts = clipboard.split()
        for part in parts:
            if "youtube.com/watch?" in part:
                parsed = urlparse(part)
                video_id = parse_qs(parsed.query).get("v")
                if video_id:
                    return f"https://www.youtube.com/watch?v={video_id[0]}"
            elif "youtu.be/" in part:
                video_id = part.split("/")[-1].split("?")[0]
                return f"https://www.youtube.com/watch?v={video_id}"
        return None
    except Exception:
        return None

def get_youtube_title(url):
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', None)
    except Exception:
        return None

def clean_title(title):
    title = re.sub(r"[\(\[].*?[\)\]]", "", title).strip()
    keywords = ["official video", "official music video", "lyric video", "hd", "hq"]
    for kw in keywords:
        title = re.sub(kw, "", title, flags=re.IGNORECASE).strip()
    title = re.sub(r"\s{2,}", " ", title)
    return title

def clean_lyrics_start(lyrics_text):
    pattern = re.compile(r"lyrics", re.IGNORECASE)
    match = pattern.search(lyrics_text)
    if match:
        return lyrics_text[match.end():].lstrip()
    else:
        return lyrics_text

class LyricsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lyrics Viewer")
        self.geometry("600x700")
        self.configure(bg="#282c34")

        self.label = tk.Label(self, text="Waiting for YouTube URL...", font=("Segoe UI", 20, "bold"), fg="#61dafb", bg="#282c34")
        self.label.pack(pady=(10, 5))

        self.text = scrolledtext.ScrolledText(self, wrap="word", font=("Calibri", 14), fg="#dcdcdc", bg="#1e2228")
        self.text.pack(expand=True, fill="both", padx=10, pady=10)
        self.text.configure(state="disabled")

        self.last_url = None

        self.check_clipboard()

    def check_clipboard(self):
        url = get_clipboard_url()
        if url and url != self.last_url:
            self.last_url = url
            self.label.config(text="Fetching lyrics...")
            self.text.configure(state="normal")
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, "Loading lyrics, please wait...\n")
            self.text.configure(state="disabled")
            Thread(target=self.fetch_and_display_lyrics, args=(url,), daemon=True).start()
        self.after(2000, self.check_clipboard)

    def fetch_and_display_lyrics(self, url):
        title = get_youtube_title(url)
        if not title:
            self.update_lyrics_text("❌ Couldn’t fetch YouTube video title.")
            self.update_label("Lyrics Viewer")
            return

        title_clean = clean_title(title)

        if " - " in title_clean:
            artist, song = [s.strip() for s in title_clean.split(" - ", 1)]
        else:
            # Fallback to YouTube channel as artist
            try:
                ydl_opts = {'quiet': True, 'skip_download': True}
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    artist = info.get("uploader", "").strip()
            except Exception:
                artist = ""
            song = title_clean.strip()

        try:
            track = genius.search_song(song, artist)
            if track and track.lyrics:
                lyrics = clean_lyrics_start(track.lyrics)
                display_title = f"{song} — {artist}" if artist else song
            else:
                lyrics = "Lyrics not found."
                display_title = "Lyrics Viewer"
        except Exception as e:
            lyrics = f"Error fetching lyrics: {e}"
            display_title = "Lyrics Viewer"

        self.update_lyrics_text(lyrics)
        self.update_label(display_title)

    def update_lyrics_text(self, text):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, text)
        self.text.configure(state="disabled")

    def update_label(self, text):
        self.label.config(text=text)

if __name__ == "__main__":
    app = LyricsApp()
    app.mainloop()

