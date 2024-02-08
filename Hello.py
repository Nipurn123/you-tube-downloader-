import streamlit as st
from pytube import YouTube, Playlist
from threading import Thread

class YouTubeDownloaderGUI:
    def __init__(self):
        st.title("YouTube Downloader")

        self.url = st.text_input("Enter YouTube URL:", key="url_input")
        self.path = st.text_input("Select Download Path:", key="path_input")

        self.browse_button = st.button("Browse", key="browse_button")
        self.download_button = st.button("Download", key="download_button")

        if self.browse_button:
            self.browse_path()

        if self.download_button:
            self.download()

    def browse_path(self):
        download_path = st.file_uploader("Browse", key="file_uploader")
        self.path = download_path

    def download(self):
        url = self.url
        download_path = self.path

        if not url or not download_path:
            st.error("Please enter a valid URL and download path.")
            return

        download_thread = Thread(target=self.download_media, args=(url, download_path))
        download_thread.start()

    def download_media(self, url, path):
        try:
            if 'playlist' in url:
                self.download_playlist(url, path)
            else:
                self.download_single_video(url, path)

            st.success("Download completed successfully.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    def download_playlist(self, url, path):
        playlist = Playlist(url)
        st.write(f'Downloading playlist: {playlist.title}')

        for video_url in playlist.video_urls:
            yt = YouTube(video_url)
            video_stream = yt.streams.get_highest_resolution()

            if not video_stream:
                st.warning(f"No suitable stream available for '{yt.title}'. Skipping.")
                continue

            video_stream.download(path)
            st.write(f"Downloaded '{yt.title}' successfully.")

    def download_single_video(self, url, path):
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()

        if not video_stream:
            st.warning(f"No suitable stream available for '{yt.title}'.")
            return

        video_stream.download(path)
        st.write(f"Downloaded '{yt.title}' successfully.")

if __name__ == "__main__":
    app = YouTubeDownloaderGUI()
