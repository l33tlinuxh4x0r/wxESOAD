import re, shutil, os, re, zipfile, time, ssl, wx
from urllib.request import urlopen, Request

class AddonDownloader():

    file_number = 0

    headers = {'User-Agent': 'Mozilla/5.0'}

    addons = ""
    addons_location = ""
    addon_temp_folder = "addontemp"
    addon_temp_name = "addon{0}.zip"

    #GUI functions
    set_status_text = None

    def __init__(self, func_set_status_text):
        self.set_status_text = func_set_status_text

    def start(self):
        self.refresh_addon_location()
        self.set_status_text("Starting....")
        if os.path.isdir(self.addon_temp_folder) == False:
            os.mkdir(self.addon_temp_folder)
        links = self.addons.split("\n")
        self.file_number = 0
        for link in links:
            if link != "" and link.startswith("#") != True:
                info = re.findall("esoui.com/downloads/info(\d*)", link)[0]
                download_url = f"https://cdn.esoui.com/downloads/file{info}/{str(int(time.time()))}"
                file = self.download(self.file_number, download_url)
                if file == False:
                    print("Failed to use the new url, using old url instead...")
                    download_url = f"https://cdn.esoui.com/downloads/file{info}/"
                    file = self.download(self.file_number, download_url)
                self.unzip(file)
                self.file_number += 1
        #delete temp folder
        shutil.rmtree(self.addon_temp_folder)
        self.end()

    def download(self, file_number, download_url):
        self.set_status_text("Downloading: " + download_url)
        tempfilename = self.addon_temp_folder + "/" + self.addon_temp_name.format(str(file_number))
        request = Request(url=download_url, headers=self.headers)
        response = urlopen(request)
        if response.getcode() != 200:
            return False
        with open(tempfilename, "wb") as f:
            f.write(response.read())
        return tempfilename


    def unzip(self, file, custom_location=""):
        self.set_status_text("Unzipping: " + file)
        with zipfile.ZipFile(file, 'r') as z:
            if custom_location == "":
                z.extractall(self.addons_location)
            else:
                z.extractall(custom_location)

    def refresh_addon_location(self):
        addons_file = open("addons.txt", "r")
        addons_location_file = open("addonslocation.txt", "r")
        self.addons = addons_file.read()
        self.addons_location = addons_location_file.read()

    def end(self):
        self.set_status_text("Done! Addons downloaded and unzipped.")
        wx.MessageBox(f"Addons downloaded and unzipped to {self.addons_location}", "Success!")

