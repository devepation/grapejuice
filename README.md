# Grapejuice

⚠️ You need at least Wine 6.11 or Wine Staging 6.16 for the Roblox Player to work!
Please grab an up to date copy from your repositories. If your repositories don't have Wine 6.11/Wine Staging 6.16, have a look at
[WineHQ's official repositories](https://wiki.winehq.org/Download).

---

These days Roblox works quite well with Wine, though there are some minor issues running it. Grapejuice fills in the
gaps around these issues, so you can experience Roblox to its fullest on your favourite Linux distribution.

The primary gap-filler feature is the fact that Wine by default creates no protocol handlers, which is how Roblox
functions at its core. Without protocol handling, you won't be able to launch Roblox Studio and Experiences from the
website!

Note that Grapejuice is unofficial software. This is not officially supported by Roblox.

## Installing Grapejuice from source

The installation guide can be found in the [documentation](https://brinkervii.gitlab.io/grapejuice/docs/).

## Troubleshooting

Are you experiencing some trouble running Roblox Studio with Grapejuice? Please check out
the [troubleshooting guide](https://brinkervii.gitlab.io/grapejuice/docs/Troubleshooting).

## Features

- Sets up a Wine prefix automatically
- Edit Roblox experiences from the website
- Enjoy Roblox experiences by launching them from the website
- FFlag editor for tweaking Roblox's behaviour

## Roblox and Wine compatibility

Most of Studio's features work on the latest version of Wine. Known issues:

- Black box following cursor
- Flickering widgets (see troubleshooting section for a fix)

Known issues on the player:

- Locking the cursor, such as by right clicking to rotate the camera, causes the cursor to stay locked.
You can install a pre-compiled patched Wine version by running [this Python script](https://pastebin.com/raw/5SeVb005),
or you can compile Wine yourself using [this guide](https://github.com/e666666/robloxWineBuildGuide).
Be careful with the guide and the script, as they're made from people on the internet.
- Window decorations (bar on the top of windows) can disappear after entering and exiting fullscreen
- Screenshot key in the player doesn't work, but screenshot button does
- Built-in screen recorder doesn't work
- Player process occasionally stays after closing the window
- Non-QWERTY keyboard layouts can cause problems with controls
