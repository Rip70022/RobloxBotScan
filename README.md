# 🤖 Roblox Server Bot Scanner (RSBS)

An advanced system for scanning Roblox servers and detecting potential bots in real time by analyzing player behavior—such as movement, chat, join time, and username patterns. Features a sleek graphical interface for ease of use.

## 📌 Features

- Interactive GUI with server status visualization.
- Direct connection to a Roblox server via Game ID.
- Automated detection based on:
  - Join time consistency
  - Unusual movement patterns
  - Suspicious chat activity
  - Bot-like usernames
- Live bot percentage estimation with confidence level
- Optional continuous scanning mode

## ⚙️ Requirements

- Python 3.8+
- Packages:
  - `numpy`
  - Custom modules: `roblox.players`, `roblox.gui`, `roblox.analytics`, `roblox.game_service` (these must be implemented in your environment or mocked appropriately)

## 🚀 Installation

1. Clone this repository:
   ```
   git clone https://github.com/Rip70022/RobloxBotScan.git 
   cd RobloxBotScan
   ```
2. Install required dependencies:
```
pip install numpy
```
`Ensure the custom roblox modules are available in your environment.`

## 🕹️ Usage:
**Run the script:**
```
python RSBS.py
```
**Enter a valid Roblox Game `ID` in the `GUI`.**

**Click `"Connect"`.**

**Press `"Start Continuous Scanning"` to begin live `analysis`.**

## 🛡️ Scanner Status Output:
```
Estimated bot percentage in the current server

Detection confidence level
```
## Detailed breakdown by behavior patterns:

`Join time`

`Movement`

`Chat`

`Username`

## 📄 License:
`This project is licensed under the MIT License. See the LICENSE file for details.`

## 👨‍💻 Author:
`Rip70022`
Discord: `x4x0`
TikTok: `0sploit`
Roblox: `NAXROC`
