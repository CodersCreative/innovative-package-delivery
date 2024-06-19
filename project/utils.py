import customtkinter
from chat import ChatScreen
from constants import *

class Progress(customtkinter.CTkFrame):
    def __init__(self, master, stages, stage, height=100, width=100,**kwargs):
        super().__init__(master, **kwargs)
        index = 0
        
        for i in range(len(stages)):
            if stage.lower() == stages[i].lower():
                index = i
                break


        print("{} / {}", index, len(stages))
        print(stage.lower())
        print(stages[index])

        percent = float(float(index) + 1.0) / float(len(stages))
        print(percent)
        bar = customtkinter.CTkProgressBar(self, height=height, width=width, orientation="horizontal", progress_color=AI_CHAT_COLOUR, fg_color=ALTERNATE_DARK_COLOUR, border_color=TEXT_COLOUR, border_width=1)
        bar.set(percent);
        bar.pack(expand=True, fill="both")




