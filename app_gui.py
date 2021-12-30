from tkinter import *
from allfunctions import date_to_timestamp, get_data, lowest_and_highest_price
import allfunctions

class MyWindow:
    def __init__(self, win):
        self.btn = Button(win, text="Submit", bg='blue', fg='white', command=self.ButtonClicked)
        self.btn.place(x=350, y=250)
        self.lblfrom = Label(window, text='Enter the start date in format dd/mm/yyyy')
        self.lblto = Label(window, text='Enter the end date in format dd/mm/yyyy')
        self.inputfrom = Entry()
        self.inputto = Entry()
        self.lblfrom.place(x=50,y=150)
        self.lblto.place(x=50,y=200)
        self.inputfrom.place(x=350, y=150)
        self.inputto.place(x=350, y=200)
        self.bearish = Text(window, width=90)
        self.bearish.place(x=30, y= 400)
        self.vol = Text(win, width=90)
        self.vol.place(x=30, y=420)
        self.h_and_l = Text(win, width=90)
        self.h_and_l.place(x=30, y=440)
    def ButtonClicked(self):
        prices = {}
        to_date = allfunctions.date_to_timestamp(self.inputto.get()) + 3600
        from_date = allfunctions.date_to_timestamp(self.inputfrom.get())
        allfunctions.get_day_price(from_date, to_date, prices)
        bear = allfunctions.calculate_bearish(prices)
        highest_vol = allfunctions.highest_volume(allfunctions.get_data(from_date, to_date))
        low_and_high = allfunctions.lowest_and_highest_price(prices)
        self.bearish.insert(END, "The longest bearish trend: " + str(bear) + " days.")
        self.vol.insert(END, "Highest trading volume: " + str(highest_vol))
        if len(low_and_high) == 2:
            self.h_and_l.insert(END, "Best day to buy: " + low_and_high[0])
            self.h_and_l.insert(END, " Best day to sell: " + low_and_high[1])
        else:
            self.h_and_l.insert(END, low_and_high[0])
        
window = Tk()
mywin=MyWindow(window)
window.title('Hello Scrooge!')
window.geometry("800x600+10+10")
window.mainloop()