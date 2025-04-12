# 🎵 NexxMusicBot - Discord Music Bot

NexxMusicBot is a powerful and easy-to-use Discord music bot that supports high-quality music playback across **multiple servers** with channel restrictions. Built for seamless audio performance and customizability.

---

## 🚀 Features

- 🎧 Play music from YouTube and other sources
- ✅ Supports **multiple servers**
- 🔒 Restrict music commands to specific channels per server
- 🔊 Customizable default volume
- ⚡ Fast and lightweight

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```arm
git clone https://github.com/nexxlokesh/MusicBot-for-Discord.git
```
### 2.  Install Dependencies
```arm
pip install discord.py yt_dlp json asyncio
```

### 3.  Configure the Bot
```arm
{
  "DISCORD_TOKEN": "your bot token",
  "ALLOWED_CHANNELS": {
    "13030658271291200": 1303071320855879,
    "1234567890345678": 9876543210985432
  },
  "DEFAULT_VOLUME": 0.25
}

```
#### 📌 Explanation:

- `DISCORD_TOKEN`: Your bot token from the Discord Developer Portal

- `ALLOWED_CHANNELS`: This object maps each guild (server) ID to a specific channel ID in that server where music commands will be accepted.

```arm
{
  "GUILD_ID_1": CHANNEL_ID_1,
  "GUILD_ID_2": CHANNEL_ID_2,
}
```
- `DEFAULT_VOLUME`: Set the default volume level (between 0.0 and 1.0). `0.25` means 25% volume.


### 4.  Run Bot
```arm
python main.py
```

---


## 🙋‍♂️ Owner Info

> This bot is developed by:

- 👤 **Name**: Lokesh Prajapat
- 💬 **Discord Server**: [CodeCanvas](https://discord.gg/trYJRwYQZ3)
- 🛠️ **GitHub**: [github.com/nexxlokesh](https://github.com/nexxlokesh)
- 🌐 **Portfolio**: [nexxlokesh.pro](https://nexxlokesh.pro)

For queries, support, or collaboration, feel free to reach out via Discord or GitHub.

---

**© 2025 NexxGuard — All Rights Reserved**
