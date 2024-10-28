import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame,sys,time
pygame.init()
pygame.font.init()
win=pygame.display.set_mode((600,600))

#global vars
global smb #show message box
smb=0
Clock=pygame.time.Clock()
global gamestate
gamestate=1

class message:
    def __init__(self,text,x,y,fontsize):
        self.text=text
        self.y=y
        self.x=x
        self.font=pygame.font.SysFont(None,fontsize)
        self.format_text()

    def format_text(self):
        text=self.text
        a=""
        self.text=[]
        for i in range(len(text)):
            if text[i]=="~":
                self.text.append(a)
                a=""
            else:
                a+=text[i]
        self.text.append(a)
    
    def draw(self,win):
        line=0
        for i in self.text:
            text=self.font.render(f"{i}",True,(0,0,0))
            win.blit(text,(self.x,self.y+(line*10)))
            line+=1

class button:
    def __init__(self,text,x,y,width,height,color,border=False,fontsize=20,enable=True):
        self.text=text
        self.y=y
        self.x=x
        self.width=width
        self.height=height
        self.color=color
        self.border=border
        self.font=pygame.font.SysFont(None,fontsize)
        self.clicked=False
        self.enable=enable
    
    def draw(self,win):
        if self.border==False:
            a=0
        else:
            a=1
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height),width=a)
        text=self.font.render(f"{self.text}",True,(0,0,0))
        win.blit(text,(self.x+10,self.y+10))
    
    def click(self,mx,my):
        if self.enable==True:
            if not self.clicked:
                if mx>self.x and mx<self.x+self.width:
                    if my>self.y and my<self.y+self.height:
                        self.clicked=True
                        return True
        return False
    def rclick(self):
        self.clicked=False

def messagebox():
    global smd
    if smb==1:
        pygame.draw.rect(win,(255,255,255),(10,400,580,190))

class document:
    def __init__(self,x,y,width,height,text,color,ispic=False,pic=None,fontsize=20,lineheight=20):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
        self.color=color
        self.ispic=ispic
        self.pic=pic
        self.font=pygame.font.SysFont(None,fontsize)
        self.format_text()
        self.enable=True
        self.lineheight=lineheight
        

    def format_text(self):
        text=self.text
        a=""
        self.text=[]
        for i in range(len(text)):
            if text[i]=="~":
                self.text.append(a)
                a=""
            else:
                a+=text[i]
        self.text.append(a)

    
    def draw(self,win):
        if self.ispic==True:
            self.pic=pygame.transform.scale(self.pic,(self.width,self.height))
            win.blit(self.pic,(self.x,self.y))
        else:
            pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
            line=0
            for i in self.text:
                text=self.font.render(f"{i}",True,(0,0,0))
                win.blit(text,(self.x+10,self.y+(line*self.lineheight)))
                line+=1
    
    def dragable(self,mx,my):
        if mx>self.x and mx<self.x+self.width and  my>self.y and my<self.y+self.height:
            while pygame.mouse.get_pressed()[0]==True:
                self.x=mx
                self.y=my
                mx,my=pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                win.fill((0,0,0))
                if gamestate==1:
                    lookroom()
                elif gamestate==2:
                    lookdesk()
                messagebox()
                pygame.display.update()
                keys=pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
            


#acual game
#sam pics
sams=pygame.image.load("samStrate.png")
samr=pygame.image.load("samright.png")
global curent_sam
curent_sam=sams
global crecord
crecord=pygame.image.load("Sam_record.png")

global diolog_index
diolog_index=0
global caseOneDocs
#case one vars
callButtons=[button("",550,110,20,20,(200,200,10))]
callButtonLabels=[message("Press To Start Next Sestion",430,140,15)]
caseOneDocs=[document(50,105,150,190,"Genarel Infomation~Name:Sam Yells~Age:42~Ocupation:None",(225,225,200))]
global c1s
c1s=0
tree=0
qc=0
global ending
ending=0
hbuttons=[button("Are you ok?",50,450,100,50,(255,255,255),border=True,fontsize=15),
button("(ingnor it)",50,500,100,50,(255,255,255),border=True,fontsize=15),]
#md 0=question 1 1=q2 2=q3 3=q4
samDialog=[message("Hello Sam",20,410,20),message("Sam:Good",20,410,20),message("Sam:Im a Astronaut",20,410,20),
message("Sam:Just my mom",20,410,20),message("Sam:My freinds say im a bit paranoid",20,410,20),message("Sam:Not very",20,410,20),message("Sam:”i grew potatoes when i was younger",20,410,20),
message("Sam(aside):What",20,410,20),message("Sam(aside):No",20,410,20),message("Sam(aside):Shut up",20,410,20),message("Sam:Sorry i have to go",20,410,20),]
#mdb 0,1=question 1
samDialogButtons=[button("How are you today?",50,450,100,50,(255,255,255),border=True,fontsize=15),
button("What do you do for work",200,450,100,50,(255,255,255),border=True,fontsize=15),button("Do you have any family?",200,500,100,50,(255,255,255),border=True,fontsize=15),
button("What brings you to the psychologist?",350,450,200,50,(255,255,255),border=True,fontsize=15),button("How close are you with your mom?",300,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),
button("Where are you from",50,500,100,50,(255,255,255),border=True,fontsize=15)
]

samDialog2=[message("Hello Sam again Sam",20,410,20),message("Sam:Good.",20,410,20),message("Sam:I heard him say he was gonna hurt me.",20,410,20),message("Sam:yes he was talking to the guy next to him saying he was gona hurt me.",20,410,20),
            message("Sam:Yes im 100% sure it was that man.",20,410,20),message("Sam:No i've neverseen him before",20,410,20),message("Sam:I saw him and he was coming at me i knew he was gona hurt me",20,410,20),message("Sam:Becuse i heard him saying something and he looked like he was about to attack me",20,410,20),message("Sam:Yeah he looked like has was about to atack me. I think.",20,410,20),
            message("Sam:Yeah I heard him talking about attacking me. I think",20,410,20),message("Sam:Uh Uh, well to be honsest with you theirs been times when i saw or hear somthing~that wasent their",20,410,20),message("Sam:Yeah i geuss you could call it that",20,410,20),message("Sam:Just my mom. But she told me never to talk to anyone about them",20,410,20),message("Sam:She told me that pepole would hate me if i told them about them",20,410,20),message("Sam:sinces my early 20s",20,410,20),
            message("Sam:No",20,410,20),message("you:Well with your symptoms Sam, I would diagnose you with schizophrenia",20,410,20),]
#0 #1->2->3 #
   #1->4
samDialogButtons2=[button("How are you today?",50,450,100,50,(255,255,255),border=True,fontsize=15),button("Why did you attack the old man?",200,450,100,50,(255,255,255),border=True,fontsize=15),
                   button("You heard him?",350,450,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("Are you sure it was him talking?",50,550,100,50,(255,255,255),border=True,fontsize=15,enable=False),
                   button("Had you ever seen him before?",350,550,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("Can you tell me what happened when you were in collage?",200,500,100,50,(255,255,255),border=True,fontsize=15),button("Why did you think that?",100,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("He looked like he was about to attack you?",175,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),
                   button("You heard him saying somthing?",400,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("You think?",100,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("Hallucination?",200,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("Have you ever told anyone about what you see and hear?",100,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("Why did she say that?",200,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),button("How long have you delt with these hallucination?",100,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),
                   button("Have you ever been checked by a doctor or digonosed with anything?",200,500,100,50,(255,255,255),border=True,fontsize=15,enable=False),]

def caseone():
    global c1s
    global gamestate
    global smb
    callButtons[0].enable=True
    callButtonLabels[0].draw(win)
    callButtons[0].draw(win)
    if c1s==1:
        gamestate=1
        callButtons[0].enable=False
        deskbutton.enable=True
        smb=1
    if c1s==2:
        gamestate=1
        callButtons[0].enable=False
        deskbutton.enable=True
        smb=1

def fristh():
    global c1s
    global diolog_index
    global curent_sam
    global gamestate
    global caseOneDocs
    global smb
    global crecord
    a=[]
    b=diolog_index
    for i in samDialogButtons:
        if i.enable==True:
            a.append(samDialogButtons.index(i))
            i.enable=False
    curent_sam=samr
    c=0

    while True:
        mx,my=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        if c<3:
            lookroom()
            messagebox()
            diolog_index=7+c
            curent_diogog()
            pygame.display.update()
            time.sleep(1)
            c+=1
        else:
            messagebox()
            curent_sam=sams
            for i in hbuttons:
                i.draw(win)
            pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                if hbuttons[0].click(mx,my):
                    lookroom()
                    messagebox()
                    message("Sam:Yeah,yeah sorry.",20,410,20).draw(win)
                    pygame.display.update()
                    time.sleep(2)
                    break
                
                elif hbuttons[1].click(mx,my):
                    lookroom()
                    messagebox()
                    message("Sam:",20,410,20).draw(win)
                    pygame.display.update()
                    time.sleep(2)
                    break
    diolog_index=10
    
    caseOneDocs.append(document(210,110,150,190,"",(0,0,0),ispic=True,pic=crecord))
    caseOneDocs.append(document(370,110,150,190,"Witness report~~Perptrator Name:Sam Yeller~Date:25 /06 /1991~location:Green Wall Collage~~Report:Mike Sting was walking~down the hallway of his collage.~suddenly as he passed Sam Yells he~was attacked unpromoted by Sam.~Sam was eventually thrown~off of Mike and Mike was taken to~the local hospital lucky unharmed.",(225,225,200),fontsize=12,lineheight=10))
    caseOneDocs.append(document(50,300,150,190,"Witness report~~Perptrator Name:Sam Yeller~Date:08 /09 /2008~location:Bedcon city bus #832~~Report:Mat Pointer, an 87 year old~mute man, was sitting down on the~bus he takes home every day.~Suddenly he was attacked by Sam~Yells. lucky a person sitting next~to Mat held Sam back and Sam was~then removed from the buss and~brought to the local police station.",(225,225,200),fontsize=12,lineheight=10))
    smb=1
    lookroom()
    c1s=1.5
    messagebox()
    message("Sam:Sorry i have to go",20,410,20).draw(win)
    pygame.display.update()
    smb=0
    time.sleep(2)
   


#lookroom vars
deskbutton=button("See Desk",250,537.5,100,25,(200,200,200),True)
def lookroom():
    global c1s
    deskbutton.enable=True
    roombutton.enable=False
    pygame.draw.rect(win,(150,50,0),(0,0,600,600))
    pygame.draw.rect(win,(100,75,50),(0,300,600,300))
    pygame.draw.rect(win,(100,50,0),(250,50,100,250))
    deskbutton.draw(win)
    if c1s==1:

        win.blit(curent_sam,(200,200))
    if c1s==2:
        win.blit(curent_sam,(200,200))


def curent_diogog():
    global c1s
    if c1s==1:
        if tree==0:
            samDialog[diolog_index].draw(win)
            for i in samDialogButtons:
                if i.enable:
                    i.draw(win)
    if c1s==2:
        samDialog2[diolog_index].draw(win)
        for i in samDialogButtons2:
            if i.enable:
                i.draw(win)



roombutton=button("See Room",250,50,100,25,(200,200,200),True)
def lookdesk():
    global c1s
    deskbutton.enable=False
    roombutton.enable=True
    pygame.draw.rect(win,(100,75,50),(0,0,600,600))
    pygame.draw.rect(win,(100,50,0),(20,100,560,400))
    caseone()
    for i in caseOneDocs:
        i.draw(win)

    roombutton.draw(win)

def dionose():
    time.sleep(2)
    global ending
    a=button("Treat",100,450,100,50,(255,225,225))
    b=button("Leave be",350,450,100,50,(255,225,225))
    while True:
        mx,my=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        win.fill((0,0,0))
        lookroom()
        win.blit(curent_sam,(200,200))
        messagebox()
        message("{Should you treat Sam for schizophrenia}",20,410,20).draw(win)
        a.draw(win)
        b.draw(win)
        pygame.display.update()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
        if pygame.mouse.get_pressed()[0]:
            if a.click(mx,my):
                a.enable=False
                ending=1
                print(ending)
                win.fill((0,0,0))
                lookroom()
                win.blit(curent_sam,(200,200))
                messagebox()
                message("you:Ok Sam here is a prescription for some Antipsychotic drugs. Unfortunately that's all~the time i have for you today so i will see you next session",20,410,20).draw(win)
                pygame.display.update()
                time.sleep(2)
                return
        
            elif b.click(mx,my):
                b.enable=False
                ending=2
                print(ending)
                win.fill((0,0,0))
                lookroom()
                win.blit(curent_sam,(200,200))
                messagebox()
                message("you:Ok Sam we made some great progress today, Unfortunately that's all the time i have for~you today so i will see you next session",20,410,20).draw(win)
                pygame.display.update()
                time.sleep(2)
                return


        Clock.tick(30)

while True:
    mx,my=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    win.fill((0,0,0))
    if ending==0:
        if gamestate==1:
            lookroom()
            
        elif gamestate==2:
            lookdesk()
        messagebox()
        curent_diogog()
        pygame.display.update()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
        if pygame.mouse.get_pressed()[0]:
            for i in caseOneDocs:
                    i.dragable(mx,my)
            if deskbutton.click(mx,my):
                gamestate=2
            if roombutton.click(mx,my):
                gamestate=1
            if callButtons[0].click(mx,my):
                if c1s<1:
                    c1s=1
                elif c1s>1:
                    diolog_index=0
                    c1s=2
            if c1s==1 and tree==0:
                if samDialogButtons[0].click(mx,my):
                    samDialogButtons[0].enable=False
                    diolog_index=1
                    qc+=1
                elif samDialogButtons[1].click(mx,my):
                    samDialogButtons[1].enable=False
                    diolog_index=2
                    qc+=1
                elif samDialogButtons[2].click(mx,my):
                    samDialogButtons[2].enable=False
                    diolog_index=3
                    qc+=1
                    samDialogButtons[4].enable=True
                elif samDialogButtons[3].click(mx,my):
                    samDialogButtons[3].enable=False
                    diolog_index=4
                    qc+=1
                elif samDialogButtons[4].click(mx,my):
                    samDialogButtons[4].enable=False
                    diolog_index=5
                    qc+=1
                elif samDialogButtons[5].click(mx,my):
                    samDialogButtons[5].enable=False
                    diolog_index=6
                    qc+=1
            elif c1s==2 and tree==0:
                if samDialogButtons2[0].click(mx,my):
                    samDialogButtons2[0].enable=False
                    diolog_index=1
                    qc+=1
                elif samDialogButtons2[1].click(mx,my):
                    samDialogButtons2[1].enable=False
                    diolog_index=2
                    qc+=1
                    samDialogButtons2[2].enable=True
                    samDialogButtons2[4].enable=True
                elif samDialogButtons2[2].click(mx,my):
                    samDialogButtons2[2].enable=False
                    diolog_index=3
                    qc+=1
                    samDialogButtons2[3].enable=True
                elif samDialogButtons2[3].click(mx,my):
                    samDialogButtons2[3].enable=False
                    diolog_index=4
                    qc+=1
                elif samDialogButtons2[4].click(mx,my):
                    samDialogButtons2[4].enable=False
                    diolog_index=5
                    qc+=1
                elif samDialogButtons2[5].click(mx,my):
                    samDialogButtons2[5].enable=False
                    diolog_index=6
                    qc+=1
                    samDialogButtons2[6].enable=True
                elif samDialogButtons2[6].click(mx,my):
                    samDialogButtons2[6].enable=False
                    diolog_index=7
                    samDialogButtons2[7].enable=True
                    samDialogButtons2[8].enable=True
                    qc+=1
                elif samDialogButtons2[7].click(mx,my):
                    samDialogButtons2[7].enable=False
                    diolog_index=8
                    samDialogButtons2[9].enable=True
                    samDialogButtons2[8].enable=False
                    qc+=1
                elif samDialogButtons2[8].click(mx,my):
                    samDialogButtons2[8].enable=False
                    samDialogButtons2[7].enable=False
                    diolog_index=9
                    samDialogButtons2[9].enable=True
                    qc+=1
                elif samDialogButtons2[9].click(mx,my):
                    samDialogButtons2[9].enable=False
                    diolog_index=10
                    
                    samDialogButtons2[10].enable=True
                    qc+=1
                elif samDialogButtons2[10].click(mx,my):
                    samDialogButtons2[10].enable=False
                    diolog_index=11
                    
                    samDialogButtons2[11].enable=True
                    qc+=1
                elif samDialogButtons2[11].click(mx,my):
                    samDialogButtons2[11].enable=False
                    diolog_index=12
                    
                    samDialogButtons2[12].enable=True
                    qc+=1
                elif samDialogButtons2[12].click(mx,my):
                    samDialogButtons2[12].enable=False
                    diolog_index=13
                    
                    samDialogButtons2[13].enable=True
                    qc+=1
                elif samDialogButtons2[13].click(mx,my):
                    samDialogButtons2[13].enable=False
                    diolog_index=14
                    
                    samDialogButtons2[14].enable=True
                    qc+=1
                
                elif samDialogButtons2[14].click(mx,my):
                    samDialogButtons2[14].enable=False
                    diolog_index=15
                    messagebox()
                    curent_diogog()
                    pygame.display.update()
                    time.sleep(2)
                    diolog_index=16
                    messagebox()
                    curent_diogog()
                    pygame.display.update()
                    time.sleep(2)
                    c1s=2.5
                    dionose()

                    
        else:
            deskbutton.rclick()
            roombutton.rclick()
            callButtons[0].rclick()
        
        if qc==4 and c1s==1:
            messagebox()
            curent_diogog()
            pygame.display.update()
            time.sleep(2)
            fristh()
            qc+=1

        
    elif ending==1:
        lookroom()
        messagebox()
        message("{One week later}",20,410,20).draw(win)
        pygame.display.update()
        time.sleep(3)
        win.blit(curent_sam,(200,200))
        messagebox()
        message("Sam:hey i just wanted you to know that I'm done with theropy and all better now",20,410,20).draw(win)
        pygame.display.update()
        time.sleep(5)
        win.fill((0,255,0))
        message("You win",20,410,30).draw(win)
        pygame.display.update()
        time.sleep(10)
        break

    elif ending==2:
        lookroom()
        messagebox()
        message("{One week later}",20,410,20).draw(win)
        pygame.display.update()
        time.sleep(3)
        win.blit(curent_sam,(200,200))
        messagebox()
        message("Sam:Help, help please their following me, their all gona get me.~Unless are you gona hurt me too?",20,410,20).draw(win)
        pygame.display.update()
        time.sleep(5)
        win.fill((255,0,0))
        message("You Lose",20,410,30).draw(win)
        pygame.display.update()
        time.sleep(10)
        break
    Clock.tick(30)