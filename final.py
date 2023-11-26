
def main():
    import back   #back.py is imorted, its a module 
    import random as r

    main_font = "Times New Roman"    

    def copycat(player_response_list,*useless_stuff):
        # Mimics the opponent's last move. If no past move, defaults to cooperating.
        if len(player_response_list):
            return player_response_list[len(player_response_list)-1] #retrive last ite, 
        else:
            return 1 #return to original state

    def all_cooperate(*useless_stuff):  # Always cooperates, regardless of the opponent's actions.
        return 1

    def all_cheat(*useless_stuff):  # Always cheat, regardless of the opponent's actions.
        return 0

    def grudger(player_response_list,*useless_stuff): # Starts by cooperating, but if the opponent ever cheats, it will cheat forever.
        return int(not (0 in player_response_list))

    def detective(player_response_list,*useless_stuff): # Starts by cooperating, then plays the following sequence: Cooperate, Cheat, Cooperate, Cooperate. If the opponent ever cheats back, it will play like a copycat. If the opponent never cheats back, it will play like an all-cheat.
        # A complex strategy: starts with a specific sequence of moves and then
    # decides based on the opponent's past actions.
        l = len(player_response_list) 
        if l in [0,2,3]: 
            return 1
        elif l==1:
            return 0
        else:
            # Mimics last move if the opponent has cheated after the first two moves
            if 0 in player_response_list[2:]:
                return player_response_list[l-1]
            else:
                return 0

    def copykitten(player_response_list,*useless_stuff): # Similar to copycat but forgives a single cheating move by the opponent.
        if len(player_response_list) < 2:
            return 1
        return (player_response_list[len(player_response_list)-1] or player_response_list[len(player_response_list)-2])

    def simpleton(player_response_list,bot_response_list,*useless_stuff):
        # Cooperates if both players did the same thing last time, else cheats.
    # Requires knowledge of its own past moves as well.
        l = len(player_response_list)
        if l:
            return int(not (player_response_list[l-1]^bot_response_list[l-1]))
        else:
            return 1

    def rando(*useless_stuff):  # Chooses randomly between cooperating and cheating.
        return r.choice([0,1])

    char_fun_dict = {"copycat":copycat,"all cooperate":all_cooperate,"all cheat":all_cheat,"grudger":grudger,"detective":detective,"copykitten":copykitten,"simpleton":simpleton,"random":rando}
    char_resp_list = [copycat,all_cooperate,all_cheat,grudger,detective,copykitten,simpleton,rando]
    character_color = {"copycat":"lightslateblue","all cooperate":"hotpink","all cheat":"red2","grudger":"yellow2","detective":"green","copykitten":"deeppink1","simpleton":"black","random":"brown"}
    character_names = list(character_color.keys())
    imgloader = {"copycat":"char1","all cooperate":"char2","all cheat":"char3","grudger":"char4","detective":"char5","copykitten":"char6","simpleton":"char7","random":"char8"}

    def computescores(playlist,botlist,givecoin=1,getcoin=3): 
        scores = [0,0]
        for i in range(len(playlist)):
            if playlist[i]:
                scores[1]+=getcoin
                scores[0]-=givecoin
            if botlist[i]:
                scores[0]+=getcoin
                scores[1]-=givecoin
        return scores
    
    class GodSet: # A class that plays the game perfectly, and can be used to find the best move for a given situation.
        def __init__(self,botname,givecoin=1,getcoin=3,maxsteps=8): # The botname is the name of the bot that the GodSet is playing against.
            self.botfunc = char_fun_dict[botname]
            self.givecoin = givecoin
            self.getcoin = getcoin
            self.maxperstep = givecoin+getcoin
            self.maxsteps = maxsteps
            self.godplay = []
            self.botplay = []
            self.currentbestmove = 1
            self.currentmove = 1
        def godstep(self): # Plays a single round of the game, and returns the bot's move.
            self.maxmax = -self.maxperstep*self.maxsteps
            self.minmin = self.maxperstep*self.maxsteps
            def descend(step):
                gsc,bsc = computescores(self.godplay,self.botplay,self.givecoin,self.getcoin)
                if step==0:
                    if gsc>self.maxmax:
                        self.maxmax = gsc
                        self.minmin = bsc
                        self.currentbestmove = self.currentmove
                    elif gsc==self.maxmax and bsc<self.minmin:
                        print("this ran now")
                        self.minmin = bsc
                        self.currentbestmove = self.currentmove
                    return
                elif step*self.maxperstep<self.maxmax-gsc:  #Pruning
                    return
                self.botplay.append(self.botfunc(self.godplay,self.botplay))
                self.godplay.append(1)
                if step==self.maxsteps:
                    self.currentmove=1
                descend(step-1)
                self.godplay[-1]=0
                if step==self.maxsteps:
                    self.currentmove=0
                descend(step-1)
                self.godplay = self.godplay[:-1]
                self.botplay = self.botplay[:-1]
            descend(self.maxsteps)
            self.botplay.append(self.botfunc(self.godplay,self.botplay))
            self.godplay.append(self.currentbestmove)
            return self.currentbestmove

    def tourney(bot1,bot2,rounds,givecoins=1,getcoins=3): # Plays a tournament between two bots, and returns the scores and the list of moves.
        scores = [0,0]
        resplists = [[],[]]
        for i in range(rounds):
            r1 = char_fun_dict[bot1](resplists[1],resplists[0])
            r2 = char_fun_dict[bot2](resplists[0],resplists[1])
            resplists[0].append(r1)
            resplists[1].append(r2)
            if r1:
                scores[0]-=givecoins
                scores[1]+=getcoins
            if r2:
                scores[1]-=givecoins
                scores[0]+=getcoins
        return (scores,resplists)

    def multitourney(charlist,err=0,resplist=[],givecoins=1,getcoins=3): # Plays a tournament between multiple bots, and returns the scores and the list of moves.
        n=len(charlist)
        scorelist = [*[0]*n]
        if resplist==[]:
            rxc = [[[[],[]] for j in range(i+1,n)] for i in range(n)][:n-1]
            resplist.extend(rxc)
        for i in range(n-1):
            for j in range(i+1,n):
                r1 = errify(char_fun_dict[charlist[i]](resplist[j-i-1][i][1],resplist[j-i-1][i][0]),err)
                r2 = errify(char_fun_dict[charlist[j]](resplist[j-i-1][i][0],resplist[j-i-1][i][1]),err)
                if r1:
                    scorelist[i]-=givecoins
                    scorelist[j]+=getcoins
                if r2:
                    scorelist[j]-=givecoins
                    scorelist[i]+=getcoins
                resplist[j-i-1][i][0].append(r1)
                resplist[j-i-1][i][1].append(r2)
        return scorelist,resplist

    def errify(ans,percent): # Returns a random answer with a given probability.
        x = r.randint(1,100)
        if x<=percent:
            return 1-ans
        return ans

    def add_index(L,backbutton=0): # Adds the index page to a given section.
        L.flush()
        L.add_label("COPYCAT - Hello! I start with Cooperate,",character_color["copycat"],main_font,24,(180,50),0)
        L.add_label("and afterwards, I just copy whatever you",character_color["copycat"],main_font,24,(180,50),1.2)
        L.add_label("did in the last round. Meow",character_color["copycat"],main_font,24,(180,50),1.2)
        L.add_player("char1",(100,50))
        L.add_label("ALWAYS COOPERATE - Let's",character_color["all cooperate"],main_font,24,(780,50),0)
        L.add_label("be best friends! <3",character_color["all cooperate"],main_font,24,(780,50),1.2)
        L.add_player("char2",(700,50))
        L.add_label("ALWAYS CHEAT -",character_color["all cheat"],main_font,24,(180,200),0)
        L.add_label("the strong shall",character_color["all cheat"],main_font,24,(180,200),1.2)
        L.add_label("eat the weak",character_color["all cheat"],main_font,24,(180,200),1.2)
        L.add_player("char3",(100,200))
        L.add_label("GRUDGER - Listen, pardner. I'll start cooperatin', and keep",character_color["grudger"],main_font,24,(480,200),0)
        L.add_label("cooperatin', but if y'all ever cheat me, I'LL CHEAT YOU BACK",character_color["grudger"],main_font,24,(480,200),1.2)
        L.add_label("'TIL THE END OF TARNATION.",character_color["grudger"],main_font,24,(480,200),1.2)
        L.add_player("char4",(400,200))
        L.add_label("DETECTIVE - First: I analyze you. I start: Cooperate, Cheat, Cooperate, Cooperate. If you",character_color["detective"],main_font,24,(180,350),0)
        L.add_label("cheat back, I'll act like Copycat. If you never cheat back, I'll act like Always Cheat, to",character_color["detective"],main_font,24,(180,350),1.2)
        L.add_label("exploit you. Elementary, my dear Watson.",character_color["detective"],main_font,24,(180,350),1.2)
        L.add_player("char5",(100,350))
        if backbutton:
            L.add_button("<---","black","consolas",24,(1050,500,100,50),"white","yellow","green","black",[[L.flush],[L4init],[s.switch_section,L4,L4]])

    L0 = back.Section((1200,600),'white')
    L1 = back.Section((1200,600),'white',"Introduction")
    L2 = back.Section((1200,600),'white',"One Game")
    L3 = back.Section((1200,600),'white',"Repeated Game")
    L4 = back.Section((1200,600),'white',"Tournament")
    L5 = back.Section((1200,600),'white',"Making Mistaeks")
    L6 = back.Section((1200,600),'white',"Sandbox Mode")
    L7 = back.Section((1200,600),'white',"God Player")
    L8 = back.Section((1200,600),'white',"Conclusion")

    def L0init(): # Adds the index page to the main section.
        L0.flush()
        L0.add_label("The",'black','bahnschrift',90,(600,50),-2)
        L0.add_label("Evolution",'black','bahnschrift',90,(600,150),-2)
        L0.add_label("of",'black','bahnschrift',90,(600,250),-2)
        L0.add_label("Trust",'black','bahnschrift',90,(600,350),-2)
        L0.add_button("Play!",'black','bahnschrift',24,(500,500,200,50),"white","yellow","green","black",[[L1init],[s.switch_section,L0,L1]])

    def L1init(): # Adds the introduction page to the main section.
        L1.flush()
        L1.add_label("During World War I, peace broke out.","black",main_font,24,(100,50),0)
        L1.add_label("It was Christmas 1914 on the Western Front. Despite strict orders not to chillax with the ","black",main_font,24,(100,0),2,background_color="white")
        L1.add_label("enemy, British and German soldiers left their trenches, crossed No Man's Land, and ","black",main_font,24,(100,0),1.2)
        L1.add_label("gathered to bury their dead, exchange gifts, and play games.","black",main_font,24,(100,0),1.2)
        L1.add_label("Meanwhile: it's 2022, the West has been at peace for decades, and wow, we suck at trust. ","black",main_font,24,(100,0),2)
        L1.add_label("Surveys show that, over the past forty years, fewer and fewer people say they trust each ","black",main_font,24,(100,0),1.2)
        L1.add_label("other. So here's our puzzle:","black",main_font,24,(100,0),1.2)
        L1.add_label("Why, even in peacetime, do friends become enemies?","green",main_font,24,(100,0),2,italic=True)
        L1.add_label("And why, even in wartime, do enemies become friends?","green",main_font,24,(100,0),1.2,italic=True)
        L1.add_label("I think ","black",main_font,24,(100,0),2)
        L1.add_label("game theory","red",main_font,24,(100,0))
        L1.add_label(" can help explain our epidemic of distrust - and how we can fix it! ","black",main_font,24,(100,0))
        L1.add_label("So, to understand all this...","black",main_font,24,(100,0),1.2)
        L1.add_button("...let's play a game.","black",main_font,24,(450,500,300,50),"white","yellow","green","black",[[L2init],[s.switch_section,L1,L2]])

    def L2init(): # Adds the first game page to the main section.
        L2.flush()
        L2.add_label("THE GAME OF TRUST","black",main_font,32,(600,50),-2)
        L2.add_label("You have one choice. In front of you is a machine: if you put a coin in the machine, the other","black",main_font,24,(100,100),0)
        L2.add_label("player gets three coins - and vice versa. You both can either choose to COOPERATE (put in coin),","black",main_font,24,(100,100),1.2)
        L2.add_label("or CHEAT (don't put in coin).","black",main_font,24,(100,100),1.2)
        L2.add_label("you","black",main_font,18,(280,220),-2)
        L2.add_label("other player","black",main_font,18,(890,220),-2)
        L2.config_machine((475,200,250,200),0,0,0,0)
        L2.add_player("char0",(280,330))
        L2.add_player("char1",(900,330),1)
        L2.add_label("Let's say the other player cheats, and doesn't put in a coin.","black",main_font,20,(600,430),-2)
        L2.add_label("What should you do?","black",main_font,20,(600,460),-2,italic=1)
        L2v = back.TempValues()
        L2v.stepnumber = 0
        def L2resp(resp):
            if L2v.stepnumber==0:
                L2.config_machine((475,200,250,200),0,1,0,1)
                L2v.stepnumber+=1
                L2.labels = []
                if resp:
                    L2.add_label("Alas, turning the other cheek just gets you slapped!","black",main_font,24,(600,70),-2)
                else:
                    L2.add_label("Exactly! Why let that moocher mooch off of you?","black",main_font,24,(600,70),-2)
                L2.add_label("If you cooperate & they cheat, you lose a coin while they gain three (score: -1 vs +3).","black",main_font,24,(600,100),-2)
                L2.add_label("However, if you both cheat, neither of you gain or lose anything (score: 0 vs 0).","black",main_font,24,(600,130),-2)
                L2.add_label("Therefore: you should CHEAT.","black",main_font,24,(600,160),-2,bold=1)
                L2.add_label("But let's say the other player cooperates, and puts in a coin.","black",main_font,20,(600,430),-2)
                L2.add_label("What should you do now?","black",main_font,20,(600,460),-2,italic=1)
            elif L2v.stepnumber==1:
                L2.config_machine((475,200,250,200),1,1,1,1)
                L2.labels = []
                if resp:
                    L2.add_label("Sure, seems like the right thing to do... OR IS IT??","black",main_font,24,(600,70),-2)
                else:
                    L2.add_label("Wow, that's mean... and also the correct answer!","black",main_font,24,(600,70),-2)
                L2.add_label("Because if you both cooperate, you both give up a coin to gain three (score: +2 vs +2).","black",main_font,24,(600,100),-2)
                L2.add_label("But if you cheat & they cooperate, you gain three coins at their cost of one (score: +3 vs -1).","black",main_font,24,(600,130),-2)
                L2.add_label('Therefore: you "should" still CHEAT.',"black",main_font,24,(600,160),-2,bold=1)
                L2.add_label("And that's our dilemma. Trust is nice, but it can let others take advantage of you - or shoot you as you come","black",main_font,20,(100,430),0)
                L2.add_label("unarmed out of a trench. Sometimes, distrust is rational! But now, what happens if we play this game...","black",main_font,20,(100,460),1.5)
                L2.buttons = []
                L2.add_button("...more than once?","black",main_font,24,(450,500,300,50),"white","yellow","green","black",[[L3init],[s.switch_section,L2,L3]])
        L2.add_button("COOPERATE","black",main_font,24,(350,500,200,50),"white","yellow","green","black",[[L2resp,1],[s.switch_section,L2,L2]])
        L2.add_button("CHEAT","black",main_font,24,(650,500,200,50),"white","yellow","green","black",[[L2resp,0],[s.switch_section,L2,L2]])

    def L3init(): # Adds the repeated game page to the main section.
        L3.flush()
        L3.add_label("Now, let's play for real. You'll be playing against 5 different opponents,","black",main_font,24,(600,40),-2)
        L3.add_label('each with their own game "strategy". With each opponent, you\'ll play',"black",main_font,24,(600,70),-2)
        L3.add_label("anywhere between 3 to 7 rounds (You won't know in advance when the","black",main_font,24,(600,100),-2)
        L3.add_label("last round is). Can you trust them? Or rather... can they trust you?","black",main_font,24,(600,130),-2)
        L3.add_label("Pick your first, real move.","black",main_font,20,(600,430),-2)
        L3.add_label("Choose wisely.","black",main_font,20,(600,460),-2,bold=1)
        L3.config_machine((475,200,250,200),0,0,0,0,1,1,1,1)
        L3.add_player("char1",(860,330),1)
        L3.add_player("char0",(280,330))
        L3v = back.TempValues()
        L3v.stepnumber = 0
        L3v.character = 0
        L3v.number_of_rounds = [5,4,4,5,7]
        L3v.current_prl = []
        L3v.current_brl = []
        L3v.current_score = 0
        L3v.step_score = [0,0]
        def L3index(): # This function is called when the player clicks the "Let's find out!" button.
            L3.flush()
            L3.add_label("COPYCAT - Hello! I start with Cooperate,",character_color["copycat"],main_font,24,(180,50),0)
            L3.add_label("and afterwards, I just copy whatever you",character_color["copycat"],main_font,24,(180,50),1.2)
            L3.add_label("did in the last round. Meow",character_color["copycat"],main_font,24,(180,50),1.2)
            L3.add_player("char1",(100,50))
            L3.add_label("ALWAYS COOPERATE - Let's",character_color["all cooperate"],main_font,24,(780,50),0)
            L3.add_label("be best friends! <3",character_color["all cooperate"],main_font,24,(780,50),1.2)
            L3.add_player("char2",(700,50))
            L3.add_label("ALWAYS CHEAT -",character_color["all cheat"],main_font,24,(180,200),0)
            L3.add_label("the strong shall",character_color["all cheat"],main_font,24,(180,200),1.2)
            L3.add_label("eat the weak",character_color["all cheat"],main_font,24,(180,200),1.2)
            L3.add_player("char3",(100,200))
            L3.add_label("GRUDGER - Listen, pardner. I'll start cooperatin', and keep",character_color["grudger"],main_font,24,(480,200),0)
            L3.add_label("cooperatin', but if y'all ever cheat me, I'LL CHEAT YOU BACK",character_color["grudger"],main_font,24,(480,200),1.2)
            L3.add_label("'TIL THE END OF TARNATION.",character_color["grudger"],main_font,24,(480,200),1.2)
            L3.add_player("char4",(400,200))
            L3.add_label("DETECTIVE - First: I analyze you. I start: Cooperate, Cheat, Cooperate, Cooperate. If you",character_color["detective"],main_font,24,(180,350),0)
            L3.add_label("cheat back, I'll act like Copycat. If you never cheat back, I'll act like Always Cheat, to",character_color["detective"],main_font,24,(180,350),1.2)
            L3.add_label("exploit you. Elementary, my dear Watson.",character_color["detective"],main_font,24,(180,350),1.2)
            L3.add_player("char5",(100,350))
            L3.add_label("Now, what if these characters were to play...","black",main_font,24,(600,450),-2) 
            L3.add_button("...against each other?","black",main_font,24,(400,500,400,50),"white","yellow","green","black",[[L4init],[s.switch_section,L3,L4]])
        def L3resp(resp): # This function is called when the player makes a move.
            botresp = char_resp_list[L3v.character](L3v.current_prl,L3v.current_brl)
            L3v.current_brl.append(botresp)
            L3v.current_prl.append(resp)
            lac = [0,0,0,0]
            if botresp and resp: # If both players cooperate, both gain 3 coins.
                lac[2]=1
                L3v.step_score[0]+=2
                L3v.current_score+=2
                L3v.step_score[1]+=2
            elif botresp and not resp:
                lac[1]=1
                L3v.step_score[0]+=3
                L3v.current_score+=3
                L3v.step_score[1]-=1
            elif resp and not botresp:
                lac[0]=1
                L3v.step_score[0]-=1
                L3v.current_score-=1
                L3v.step_score[1]+=3
            else:
                lac[3]=1
            L3.config_machine((475,200,250,200),*lac,1,1,1,1)
            L3v.stepnumber+=1
            L3.labels = []
            if L3v.stepnumber==L3v.number_of_rounds[L3v.character]: # If the game is over, the player moves on to the next character.
                L3v.character+=1
                L3v.stepnumber=0
                L3v.current_prl = []
                L3v.current_brl = []
                L3v.step_score = [0,0]
                L3.add_player("char%d"%(L3v.character+1),(860,330),1)
                L3.add_player("char0",(280,330))
            if L3v.character==5: # If the player has played against all five characters, the game ends.
                L3.flush()
                L3.add_label("And your total score is...","black",main_font,24,(100,40),0)
                L3.add_label("%d"%L3v.current_score,"black",main_font,72,(100,40),0.4)
                if L3v.current_score>35:
                    L3.add_label("which is pretty good! (the lowest & highest possible","black",main_font,24,(180,70),0)
                elif L3v.current_score>20:
                    L3.add_label("which is not bad! (the lowest & highest possible","black",main_font,24,(180,70),0)
                else:
                    L3.add_label("which is okay! (the lowest & highest possible","black",main_font,24,(180,70),0)
                L3.add_label("scores are 7 and 49, respectively)","black",main_font,24,(180,70),1.2)
                L3.add_label("So who were these strange characters you just played against?","black",main_font,24,(100,200),0)
                L3.add_player("char1",(150,300),1)
                L3.add_player("char2",(360,300),1)
                L3.add_player("char3",(570,300),1)
                L3.add_player("char4",(780,300),1)
                L3.add_player("char5",(990,300),1)
                for b in L3.buttons: # This loop adds the "Let's find out!" button to the page.
                    print(b[2][0])
                L3.add_button("Let's find out!","black",main_font,24,(450,500,300,50),"white","yellow","green","black",[[L3index],[s.switch_section,L3,L3]])
            else:
                L3.add_label("opponent: %d of 5"%(L3v.character+1),"black",main_font,20,(600,50),-2)
                L3.add_label("your total score: %d"%(L3v.current_score),"black",main_font,20,(600,80),-2)
                L3.add_label("%d ~ %d"%tuple(L3v.step_score),"black",main_font,70,(600,120),-2)
        L3.add_button("COOPERATE","black",main_font,24,(350,500,200,50),"white","yellow","green","black",[[L3resp,1],[s.switch_section,L3,L3]])
        L3.add_button("CHEAT","black",main_font,24,(650,500,200,50),"white","yellow","green","black",[[L3resp,0],[s.switch_section,L3,L3]])

  

    s = back.Screen((1400,700),(1300,700),"logo.png","The Evolution of Trust",L0,{L0:L0init,L1:L1init,L2:L2init,L3:L3init},"white")
    L0init()
    s.switch_section(0,L0)

    while 1: # This loop runs the game.
        while L0.enabled: # This loop runs the main section.
            s.before()
            s.place_subscreen(L0.return_subscreen())
            s.after()
            s.event_handler(L0.buttons,[L0.ready_objects,L0.ready_dynamic])
        while L1.enabled: # This loop runs the first section.
            s.before()
            s.place_subscreen(L1.return_subscreen())
            s.after()
            s.event_handler(L1.buttons,[L1.ready_objects,L1.ready_dynamic])
        while L2.enabled: # This loop runs the second section.
            s.before()
            s.place_subscreen(L2.return_subscreen())
            s.after()
            s.event_handler(L2.buttons,[L2.ready_objects,L2.ready_dynamic])
        while L3.enabled: # This loop runs the third section.
            s.before()
            s.place_subscreen(L3.return_subscreen())
            s.after()
            s.event_handler(L3.buttons,[L3.ready_objects,L3.ready_dynamic])
        

if __name__ == "__main__": # This runs the game.
    main()