import asyncio
import kivy
import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class MafiaApp(App):
    def build(self):
        self.lock=asyncio.Lock
        self.temp=False
        self.bufer=""
        layout = BoxLayout(orientation='vertical')
        self.input = TextInput(
            multiline=False, readonly=False
        )
        btn1 = Button(text='proceed')
        self.label = Label()
        btn1.bind(on_press=self.move)
        layout.add_widget(self.label)
        layout.add_widget(self.input)
        layout.add_widget(btn1)
        
        return layout

    def move(self,instance):
        if self.temp:
            pass
        else:
            self.buffer=self.input.text
            self.temp=True
        self.input.text=""

    async def get_string(self):
        while not self.temp:
            await asyncio.sleep(0.1)
        self.temp=False
        wyn=self.buffer
        return wyn



    async def in_t(self,string=None):
        if string!=None:
            await self.out(string)
        while True:
            n=await self.get_string()
            if n.isdigit():
                return int(n)
            else:
                await self.out("zła liczba\n")

    async def in_str(self,string=None):
        if string!=None:
            await self.out(string)
        return await self.get_string()
    
    async def out(self,name):
        if len(self.label.text)>1000:
            self.label.text=self.label.text[100:]
        self.label.text+=name


    async def reset_label(self):
        self.label.text=""