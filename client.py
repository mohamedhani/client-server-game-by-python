# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from tkinter import *
from tkinter import messagebox
from socket import *
from PIL import ImageTk, Image
from threading import Thread 
import random
# global variables
current1=0
current2=0
score1=0
score2=0
turn =1
def toggleColors(black,red):
    black["fg"]="black"
    red['fg']="red"
#function of update dice
def update_dice(number):
    global diceLabel
    imageTitle ="dice-"+str(number)+".png"
    img = ImageTk.PhotoImage(Image.open(imageTitle).resize((100,100),Image.ANTIALIAS))
    diceLabel.config(image=img)
    diceLabel.image=img
              
# function of generate dice 
def roll_dice():
    global current2
    global player2Current
    global sc
    global turn
   
    if(turn==2):
        r =random.randint(1,6)
        update_dice(r)
        if(r!=1):
            current2+=r    
            sendData = str(r).encode('utf-8')
            sc.send(sendData)
            player2Current['text']=str(current2)
        else:
            turn=1
            sendData = "turn".encode('utf-8')
            sc.send(sendData)
            player2Current['text']="0"
            current2=0
            toggleColors(player2Label,player1Label)
def hold_dice():
    global current2
    global score2
    global turn 
    global player2Score
    global player2Current
    global conn
    if(turn==2):
        turn=1
        score2+=current2
        sendDate="hold="+str(score2)
        sendDate=sendDate.encode('utf-8')
        sc.send(sendDate)
        current2=0
        toggleColors(player2Label,player1Label)
        player2Current['text']='0'
        player2Score['text']=str(score2)
        if(score2>=50):
                messagebox.showinfo("congratulation","you win")
                wind.destroy()
                sc.close()
        
      
wind = Tk();
wind.title('client')
wind.geometry("600x600")
#prepare player1 
player1Label = Label(wind,text="player 1",font=("Helvelt",'15'),fg="red")
player1Label.place(x=100,y=100)

player1Score =Label(wind,text="0",font=("Helvelt",'15')) 
player1Score.place(x=120,y=150)

Label(wind,text="current",font=("Helvelt",'15')).place(x=100,y=300)
player1Current=Label(wind,text="0",font=("Helvelt",'15'))
player1Current.place(x=120,y=350)

#prepare player 2 
player2Label = Label(wind,text="player 2",font=("Helvelt",'15'))
player2Label.place(x=450,y=100)

player2Score =Label(wind,text="0",font=("Helvelt",'15'))
player2Score.place(x=470,y=150)

Label(wind,text="current",font=("Helvelt",'15')).place(x=450,y=300)
player2Current=Label(wind,text="0",font=("Helvelt",'15'))
player2Current.place(x=470,y=350)
# prepare buttons
rollButton = Button(wind,text="Roll Dice",width=10,height=2,font=("Helvelt",'15'),command=roll_dice)
rollButton.place(x=270,y=400)
holdButton = Button(wind,text="Hold",width=10,height=2,font=("Helvelt",'15'),command=hold_dice)
holdButton.place(x=270,y=500)
#prepre dice image 

diceLabel = Label(wind)
diceLabel.place(x=250,y=120)

def receive_thread(sc):
    global current1
    global score
    global turn
    global player1Current
    global player1Score
    while True :
        output=sc.recv(255);
        output=output.decode('utf-8')
        print(output)
        output=output.split('=')
        print(output[0])
        if(output[0] =="turn"):
            current1=0
            toggleColors(player1Label,player2Label)
            player1Current['text']='0'
            turn=2
            update_dice(1)
        elif(output[0]=='hold'):
            turn=2
            score1=int(output[1])
            toggleColors(player1Label,player2Label)
            player1Score['text']=output[1]
            player1Current['text']='0'
            current1=0
            if(score1>=50):
                messagebox.showinfo("congratulation","player 1 win")
                wind.destroy()
                sc.close()
        else:
            output=int(output[0])
            update_dice(output)
            print(current1)
            current1=current1+output 
            player1Current['text']=int(current1)

#function of recive date thread

    
#socket prepare 
            
sc =socket(AF_INET,SOCK_STREAM)
host="127.0.0.1"
port=9000
sc.connect((host,port))
thread=Thread(target=receive_thread,args=(sc,))
thread.start()
wind.mainloop()