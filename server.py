# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:12:16 2019

@author: mohamed
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
    global current1
    global player1Current
    global conn
    global turn
    if(turn==1):
        r =random.randint(1,6)
        update_dice(r)
        if(r!=1):
            current1+=r
            sendData = str(r).encode('utf-8')
            conn.send(sendData)
            player1Current['text']=str(current1)
        else:
            turn=2
            sendData="turn".encode('utf-8')
            conn.send(sendData)
            player1Current['text']="0"
            toggleColors(player1Label,player2Label)
            current1=0

#function of hold
def hold_dice():
    global current1
    global score1
    global turn 
    global conn
    global player1Current
    global player1Score
    if(turn==1):
        turn=2
        score1+=current1
        sendDate="hold="+str(score1)
        sendDate=sendDate.encode('utf-8')
        conn.send(sendDate)
        player1Current['text']='0'
        player1Score['text']=str(score1)
        toggleColors(player1Label,player2Label)
        current1=0
        if(score1>=50):
                messagebox.showinfo("congratulation","you win")
                wind.destroy()
                sc.close()
        
        
wind = Tk();
wind.title('server')
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


# recieve thread function 
output[0]="turn"
def receive_thread(conn):
    global current2
    global score2
    global turn
    global player2Current
    global player2Score
    global current2
    global player2Current
    while True :
        output=conn.recv(255);
        output=output.decode('utf-8')
        output=output.split('=')
        if(output[0] =="turn"):
            current2=0
            player2Current['text']='0'
            toggleColors(player2Label,player1Label)
            turn=1
            update_dice(1)
        elif(output[0]=='hold'):
            turn=1
            score2=int(output[1])
            player2Score['text']=output[1]
            player2Current['text']='0'
            toggleColors(player2Label,player1Label)
            current2=0
            if(score2>=50):
                messagebox.showinfo("congratulation","player 2 win")
                wind.destroy()
                sc.close()
        else:           
            output=int(output[0])
            current2+=output
            player2Current['text']=str(current2)
            update_dice(output)
# socket prepare 
sc = socket(AF_INET,SOCK_STREAM)
host ="127.0.0.1"
port=9000
sc.bind((host,port))
sc.listen(1)
while True:
    conn,add=sc.accept()
    thread= Thread(target=receive_thread,args=(conn,))
    thread.start()
    wind.mainloop()
    