import customtkinter
from chat import ChatScreen
from utils import Progress
from constants import *
import tkintermapview

class DriverDashboardScreen(customtkinter.CTkFrame):
    def __init__(self, master, driver, **kwargs):
        super().__init__(master, **kwargs)
        self.chat = ChatScreen(master=self, width=300);
        self.chat.pack(fill="y", side="left", anchor="e")
    
        self.details = Contents(master=self, fg_color="transparent", driver=driver);
        self.details.pack(fill="both", side="right", expand=True)


class Contents(customtkinter.CTkFrame):
    def __init__(self, master, driver, **kwargs):
        super().__init__(master, **kwargs)
        smaster = master.master
        self.driver = driver
        self.driver_profile = smaster.drivers[smaster.drivers["driver_id"] == driver]
        driver_activity = smaster.delivery[smaster.delivery["driver_id"] == driver]
        self.packages = []
        self.package_deliveries = []
        self.markers = []

        self.package_names = []

        for i, package in driver_activity.iterrows():
            try:
                stage = package["stage"]
                if stage != PROGRESS_STAGES[len(PROGRESS_STAGES) -1]:
                    pid = package["parcel_id"]
                    pack = smaster.parcels[smaster.parcels["parcel_id"] == pid]
                    packd = smaster.delivery[smaster.delivery["parcel_id"] == pid]
                    self.package_names.append(str(pack["parcel_name"].values[0]))
                    self.packages.append(pack)
                    self.package_deliveries.append(packd)
                    self.markers.append((float(packd['latitude'].values[0]), float(packd['longitude'].values[0]), str(pack["parcel_name"].values[0])))
            except:
                pass
            #

        # print(self.package_deliveries[0].iloc[0])
        self.package_var = customtkinter.StringVar()
        self.current_package = self.packages[0]
        self.current_package_deliveries = self.package_deliveries[0]
        self.package_var.set(self.package_names[0])
        self.change_package(self.package_names[0])


    def change_package(self, choice):
        self.package_var.set(choice)
        try:
            self.stats.destroy()
            self.package_box.destroy()
            self.progress.destroy()
            self.map_widget.destroy()
            self.rides.destroy()
            self.rating.destroy()
        except:
            pass
        for pack in self.packages:
            if pack["parcel_name"].values[0] == choice:
                self.current_package = pack
                print("found")
                for packd in self.package_deliveries:
                    if pack["parcel_id"].values[0] == packd["parcel_id"].values[0]:
                        self.current_package_deliveries = packd
                        print("found2")
                        break
                break

        self.rides = customtkinter.CTkLabel(self, text="{} Rides\nAvg Mins/Ride : {}".format(self.driver_profile["rides"].values[0], int(self.driver_profile["average_distance_per_ride"].values[0] / self.driver_profile["average_speed"].values[0] * 60)), font=OMEGA_FONT, justify="left")
        self.rides.pack(anchor="w")
        percent = self.driver_profile["average_rating"].values[0] / 5
        self.rating = customtkinter.CTkProgressBar(self, orientation="horizontal", height = 20, width=300, progress_color=ACCENT_COLOUR, fg_color=ALTERNATE_DARK_COLOUR, border_color=TEXT_COLOUR, border_width=1)
        self.rating.set(percent);
        self.rating.pack( anchor="w", padx = (0, PADDING_LARGE), pady = (PADDING_SMALL, PADDING_LARGE * 2))
        self.package_box = customtkinter.CTkComboBox(self, values=self.package_names, command=self.change_package, variable=self.package_var, width=300, height=30, text_color=TEXT_COLOUR, button_color=DEFAULT_COLOUR, border_color=TEXT_COLOUR, border_width=1, fg_color=DEFAULT_COLOUR);
        self.package_box.pack(anchor="w")        
        self.progress = Progress(self, stages=PROGRESS_STAGES, stage=self.current_package_deliveries["stage"].values[0], width=self.package_box._current_width-200, height = 20) 
        self.progress.pack(pady=PADDING_SMALL, anchor="w", fill="x", padx = (0, PADDING_LARGE))        
        self.stats = customtkinter.CTkLabel(self, fg_color="transparent", text=f"{self.current_package['parcel_weight'].values[0]} Kg - {self.current_package_deliveries['timestamp'].values[0]}", font=LARGE_FONT, justify="left")

        self.stats.pack()

        self.map_widget = tkintermapview.TkinterMapView(self)
        for marker in self.markers:
            self.map_widget.set_marker(marker[0], marker[1], marker[2])

        self.map_widget.set_position(float(self.current_package_deliveries['latitude'].values[0]), float(self.current_package_deliveries['longitude'].values[0]))
        self.map_widget.pack(fill="both", expand=True)


