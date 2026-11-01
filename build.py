#!/usr/bin/env python3
"""Build a "Vertical" Final Cut Pro workspace from Apple's Default workspace.

Layout: Default (browser and inspector over timeline) with the viewer
as a full-height column on the far right. Built for 9:16 reels.
"""
import plistlib, subprocess
from pathlib import Path

FCP = Path("/Applications/Final Cut Pro.app/Contents/Resources/Workspaces/Factory 1 - Default.moduleLayout")
OUT = Path(__file__).with_name("Vertical.fcpworkspace")
NAME = "Vertical"
# Fixed UUID so reinstalling replaces the same workspace instead of adding a copy.
IDENT = "5E1F9A2C-7B3D-4C8E-9A61-0D2B4F6E8A11"

# Factory files start with blank lines, so let plutil parse them.
raw = subprocess.run(["plutil", "-convert", "xml1", "-o", "-", str(FCP)], check=True, capture_output=True).stdout
p = plistlib.loads(raw)

def find(m, ident):
    if m.get("Identifier") == ident:
        return m
    for s in m.get("Submodules", []):
        r = find(s, ident)
        if r:
            return r

main_win = next(l for l in p["Layouts"] if l.get("Identifier") == "PEMainWindowModule")
maincont = find(main_win, "PEMainContainerModule")
upper = find(main_win, "PEUpperDeckContainer")
lower = find(main_win, "PELowerDeckContainer")
viewer = find(upper, "PEMainDisplayArea")

# Default layout, but the viewer leaves the top row and becomes a full-height
# column on the right. It must stay inside PEMainContainerModule: Final Cut
# crashes if it sits anywhere else (it thinks the viewer is on a second display).
upper["Submodules"] = [s for s in upper["Submodules"] if s is not viewer]
maincont["Submodules"] = [upper, lower, viewer]

# Main container: [ (top row over timeline) | viewer ]
maincont["containersLayout"] = {"root": {
    "CurrentSize": "{1280, 705}",
    "allowSeamDragging": True,
    "orientation": 1,
    "proportion": 0.0,
    "items": [
        {
            "CurrentSize": "{1000, 705}",
            "allowSeamDragging": True,
            "isVisible": True,
            "orientation": 0,
            "proportion": 0.8,
            "items": [
                {"CurrentSize": "{1000, 353}", "Identifier": "PEUpperDeckContainer", "isVisible": True, "proportion": 0.5},
                {"CurrentSize": "{1000, 352}", "Identifier": "PELowerDeckContainer", "isVisible": True, "proportion": 0.5},
            ],
        },
        {"CurrentSize": "{280, 705}", "Identifier": "PEMainDisplayArea", "isVisible": True, "proportion": 0.2},
    ],
}}

# Top row keeps Default's order minus the viewer: browser, then inspector.
upper["containersLayout"] = {"root": {
    "CurrentSize": "{1000, 353}",
    "allowSeamDragging": True,
    "orientation": 1,
    "proportion": 1.0,
    "items": [
        {"CurrentSize": "{597, 353}", "Identifier": "PEMediaEventOrganizerContainerModule", "isVisible": True, "proportion": 1.0},
        {"Identifier": "PECompareDisplayArea", "isVisible": False, "proportion": 0.0},
        {"Identifier": "PEMediaEventDisplayArea", "isVisible": False, "proportion": 0.0},
        {"CurrentSize": "{403, 353}", "Identifier": "PEInspectorColorSwapModule", "isVisible": True, "userResizableOnly": True},
    ],
}}

# Let Final Cut's drag-to-rearrange code act on our panel groups (same as the
# workspaces made by online generators). Untested in 12.4; set False to undo.
REARRANGE = True
for m in (find(main_win, "PEOuterContainerModuleID"), maincont, upper, lower):
    m["canRearrangeLayout"] = REARRANGE

lower["containersLayout"]["root"]["CurrentSize"] = "{1000, 352}"
lower["containersLayout"]["root"]["items"][0]["CurrentSize"] = "{1000, 352}"

p["Identifier"] = IDENT
p["Source Name"] = IDENT
p["Display Name"] = NAME
OUT.write_bytes(plistlib.dumps(p, fmt=plistlib.FMT_XML))
print(OUT)
