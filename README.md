# 🚀 AI-Powered Cosmos Video Generator & Auto Uploader

This project generates space-themed short stories using artificial intelligence, creates a video based on the story, and then automatically uploads the video to TikTok, YouTube, and Instagram. The project provides a completely automated video production and uploading process using Groq API, Selenium, InVideo, and VEED platforms.
<br><br><br>

## ✨ Features
🧠 Generating 33-word space, astrology, and cosmology themed stories with artificial intelligence
🎬 Automatic video creation with InVideo or VEED.io
💾 Downloading and renaming the video
📤 Automatic uploading to TikTok, YouTube, and Instagram
🕵️‍♂️ Simulating the entire process with Selenium
🖥️ Preserving sessions using Chrome user profile
<br><br><br>

## 📁 Project Structure
├── main.py                -> Main automation script
├── .env                   -> API keys and user profile settings
├── requirements.txt       -> Required Python libraries
<br><br><br>

## ⚙️ Installation
Create your Python environment:
```
python -m venv venv
source venv/bin/activate
```
<br><br><br>

## Install the required libraries:
```
pip install -r requirements.txt
```
<br><br><br>

## Create and configure the .env file as follows:
```
GROQ_API_KEY=your_groq_api_key_here
CHROME_PROFILE_PATH=C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data
CHROME_PROFILE_NAME=Default
```
Note: The Chrome user profile ensures you are logged into your social media accounts. How to find it?
<br><br><br>

## ▶️ Usage
- Run ```main.py```
- A short story is automatically generated
- Video is created with InVideo, or VEED if InVideo fails
- Video is downloaded and renamed
- The video is uploaded to TikTok, YouTube, and Instagram in sequence
<br><br><br>

## 🛠 Technologies Used
🧠 Groq API – Story generation with LLaMA3 model
🕸 Selenium WebDriver – Web automation
🌐 InVideo / VEED.io – Video production
🎥 TikTok Studio / YouTube Studio / Instagram Web – Automatic uploading
🧪 dotenv – Secret variable management
📦 webdriver-manager – Automatic ChromeDriver installation
<br><br><br>

## 🧪 Example Story
```Stars danced as galaxies spun stories of forgotten worlds. Mars whispered to Saturn, while a comet traced time's breath across the cosmos. Wonder was born in silence. Under 30 second.```
<br><br><br>

## ❗️Warnings
Video uploading on the web version of Instagram may sometimes encounter security restrictions. VPN or manual login may be required.
Pay attention to plan limits on video production sites.

## 🤝 Contributing
Pull requests and suggestions are welcome! 🎉
