import streamlit as st
from pytube import YouTube, Playlist
import os

class YouTubeDownloaderGUI:
    def __init__(self):
        st.title("YouTube Downloader")

        self.url = st.text_input("Enter YouTube URL:")
        self.download_button = st.button("Download")

        self.path = None
        self.download_location_button = st.button("Choose Download Location")
        if self.download_location_button:
            self.choose_download_location()

        if self.download_button:
            self.download()

    def choose_download_location(self):
        self.path = st.text_input("Enter download location path:")
        st.write("Download location chosen:", self.path)

    def download(self):
        url = self.url

        if not url:
            st.error("Please enter a valid URL.")
            return

        if self.path is None or not os.path.exists(self.path):
            st.error("Please enter a valid download location.")
            return

        try:
            if 'playlist' in url:
                self.download_playlist(url)
            else:
                self.download_single_video(url)

            st.success("Download completed successfully.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    def download_playlist(self, url):
        playlist = Playlist(url)
        st.write(f'Downloading playlist: {playlist.title}')

        for video_url in playlist.video_urls:
            yt = YouTube(video_url)
            video_stream = yt.streams.get_highest_resolution()

            if not video_stream:
                st.warning(f"No suitable stream available for '{yt.title}'. Skipping.")
                continue

            video_stream.download(self.path)
            st.write(f"Downloaded '{yt.title}' successfully.")

    def download_single_video(self, url):
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()

        if not video_stream:
            st.warning(f"No suitable stream available for '{yt.title}'.")
            return

        video_stream.download(self.path)
        st.write(f"Downloaded '{yt.title}' successfully.")

if __name__ == "__main__":
    app = YouTubeDownloaderGUI()


