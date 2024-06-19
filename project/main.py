import customtkinter
from login import LoginScreen
import pandas as pd
from constants import *
from llm import setup_chat
from user_dashboard import UserDashboardScreen 
from support_dashboard import SupportDashboardScreen 
from driver_dashboard import DriverDashboardScreen 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__(fg_color=DEFAULT_COLOUR)
        self.title("Parcel")
        self.geometry(f"{WINDOW_SIZE['x']}x{WINDOW_SIZE['y']}")
        self.grid_rowconfigure((0,1,2), weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

        self.drivers = pd.read_csv("./data/drivers.csv")
        self.parcels = pd.read_csv("./data/parcels.csv")
        self.users = pd.read_csv("./data/user_activity.csv")
        self.delivery = pd.read_csv("./data/parcel_delivery.csv")
        print(self.delivery)
    
        customtkinter.DrawEngine.preferred_drawing_method = "circle_shapes";
        customtkinter.set_widget_scaling(2);
        customtkinter.set_appearance_mode("dark");
        # customtkinter.set_default_color_theme("dark-blue");

        self.on_login()

    def on_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.login = LoginScreen(master=self, fg_color="transparent");
        # self.login.pack(expand=True, fill="both", anchor="center")
        self.login.grid(column=1, row=1)
    def on_user(self, user_id):
        for widget in self.winfo_children():
            widget.destroy()
        try:
            self.dash = UserDashboardScreen(master=self, fg_color="transparent", user=int(user_id));
            self.dash.pack(expand=True, fill="both")
        except:
            pass

    def on_support(self,):
        for widget in self.winfo_children():
            widget.destroy()
        self.dash = SupportDashboardScreen(master=self, fg_color="transparent",);
        self.dash.pack(expand=True, fill="both")
    

    def on_driver(self, driver_id):
        for widget in self.winfo_children():
            widget.destroy()

        try:
            self.dash = DriverDashboardScreen(master=self, fg_color="transparent", driver=int(driver_id));
            self.dash.pack(expand=True, fill="both")
        except:
            pass

if __name__ == "__main__":
    setup_chat()
    app = App()
    app.mainloop()
