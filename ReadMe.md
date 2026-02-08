# Instagram Reels to YouTube Shorts Automation

This project is a Python-based automation script that downloads Instagram Reels from multiple public accounts and uploads them to YouTube as Shorts at fixed intervals.

The project was originally created as a **personal experiment** to understand long-running automation, API quotas, OAuth handling, and content pipelines. It was not initially intended for public release.

---

## ⚠️ Important Note

This repository contains **inconsistent naming and spelling mistakes** across files and directories.

These have been intentionally left unchanged to avoid breaking internal logic, as the project is 2–3 years old and was built purely for experimentation rather than production use.

Please keep this in mind while reviewing the code.

---

## ✨ Features

- Downloads reels from **multiple public Instagram accounts**
- Filters videos to **< 60 seconds** (YouTube Shorts compatible)
- Uploads videos as **YouTube Shorts**
- Upload interval: **1 video every 2 hours**
- Automatically deletes uploaded videos from local storage
- Rotates Instagram accounts when videos are exhausted
- Supports **multiple YouTube OAuth projects** to handle quota limits
- Automatic cooldown when quotas or upload limits are hit
- Caption reuse from Instagram (if available) or auto-generated titles
- Safe file deletion with file-lock detection

---

## 🧠 How It Works (High-Level)

1. Instagram usernames are stored in `Usernames.txt`
2. Reels are downloaded into:

```
Downloads/<instagram_username>/
```

3. Captions (if available) are extracted into:

```
Downloads/video_titles/<instagram_username>/
```

4. Videos are uploaded to YouTube as Shorts
5. After successful upload:
- Video file is deleted
- Caption file is deleted
6. When a user’s videos are exhausted:
- The user is removed from the active list
7. Upload continues every 2 hours
8. When YouTube API quota is exhausted:
- Another OAuth project is selected automatically
- Cooldown is applied if all projects are exhausted

---

## 🗂️ Project Structure

```
project/
│
├── Downloads/
│   ├── <instagram_username>/
│   │   └── <all videos downloaded from instagram_username instagram account>
│   ├── <video_titles>/
│   │   └── <instagram_username>/
│   │       └── <titles_text_files>/
│   └── Username_list.txt
│
├── secreat_keys/ # OAuth client JSON files (ignored)
│
├── secreat_keys_credentials/ # Stored OAuth credentials (ignored)
│
├── client_secreat_keys.txt
│
├── Connector.py
│
├── downloaded.py
│
├── main.py
│
├── upload.py
│
├── Usernames.txt
│
└── Z-how_To_Use.txt

```


---

## 🛠️ Requirements

- Python 3.x
- Windows OS (tested on Windows)
- Dummy Instagram account (recommended)

### Python Libraries
- instaloader
- moviepy
- google-api-python-client
- google-auth
- google-auth-oauthlib
- psutil

---

## 🚀 Setup

Detailed setup instructions are available in:
```
Z-how_To_Use.txt
```


This includes:
- Instagram login setup
- Google Cloud project creation
- YouTube Data API configuration
- OAuth client creation
- Required scopes
- First-time authorization flow

---

## ⚠️ Limitations

- Only **public Instagram accounts** are supported
- Windows-only paths are used
- User mode is incomplete (Developer mode is functional)
- Not production-hardened
- No guarantee of compliance with platform policies

---

## 📜 Disclaimer

This project does **not claim ownership of any content**.

You are responsible for:
- respecting Instagram and YouTube policies
- ensuring you have the right to upload any content
- using this project ethically and legally

---

## 🎯 Purpose of This Project

This project exists to demonstrate:
- automation design
- API quota handling
- OAuth lifecycle management
- retry & cooldown strategies
- real-world scripting challenges

It is shared for **educational and learning purposes only**.