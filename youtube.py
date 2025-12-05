import json, requests, yt_dlp
class yt:
    def __init__(self, url, debug):
        self.url = url
        self.debug = debug
        info = self.get_video_info(self.url)
        self.title = info["title"]
        self.description = info["description"]
        self.transcript = info["transcript"]

    def transcript(self, raw_text: str) -> str:
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            return raw_text

        if isinstance(data, dict) and "events" in data:
            parts = []
            for event in data.get("events", []):
                for seg in event.get("segs", []):
                    text = seg.get("utf8", "")
                    if text == "\n":
                        parts.append("\n")
                    else:
                        parts.append(text)
            transcript = "".join(parts)
            transcript = transcript.replace("\r", "")
            while "\n\n\n" in transcript:
                transcript = transcript.replace("\n\n\n", "\n\n")
            return transcript.strip()
        return raw_text

    def get_caption_track(self, track: dict) -> str | None:
        try:
            url = track["url"]
            resp = requests.get(url)
            resp.raise_for_status()
            raw_text = resp.text
            return self.transcript(raw_text)
        except Exception as e:
            if self.debug:
                print(f"Error downloading subtitles: {e}")
            return None
        
    def get_video_info(self, url: str):
        try:
            ydl_opts = {
                "skip_download": True,
                "quiet": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en", "en-US", "es", "es-419", "es-LA", "es-ES"],
                "simulate": True,
                "dump_single_json": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                data = ydl.extract_info(url, download=False)

            title = data.get("title", "Error: No Title")

            description = data.get("description", "")

            subtitles = data.get("subtitles") or {}
            automatic_captions = data.get("automatic_captions") or {}

            transcript_text = None

            transcript_priority = ["en", "en-US", "es", "es-419", "es-LA", "es-ES"]

            for lang in transcript_priority:
                if lang in subtitles:
                    transcript_text = self.get_caption_track(subtitles[lang][0])
                    if transcript_text:
                        break

            if not transcript_text:
                for lang in transcript_priority:
                    if lang in automatic_captions:
                        transcript_text = self.get_caption_track(automatic_captions[lang][0])
                        if transcript_text:
                            break

            if not transcript_text:
                transcript_text = " * No transcript available."

            return {
                "title": title,
                "description": description,
                "transcript": transcript_text,
            }
        except yt_dlp.utils.DownloadError as e:
            print(f"URL not found: {e}")
            return {
                "title": "Error: No Title",
                "description": "Error: No Description",
                "transcript": "Error: No Transcript",
            }
        except Exception as e:
            print(f"Error: {e}")
            return {
                "title": "Error",
                "description": "An unexpected error occurred.",
                "transcript": "",
            }
        