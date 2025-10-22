# Grace Hopper Celebration (GHC) 2025: Virtual Career Fair 1:1 Interview Slot Check Automation

**Note:** Generative AI was extensively used to create this script.

## Dependencies
- Google Chrome
- Chrome WebDriver
- Pushbullet
- Python 3.x
- python-dotenv
- Selenium

## Setup and Configuration
*(Tested on Windows 11 and Google Chrome)*
1. **Pushbullet Setup** 
	- Create an account on [Pushbullet](https://www.pushbullet.com/).  
	- In the Pushbullet web app, navigate to **Settings** and create an **Access Token**.  
	- Create a `.env` file in the project root and add your Pushbullet access token(s):
	```env
	PUSHBULLET_ACCESS_TOKENS=<access-token-1>
	```
	For multiple tokens, separate them with semicolons:
	```env
	PUSHBULLET_ACCESS_TOKENS=<access-token-1>;<access-token-2>
	```
2. To receive real-time alerts, make sure notifications are enabled for Pushbullet on your Desktop and/or Android app.

### Optional Configurations:
1. Edit config.py to modify settings such as:
	- Script sleep duration (default: one hour, to avoid server overload)
	- Notification preferences (opt out of certain companies or only alert for a whitelist. default: alert enabled for all companies)
2. If you plan to run the script overnight, ensure your PC’s screen timeout and sleep settings will not interrupt execution.

## Launching the Script
1. Open PowerShell
2. Run the script:
	```powershell
	python .\main.py
	```
3. A Chrome window will open. Enter your GHC credentials.
4. Return to PowerShell and press any key to start the automation.

## ✨ Star the Repo!
If you found this script useful, **please star this repository**! :)