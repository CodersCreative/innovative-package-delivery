import customtkinter
from chat import ChatScreen
from utils import Progress
from constants import *
from login import FormInput
from constants import *

class SupportDashboardScreen(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.chat = ChatScreen(master=self, width=300);
        self.chat.pack(fill="y", side="left", anchor="e")
    
        self.details = Contents(master=self, fg_color="transparent");
        self.details.pack(fill="both", side="right", expand=True)


class Package(customtkinter.CTkFrame):
    def __init__(self, master, stage, name, time, height, fg_color=ALTERNATE_DARK_COLOUR, **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)
        self.name = customtkinter.CTkLabel(self, text=name, font=LARGE_FONT)
        self.name.pack(side="left", anchor="w", fill="y", expand=True)
        self.stage = Progress(self, stage=stage, stages=PROGRESS_STAGES, height=height, fg_color="transparent")
        self.stage.pack(anchor="s", fill="x", expand=True,)
        self.time = customtkinter.CTkLabel(self, text=time)
        self.time.pack(side="right", anchor="e", fill="y", expand=True)

class Packages(customtkinter.CTkScrollableFrame):
    def __init__(self, master, packages, **kwargs):
        super().__init__(master, **kwargs)
        self.package_widgets = []
        self.update_messages(packages)

    def update_messages(self, packages):
        self.destroy_children()
        self.package_widgets = []
        
        for package in packages:
            package = Package(master=self, name=package["name"], stage=package["stage"], time=package["time"], height = 20,) 
            package.pack(pady=PADDING_SMALL, anchor="w", fill="x", padx = (0, PADDING_LARGE), expand=True)            
            self.package_widgets.append(package)
            
    def destroy_children(self):
        try:
            for widget in self.package_widgets:
                widget.destroy()
        except:
            pass

class Contents(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.smaster = master.master
        self.user_id = customtkinter.StringVar()
        self.user_id.set("1")
        self.packages = Packages(self, packages=[], fg_color="transparent") 
        self.packages.pack(expand=True, fill="both")
        self.change_package()

    def change_package(self):
        smaster = self.smaster
        try:
            self.user_box.destroy()
            self.packages.destroy_children()
        except:
            pass

        packages = []

        user_activity = smaster.users[smaster.users["user_id"] == int(self.user_id.get())]
        
        for _, package in user_activity.iterrows():
            try:
                pid = package["parcel_id"]
                pack = smaster.parcels[smaster.parcels["parcel_id"] == pid]
                packd = smaster.delivery[smaster.delivery["parcel_id"] == pid]
                packages.append({"name" : pack["parcel_id"].values[0], "stage" : packd["stage"].values[0], "time" : packd["timestamp"].values[0]})
            except:
                pass

        self.packages.update_messages(packages)

        self.user_box = FormInput(self, input_var=self.user_id, command=self.change_package, fg_color="transparent", width=self._current_width);
        self.user_box.pack(anchor="n")



