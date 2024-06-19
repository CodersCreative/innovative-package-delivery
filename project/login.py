import customtkinter
from constants import *

class FormInput(customtkinter.CTkFrame):
    def __init__(self, master, command, input_var, button_text=">", button_color=ACCENT_COLOUR, txt_color=DEFAULT_COLOUR, entry_colour=DEFAULT_COLOUR, entry_border_color=TEXT_COLOUR, entry_txt_colour=TEXT_COLOUR,**kwargs):
        super().__init__(master, **kwargs);
        
        self.entry = customtkinter.CTkEntry(self, textvariable=input_var, border_color=entry_border_color, text_color=entry_txt_colour, fg_color=entry_colour, border_width=1, font=MEDIUM_FONT);
        self.entry.pack(side="left", anchor="w", expand=True, fill="both", padx=PADDING_SMALL)

        self.event = customtkinter.CTkButton(self, text=button_text, command=command, width=self.entry._current_height, height=self.entry._current_height, text_color=txt_color, fg_color=button_color, font=LARGE_FONT)
        self.event.pack(side="left", anchor="e", padx=PADDING_SMALL)

class LoginScreen(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs);
        
        self.master = master


        self.user_id = customtkinter.StringVar()
        self.user_id.set("Enter User ID")

        self.driver_id = customtkinter.StringVar()
        self.driver_id.set("Enter Driver ID")
        
        self.support_id = customtkinter.StringVar()
        self.support_id.set("Enter Support ID")


        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.pack(anchor="center")

        self.user = FormInput(self.container, fg_color="transparent", command=self.user_fn, input_var=self.user_id)
        self.user.pack(pady=PADDING_SMALL)

        self.driver = FormInput(self.container, fg_color="transparent", command=self.driver_fn, input_var=self.driver_id)
        self.driver.pack(pady=PADDING_SMALL)


        self.support = customtkinter.CTkButton(self.container, text="Support", command=self.support_fn, width=self.driver._current_width-25, text_color=DEFAULT_COLOUR, fg_color=ACCENT_COLOUR)
        self.support.pack(pady=PADDING_SMALL, padx=PADDING_SMALL)


    def support_fn(self):
        self.master.on_support()
    
    def driver_fn(self):
        self.master.on_driver(self.driver_id.get())

    def user_fn(self):
        self.master.on_user(self.user_id.get())
