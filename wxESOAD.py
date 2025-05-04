import os, platform, sys, wx
from pathlib import Path
from threading import Thread
from addondownloader import AddonDownloader

def touch_file(filename):
    """Makes sure file exists"""
    filename = Path(filename)
    filename.touch(exist_ok=True)
    return filename

def create_addon_files():
    addons_file = open(touch_file("addons.txt"), "r+")
    addons_location_file = open(touch_file("addonslocation.txt"), "r+")
    addons = addons_file.read()
    addons_location = addons_location_file.read()
    if addons_location == "":
        if platform.system() == "Windows":
            addons_location = os.path.abspath(os.path.expanduser("~\\Documents\\") + "Elder Scrolls Online\\live\\AddOns\\")
        else:
            addons_location = f"{Path.home()}/.local/share/Steam/steamapps/compatdata/306130/pfx/drive_c/users/steamuser/Documents/Elder Scrolls Online/live/AddOns"
    addons_file.close()
    addons_location_file.close()
    return addons_location, addons

def update_status_text(text):
    statusbar.SetStatusText(text)

def on_start_download(event):
    #Save all the input data to text files
    #ESO addon location folder
    addons_location_field.SaveFile(filename="addonslocation.txt")
    #List of links
    textbuffer = addon_link_textview.SaveFile(filename="addons.txt")

    adlthread = Thread(target=adl.start)
    handle_thread(adlthread)

def handle_thread(thread):
    thread.daemon = True
    try:
        thread.start()
    except Exception as err:
        update_status_text(str(err))


addons_location, addons = create_addon_files()
adl = AddonDownloader(update_status_text)

# GUI starts here
app = wx.App(False)
frame = wx.Frame(None, wx.ID_ANY, title="wxESOAD (ESO Addon Downloader)", size=(500, 600))
frame.SetIcon(wx.Icon(os.path.join(os.path.dirname(__file__), "esotux.png")))
frame.Centre()
frame.SetMinSize(size=(500, 600))

p = wx.Panel(frame)
vs = wx.BoxSizer(wx.VERTICAL)

# Addons location
addonslbl = wx.StaticText(p, wx.ID_ANY, label="ESO Addon folder location:")
addons_location_field = wx.TextCtrl(p, value=addons_location)

def select_directory(event):
    with wx.DirDialog(None, "Select Addons Directory", defaultPath=addons_location_field.GetLineText(0), style=wx.DD_SHOW_HIDDEN) as addons_location:
        addons_modal = addons_location.ShowModal()
        if addons_modal != wx.ID_OK:
            pass
        else:
            addons_location_field.SetValue(value=addons_location.GetPath())

aobutton = wx.Button(p, wx.ID_ANY, "Select")
aobutton.Bind(wx.EVT_BUTTON, select_directory)

# Addons links
addonslinkslbl = wx.StaticText(p, wx.ID_ANY, label="Links to ESOUI.com addon pages, one per line:")
addon_link_textview = wx.TextCtrl(p, wx.ID_ANY, value=addons, style=wx.TE_MULTILINE|wx.TE_DONTWRAP)
addon_link_textview.SetFocus()

# Download button
dlButton = wx.Button(p, wx.ID_ANY, "Download")
dlButton.Bind(wx.EVT_BUTTON, on_start_download)

# Status bar
statusbar = wx.StatusBar(p, wx.ID_ANY, wx.STB_ELLIPSIZE_END)
statusbar.SetStatusText("Ready to download...")

vs.Add(addonslbl, 0, wx.EXPAND | wx.ALL, border=5)
vs.Add(addons_location_field, 0, wx.EXPAND | wx.ALL, border=5)
vs.Add(aobutton, 0, wx.EXPAND | wx.ALL, border=5)
vs.Add(addonslinkslbl, 0, wx.EXPAND | wx.ALL, border=5)
vs.Add(addon_link_textview, 1, wx.EXPAND | wx.ALL, border=5)
vs.Add(dlButton, 0, wx.EXPAND | wx.ALL, border=5)
vs.Add(statusbar, 0, wx.EXPAND)

p.SetSizer(vs)

frame.Show(True)
app.MainLoop()

