import customtkinter as ctk
from constants import *
from llm import add_to_messages_and_gen, messages_chat, add_to_messages_and_gen_data, messages_chat_data
from login import FormInput

class Message(ctk.CTkFrame):
    def __init__(self, master, title, text, fg_color="grey", width=300, **kwargs):
        super().__init__(master, fg_color=fg_color, width=width, **kwargs)
        self.title = ctk.CTkLabel(self, text=title, fg_color=fg_color, width=width, height=10, justify="left")
        self.text = MessageText(self, text=text, fg_color=DEFAULT_COLOUR)
        self.title.pack(padx=0, pady=0, side="top")
        self.text.pack(padx=PADDING_LARGE, pady=PADDING_LARGE, fill="both", expand=True, side="bottom")

class MessageText(ctk.CTkFrame):
    def __init__(self, master, text, fg_color=DEFAULT_COLOUR, **kwargs):
        super().__init__(master, fg_color=fg_color,**kwargs)
        self.text = ctk.CTkTextbox(self, font=MEDIUM_FONT, width=SIDEBAR_SIZE, fg_color=fg_color, text_color=TEXT_COLOUR, height=75)
        self.text.insert("0.0", text)
        self.text.pack()

class Chat(ctk.CTkScrollableFrame):
    def __init__(self, master, messages, **kwargs):
        super().__init__(master, **kwargs)
        self.message_widgets = []
        self.update_messages(messages)

    def update_messages(self, messages):
        for widget in self.message_widgets:
            widget.destroy()
        self.message_widgets = []
        
        for msg in messages:
            colour = AI_CHAT_COLOUR if msg["title"] == "AI" else ACCENT_COLOUR
            message = Message(master=self, title=msg["title"], text=msg["text"], fg_color=colour, width=300)
            message.pack(padx=PADDING_SMALL, pady=PADDING_SMALL, fill="x")
            self.message_widgets.append(message)

class ChatScreen(ctk.CTkFrame):
    def __init__(self, master, fg_color=ALTERNATE_DARK_COLOUR, **kwargs):
        super().__init__(master, fg_color=fg_color, **kwargs)
        self.master = master
        self.messages = messages_chat
        self.inp = ctk.StringVar()
        self.inp.set("")

        self.event = ctk.CTkButton(self, text="<", command=self.login, font=MEDIUM_FONT, width=SIDEBAR_SIZE, height=10, fg_color=ACCENT_COLOUR)
        self.event.pack(side="top", anchor="n", padx=PADDING_SMALL)

        self.inp_data = ctk.StringVar()
        self.inp_data.set("")

        self.tabview = ctk.CTkTabview(self, fg_color="transparent", text_color=DEFAULT_COLOUR, segmented_button_selected_color=TEXT_COLOUR, segmented_button_fg_color=DEFAULT_COLOUR)
        self.tabview.pack(fill="both", expand=True)

        self.tabview.add("Parcels")  # add tab at the end
        self.tabview.add("General")
        self.tabview.set("Parcels")
        
        self.gen_chat = ctk.CTkFrame(master=self.tabview.tab("General"), fg_color="transparent")
        self.gen_chat.pack(expand=True, fill="both")

        self.chat = Chat(master=self.gen_chat, messages=messages_chat, fg_color="transparent", scrollbar_button_color=TEXT_COLOUR);
        self.chat.pack(anchor="n", fill="both", expand=True)

        self.input = FormInput(master=self.gen_chat, input_var=self.inp, command=self.enter, fg_color="transparent")
        self.input.pack(anchor="s", fill="x", pady=(0, PADDING_LARGE))


        self.data_chat = ctk.CTkFrame(master=self.tabview.tab("Parcels"), fg_color="transparent")
        self.data_chat.pack(expand=True, fill="both")

        self.chat_data = Chat(master=self.data_chat, messages=messages_chat_data, fg_color="transparent", scrollbar_button_color=TEXT_COLOUR);
        self.chat_data.pack(anchor="n", fill="both", expand=True)

        self.input = FormInput(master=self.data_chat, input_var=self.inp_data, command=self.enter_data, fg_color="transparent")
        self.input.pack(anchor="s", fill="x", pady=(0, PADDING_LARGE))

    def enter(self):
        add_to_messages_and_gen(self.inp.get())
        self.chat.update_messages(messages_chat)

    def enter_data(self):
        add_to_messages_and_gen_data(self.inp_data.get())
        self.chat_data.update_messages(messages_chat_data)

    def login(self):#
        self.master.master.on_login()
