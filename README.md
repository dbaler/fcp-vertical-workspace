# Vertical Workspace for Final Cut Pro

A Final Cut Pro workspace for editing 9:16 video (Reels, TikTok, Shorts).

It is Final Cut's Default layout with one change: the viewer moves out of the top row and becomes a full-height column on the right, so a vertical clip uses the whole height of your screen instead of a small box in the corner.

```
+--------------------+-----------+---------+
|      Browser       | Inspector |         |
+--------------------+-----------+ Viewer  |
|                                |  (full  |
|            Timeline            | height) |
|                                |         |
+--------------------------------+---------+
```

Tested on Final Cut Pro 12.4, macOS 26. Works best on wide and ultrawide monitors.

## Install

1. Download the latest zip from [Releases](../../releases) and unzip it.
2. Right-click `Install.command` and choose **Open**. (macOS may block a plain double-click on files downloaded from the internet.)
3. Quit Final Cut Pro and open it again.
4. Choose **Window > Workspaces > Vertical**.

### Manual install

Copy `Vertical.fcpworkspace` into:

```
~/Library/Application Support/Final Cut Pro/Workspaces/
```

In Finder use **Go > Go to Folder** and paste the path. Create the `Workspaces` folder if it is missing. Then restart Final Cut Pro.

### Remove

Choose **Window > Workspaces > Default**, then delete `Vertical.fcpworkspace` from the folder above.

## Tips

- Drag the borders between panels to resize them.
- **Window > Workspaces > Save Workspace as** keeps your own sizes as a new workspace.
- Avoid the full-screen viewer (Shift-Command-F) in this workspace for now. It is untested and Final Cut's exit-full-screen code expects the viewer in its usual spot.

## How it works

Final Cut workspaces are property list files (`.fcpworkspace`). Each one describes the window as a tree of panel groups (containers) and the panels inside them (browser, viewer, inspector, timeline), plus how each group is split: side by side or stacked, and in what proportions.

`build.py` reads Apple's own Default workspace from inside the Final Cut app bundle and rearranges it:

- The viewer (`PEMainDisplayArea`) leaves the top row (`PEUpperDeckContainer`).
- The main group (`PEMainContainerModule`) is split side by side: a stacked node holding the top row and the timeline on the left, the viewer on the right.
- Every other panel stays in the group Apple puts it in.

To rebuild after editing proportions:

```bash
python3 build.py
```

### The crash to avoid

The first version moved the viewer out of `PEMainContainerModule` entirely. Final Cut 12.4 crashed the moment the workspace was chosen.

Final Cut decides the viewer is "full screen on another display" whenever the viewer is not inside `PEMainContainerModule`. It then asks that panel which screen it is on, gets the main window instead, and aborts with an unrecognized selector (`screenNumber`) inside `-[PEAppController mainWindowChangedScreens:]`.

Rule: **keep the viewer somewhere inside `PEMainContainerModule`.** Nested splits inside that group are fine.

### Why keep Apple's panel groups

Some workspace generators replace Apple's groups with their own. Final Cut still loads those, but its menu code looks up the top row and timeline groups by name (Hide/Show Timeline, full-height inspector, Event Viewer, Compare Viewer). If those groups are missing, the commands can stop working. This workspace keeps them, and keeps the hidden Event Viewer and Compare Viewer panels too.

## License

MIT. Not affiliated with Apple. Final Cut Pro is a trademark of Apple Inc.
