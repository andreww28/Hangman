import random
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk,Image
import time
import os

root = tk.Tk()

guess_string_text = tk.StringVar()
remaning_lives = tk.StringVar()
lives_count = 8
remaning_lives.set(8)

correct_guess_letter_list = [] 
wrong_guess_letter_list = []                #store all wrong guess letter that the user entered, this will avoid duplication of wrong letter that result of reducing the lives

chosen_category = StringVar()
chosen_category.set("Person")
options = ["Person", "Fruits", "Animals", "Country"]

chosen_category_animal = StringVar()
chosen_category_animal.set("Land")
animalType_options = ["Land", "Air", "Water"]

chosen_category_continent = StringVar()
chosen_category_continent.set("Asia")
continent_options = ["Asia", "Africa", "Europe","North America", "South America"]


def main():
    app = Main(root)
    root.mainloop()


def getRandomText():
    category = chosen_category.get()            #getting the selected option in optionmenu
    random_list = Random_List()         #creating an instance of random_list class. This will help to access the list of random string based on the category

    if category == "Person":
        choices = random_list.person()  #assigning the list of person name from random list class to variable choices

    if category == "Animals":
        choices = random_list.animal()

    if category == "Fruits":
        choices = random_list.fruits()

    if category == "Country":
        choices = random_list.country()

    chosen_word = random.choice(choices)        #Choosing a random string from the selected list based on the chosen category
    chosen_word = chosen_word.replace(" ", "\n")  #replacing the white spaces to new line to know that it is more than one word
    
    return chosen_word.upper()

def get_chosen_random_string():  #this will also display the unknown random text in screen
    word = ""
    guessWord = getRandomText()  #assigning the chosen random string from that function

    for letter in guessWord:
        word += letter + " "

    guess_string_text.set(re.sub('[A-Z]','_',word))   #replacing letter to _ 
    return guessWord   #Purpose of returning the random text: Avoid changing the unknown string, this will help to display the correct letter entered by user 


class Main:
    global chosen_category
    global option

    width = 850
    height = 700
    x = int((1920 - width)/2)
    y = int((1080 - height)/2)

    def __init__(self,window):
        self.window = window
        self.window.title("Hangman")
        self.window.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x,self.y))
        self.window.resizable(0,0)

        icon = ImageTk.PhotoImage(file = ".\\img\\icon.png")
        self.window.iconphoto(False, icon)

        #configuring widgets 
        self.footer = tk.Label(self.window, text="Developed by:  John Andrew San Victores", fg="#111111", font=("Dubai Light",10, "bold"))
        self.mainFrame = tk.Frame(self.window, bg = "black")
        self.guessLabel = tk.Label(self.mainFrame, textvariable=guess_string_text, fg='#CDC6EC',bg = "#0C0919" ,font=("Broadway",38))
        self.catLabel = tk.Label(self.mainFrame, text="CATEGORY", fg='white', bg="black", font=("Berlin Sans FB Demi",18))
        self.category_list = tk.OptionMenu(self.mainFrame, chosen_category, *options,command = self.OptionMenu_SelectionEvent)
        self.lives_label = tk.Label(self.mainFrame, text="Lives:", fg='white', bg="black", font=("Berlin Sans FB Demi",18))
        self.remaining_life = tk.Label(self.mainFrame, textvariable=remaning_lives, fg='white', bg="black", font=("AR CHRISTY",18))
        self.inputGuess = tk.Entry(self.mainFrame, font=("", 24), bg="#A598DC")
        

        #displaying widgets on the screen
        self.footer.pack(anchor=tk.E, side="bottom")
        self.mainFrame.place(relwidth=1, relheight=0.96)
        self.display_img(img_filename=".\\img\\img1.png") #Display the default image where the hangman image is
        self.guessLabel.place(relx = 0.05, rely =0.5, relwidth=1-.1, relheight =0.96-0.65)
        self.catLabel.place(relx = (0.289 - 0.2)/2, rely=0.02, relwidth = 0.2, relheight=0.1)
        self.category_list.place(relwidth=0.15, anchor = tk.NW, rely = 0.1, relx = (0.289-0.15)/2)
        self.lives_label.place(relx =(0.289+.422) + (0.289 - 0.15)/2 , rely=0.04, relwidth = 0.15, relheight=0.06) 
        self.remaining_life.place(relx =(0.289+.422) + (0.289 - 0.02)/2 , rely=0.02 + 0.07, relwidth = 0.02, relheight=0.1) 
        self.inputGuess.place(relwidth=0.2, rely = 0.86, relx=(1-0.2)/2)


        self.inputGuess.bind('<Return>', self.submitChr)
        self.guessWord = get_chosen_random_string()  


    def display_img(self, img_filename=""):
        try:
            self.pic.place_forget()     #avoid overlaying of hangman image
        except:
            pass

        #displaying the hangman image
        self.load = Image.open(img_filename)
        self.render = ImageTk.PhotoImage(self.load)
        self.pic = tk.Label(self.window, image=self.render)
        self.pic.image = self.render
        self.pic.place(relx = .578/2, rely = 0.05, relwidth=1-.578, relheight = 0.96-0.55)
        

    def setDefault(self):
        global wrong_guess_letter_list
        global correct_guess_letter_list
        global lives_count

        self.guessWord = get_chosen_random_string()         #changing the unknown random  string when the game start again
        self.guessLabel.config(fg="white")
        self.display_img(img_filename=".\\img\\img1.png")
        self.inputGuess.delete(0, tk.END)

        wrong_guess_letter_list.clear()
        correct_guess_letter_list.clear()
        remaning_lives.set(8)
        lives_count = 8


    def OptionMenu_SelectionEvent(self, evt):
        try:        #This will remove the subOptions menu when the user selected other than animals and country
            self.category_list_animal.destroy()
            self.category_list_continent.destroy()
        except:
            pass

        if chosen_category.get() == "Animals":       #displaying the sub option for animals if the user select the animals in main option menu
            self.category_list_animal = tk.OptionMenu(self.mainFrame, chosen_category_animal, *animalType_options,command = self.SubOptionMenu_SelectionEvent)
            self.category_list_animal.place(relwidth=0.13, anchor = tk.NW, rely = 0.17, relx = (0.289-0.13)/2)

        if chosen_category.get() == "Country":  #displaying the sub option for country if the user select the country in main option menu
            self.category_list_continent = tk.OptionMenu(self.mainFrame, chosen_category_continent, *continent_options,command = self.SubOptionMenu_SelectionEvent)
            self.category_list_continent.place(relwidth=0.16, anchor = tk.NW, rely = 0.17, relx = (0.289-0.15)/2)

        self.setDefault()   #setting all to default when the user change the category in main option menu
        
        
    def SubOptionMenu_SelectionEvent(self,evt):
        self.setDefault()   #setting all to default when the user change the category in sub option menu

        
    def set_state_of_optionMenu(self,state):  # changing the state of all option menu if the unknown word giessed or when you are dead
        self.category_list.config(state=state)

        try:
            self.category_list_animal.config(state=state)
        except:
            try:
                self.category_list_continent.config(state=state)
            except:
                pass


    def playAgain(self):    #execute if the user press the play again button
        self.playBtn.place_forget()
        self.inputGuess.place(relwidth=0.2, rely = 0.86, relx=(1-0.2)/2)
        self.set_state_of_optionMenu(NORMAL)
        self.setDefault()
        self.window.unbind('<Return>')

    def play_again_event(self, evt):
        self.playAgain()

    def startOver(self):    #execute if the user guessed the unknown word or when the game is over
        self.inputGuess.place_forget()

        self.load = Image.open(".\\img\\retry2.png")
        image = self.load.resize((212,70), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(image)
        self.playBtn = tk.Button(self.mainFrame, image = self.render, command=self.playAgain, cursor="hand2", borderwidth=0, bg="black", activebackground="black")
        self.playBtn.place(relwidth=0.25, rely = 0.85, relx=(1-0.25)/2)

        self.window.bind('<Return>', self.play_again_event)
        self.set_state_of_optionMenu(DISABLED)


    def submitChr(self, evt):   
        global lives_count
        self.inputChr = self.inputGuess.get().upper()
        self.inputGuess.delete(0,tk.END)

        if len(self.inputChr) == 1 and ord(self.inputChr) in range(65,97):  #check if the input character is valid
            check_text = Text(self.inputChr, self.guessWord)
            check_text.check() #calling check function in text class which check if the input character is in the unknown word

            check_guesses = guess_string_text.get().replace(" ","").replace("\n","")  #getting the text in guess_label and removing all white spaces 
            correct_word = self.guessWord.replace(" ", "").replace("\n", "")    #getting the unknown word then removing all  white spaces

            self.display_hangman_image(lives_count) #displaying the hangman image based on the upadted lives

            reveal_word = ""
            for letter in self.guessWord:
                reveal_word += letter + " "
 
            if lives_count == 0: #check if its gameover
                self.guessLabel.config(fg="red")    #change the font color of guess label on screen to red if dead
                guess_string_text.set(reveal_word)
                self.startOver() #display the play again button 

            if check_guesses == correct_word:  #check if the user guess all the character
                self.guessLabel.config(fg="yellow") #change the font color of guess label on screen to yellow if the user guessed the word
                self.display_img(img_filename=".\\img\\alive.png")
                self.startOver()


    def display_hangman_image(self, remaining_lives_count):   #displaying the hangman images  based on the lives count
        if remaining_lives_count == 7:
            self.display_img(img_filename=".\\img\\img2.png")

        if remaining_lives_count == 6:
            self.display_img(img_filename=".\\img\\img3.png")

        if remaining_lives_count == 5:
            self.display_img(img_filename=".\\img\\img4.png")

        if remaining_lives_count == 4:
            self.display_img(img_filename=".\\img\\img5.png")

        if remaining_lives_count == 3:
            self.display_img(img_filename=".\\img\\img6.png")

        if remaining_lives_count == 2:
            self.display_img(img_filename=".\\img\\img7.png")

        if remaining_lives_count == 1:
            self.display_img(img_filename=".\\img\\img8.png")

        if remaining_lives_count == 0:
            self.display_img(img_filename=".\\img\\img10.png")


class Text: #this class help to check if the input character by user is presemt in unknown word
    temp_guess_string = ""

    def __init__(self, inputChr='', random_str=""):
        self.inputChr = inputChr
        self.random_str = random_str
        

    def check(self):
        global lives_count

        for letter in self.random_str: #this loop help to store the correct letter entered by user
            if self.inputChr == letter: 
                correct_guess_letter_list.append(self.inputChr) #storing the correct letter in the correct letter list

        for i in range(len(self.random_str)): 
            if self.random_str[i] in correct_guess_letter_list or self.random_str[i] == "\n": # check  if the letter is in the unknown word or if the letter is equal to new line
                self.temp_guess_string += self.random_str[i] + " "  #if it is, then the input letter will append to the temp_guess_string
            else:
                self.temp_guess_string += "_ " #if it's not, then the underscore will append to the temp_guess_string

        if self.inputChr not in self.random_str and self.inputChr not in wrong_guess_letter_list:   
            lives_count -= 1
            wrong_guess_letter_list.append(self.inputChr)
            remaning_lives.set(lives_count)

        guess_string_text.set(self.temp_guess_string)   #displating the temp_guess_string in the guess string text label on screen
        check_guesses = guess_string_text.get().replace(" ","").replace("\n","")
        correct_word = self.random_str.replace(" ", "").replace("\n", "")

        if check_guesses == correct_word or lives_count == 0:   
            temp_guess_string = ""  #setting again to none the temp_guess_string
            correct_guess_letter_list.clear()
            wrong_guess_letter_list.clear()
 
class Random_List:

    path = ".\\txt\\"

    def __init__(self):
        self.random_list = []


    def get_string_from_file(self, filename):
        with open(filename, "r") as f:
            for line in f:
                self.random_list.append(str(line[:-1])) #removing the new line(\n) in the current string line

        return self.random_list


    def person(self):
        return self.get_string_from_file(self.path + "person.txt")


    def animal(self):
        animal_category = chosen_category_animal.get()       #assigning the selected option in the animal option menu

        if animal_category == "Land":
            return self.get_string_from_file(self.path +"animal.land.txt")

        if animal_category == "Air":
            return self.get_string_from_file(self.path + "animal.air.txt")

        if animal_category == "Water":
            return self.get_string_from_file(self.path + "animal.water.txt")


    def fruits(self):
        return self.get_string_from_file(self.path + "fruits.txt")


    def country(self):
        continent_category = chosen_category_continent.get()    #assigning the selected option in the country options menu

        if continent_category == "Asia":
            return self.get_string_from_file(self.path + "country.asia.txt")

        if continent_category == "Africa":
            return self.get_string_from_file(self.path + "country.africa.txt")

        if continent_category == "Europe":
            return self.get_string_from_file(self.path + "country.europe.txt")

        if continent_category == "North America":
            return self.get_string_from_file(self.path + "country.northAmerica.txt")

        if continent_category == "South America":
            return self.get_string_from_file(self.path + "country.southAmerica.txt")


if __name__ == '__main__':
    main()
