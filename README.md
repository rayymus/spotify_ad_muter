# Spotify Ad Muter
Mutes Spotify ads and removes the large banner ad.
## How it works
- Every few seconds, takes a screenshot and checks if there is a large banner advertisement or music advertisement.
- Plays a beep sound before opening Spotify, muting, and returning to the original window.
## Running
- Download the files
- Install the modules in the `requirements.txt` file
- Run the `main.py` file
## Installing Tesseract
- Run the following command to install `brew` and follow the instructions to add it to path
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- Run the following command to install tesseract
```
brew install tesseract
```
## Debugging
- Make sure the Spotify app is open
- Adjust the `MUTE_BUTTON_LOCATION` variable in the code to the position of the mute button on the app (assuming the window does not move)
- Make sure the Spotify window is not too small
- Make sure the mute status in printed on the console is correct; "working... currently **muted**"
- Check if the programme is able to properly detect advertisements
## Acknowledgements
`beep.mp3` taken from [pixabay](https://pixabay.com/sound-effects/ping-82822/)
## *IMPORTANT*
This only works on **MacOS**
For this to work on windows, modifications have to be made to the `takeScreenshot` function and the switching of windows.
