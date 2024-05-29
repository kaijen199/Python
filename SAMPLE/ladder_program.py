#MA1008 Mini Project Mai Kai Jen MA10

import turtle

def issue_challenge (p1, p2, date):
    """
    The function takes in the arguments of p1, the challenger position and p2, the challenged position and appends the challenge data to the data.
    The score will not be input and will be done by the record result function
    NOTE: Very important to note the -1 as indexing start from 0 while ranking starts from 1
    """
    
    if p1 - p2 <= 3: #check for forbidden challenge, which is not allowed when above 3
        ladder = open("ladder.txt", "r")
        players = ladder.readlines()
        challenger = players[p1-1].rstrip() #retrieves challenger by current position on ladder and strip new line
        challenged = players[p2-1].rstrip() #retrieves challenged by current position on ladder and strip new line
        ladder.close()
        
        data = open("data.txt", "a+") #open the data file, store its existing contents in a string and append the new challenge
        data.write(str(challenger) + " " + str(p1) + "/" + str(challenged) + " " + str(p2) + "/" + str(date) + "/""\n")
        data.close()

        data = open("data.txt", "r") #write the contents in a new file
        save_state = data.read() #saves the data in a string
        data.close()

        data = open("data_"+date+".txt", "w") 
        data.write(save_state) #saves the string into a new file to provide a save state for retrieval when querying
        data.close()        
    
    #Example function call
    #issue_challenge (4, 3, "20-07-2000")

def join_ladder(player, date):
    """
    The function takes in the player and the join date and edits the ladder file and data file
    """
    ladder = open("ladder.txt", "a")
    ladder.write("\n" + player) #append the contents to the ladder file
    ladder.close()

    data = open("data.txt", "a")
    data.write("+" + player + "/" + date + "\n") #append the contents to the data file
    data.close()

    data = open("data.txt", "r")
    save_state = data.read() #saves the data in a string
    data.close()

    data = open("data_"+date+".txt", "w")
    data.write(save_state) #saves the string into a new file to provide a save state for retrieval when querying
    data.close()

    data = open("ladder.txt", "r")
    save_state = data.read() #saves the data in a string
    data.close()

    data = open("ladder_"+date+".txt", "w")
    data.write(save_state) #saves the string into a new file to provide a save state for retrieval when querying
    data.close()  

    #example function call
    #join_ladder("bob", "12-02-2020")

def player_match(most_active=True):
    '''
    The function returns by default the most active player, and when most_active argument is False it gives the least active player.
    The function also returns the number of matches the player has played
    '''
    data = open("data.txt", "r")
    data_text = data.readlines()
    data.close()
    players = {} #initialise a dictionary to keep track of the number of matches a player has played
    for line in data_text:
        if not line.startswith("+") and not line.startswith("-"):
            x = line.split("/", 2) #due to the way data entries are formatted, we want the names which are separated by the first 2 forward slashes
            
            challenger_string = x[0] #store the first element of the list which contanins the challenger name and the position
            challenged_string = x[1] #store the second element of the list which contanins the challenged name and the position
            challenger = ''
            challenged = ''
            for j in challenger_string: #the following is to remove the position and keep the name only
                if not j.isdigit():
                    challenger += j

            for j in challenged_string:
                if not j.isdigit():
                    challenged += j

            if challenger in players: #if player is already in dictionary, add 1 for every match he/she has played
                players[challenger] += 1
            else:
                players[challenger] = 1 #if player is not in dictionary, create new entry
            if challenged in players:
                players[challenged] += 1
            else:
                players[challenged] = 1

        #at the end of this there will be a dictionary generated showing the players and the number of matches he/she has played in
    
    if most_active: #returns based on whether the argument wants the most active or the least active player.
        return max(players, key=players.get), str(players[max(players, key=players.get)])
    else:
        return min(players, key=players.get), str(players[min(players, key=players.get)])

    #Example function calls:
    #print(player_match(True))
    #print(player_match(False))
    
def record_result (p1, p2, date, scores):
    """
    The function searches the data file for a match that has been issued but has not any recorded score and records the score for that relevant entry.
    The function takes in the argument of player position and records the results, after which the ladder is adjusted according to the result
    The function lastly returns the result for use of display in the GUI
    NOTE: TO RECORD RESULT CHALLENGE MUST FIRST BE ISSUED
    """
    ladder = open("ladder.txt", "r")
    players = ladder.readlines()
    challenger = players[p1-1].rstrip() #retrieves challenger by current position on ladder and strip new line
    challenged = players[p2-1].rstrip() #retrieves challenged by current position on ladder and strip new line
    ladder.close()
    
    data = open("data.txt", "r")    
    match_history = data.read()
    if match_history.find(str(challenger) + " " + str(p1) + "/" + str(challenged) + " " + str(p2) + "/" + str(date) + "/""\n") != -1:
        found = True #check if the match exists to prevent deleting of file, makes use of the fact that find() method returns -1 if not found
        match_history_updated = match_history.replace(str(challenger) + " " + str(p1) + "/" + str(challenged) + " " + str(p2) + "/" + str(date) + "/""\n",\
                          str(challenger) + " " + str(p1) + "/" + str(challenged) + " " + str(p2) + "/" + str(date) + "/" + scores + "\n")
        #finds the challenge and replaces it with the updated one which includes the result of the challenge

    else:
        match_history_updated = match_history #ensures that if match is not found the file is still intact
    data.close()

    data = open("data.txt", "w")
    data.write(match_history_updated) #overwrite with recorded result
    data.close()

    #determining who won
    score_list = scores.split() #splits the scores into a list by whitespace
    challenger_points = 0
    challenged_points = 0
    for i in score_list:
        if int(i[0:1]) > int(i[3:4]):
            challenger_points += 1
        elif int(i[0:1]) < int(i[3:4]):
            challenged_points += 1
    if challenger_points > challenged_points:
        challenger_win = True
    else:
        challenger_win = False
    

    #update the ladder (which only happens when the challenger won)
    if challenger_win:      
        ladder = open("ladder.txt", "r")
        player_list = ladder.readlines()
        winner = player_list[p1-1] #retrieves the name of the winner
        player_list.insert(p2-1, winner) #the challenger takes the place of the challenged
        player_list.pop(p1) #now there is a duplicate of the challenger name, remove the challenger from its original position
        ladder.close()

        ladder = open("ladder.txt", "w")
        ladder.writelines(player_list) #overwrite with updated result
        ladder.close()

    data = open("data.txt", "r")
    save_state = data.read() #saves the data in a string
    data.close()

    data = open("data_"+date+".txt", "w")
    data.write(save_state) #saves the string into a new file to provide a save state for retrieval when querying
    data.close()

    data = open("ladder.txt", "r")
    save_state = data.read() #saves the data in a string
    data.close()

    data = open("ladder_"+date+".txt", "w")
    data.write(save_state) #saves the string into a new file to provide a save state for retrieval when querying
    data.close()       
    
    #Example function call - challenger lost
    #record_result(4, 3, "20-07-2000", "20-22 18-21")
    #Example function call - challenger won
    #record_result(4, 3, "20-07-2000", "22-20 21-18")

def retrieve_save_state(date, savetype):
    """
    This function retrieves the last save state to perform edits to the data and ladder at the respective dates.
    Date is in the format DD-MM-YYYY
    Save Type takes in string either "data" or "ladder"
    Function returns a string of the file name with the relevant file having the most recent save entry since that date
    """
    import os #imports this library to know the files in the directory
    list_of_files = []
    list_ladder_save_date = []
    list_data_save_date = []
    # Get .txt files found in the working directory
    for f_name in os.listdir(): #get all .txt files
        if f_name.endswith('.txt'):
            list_of_files.append(f_name)
            
    for f_name in list_of_files:
        if f_name.startswith('data_'): #get all data files
            list_data_save_date.append(f_name[11:15]+f_name[8:10]+f_name[5:7]) #convert dates to YYYYMMDD format in a list for easy comparison
                            
    for f_name in list_of_files:
        if f_name.startswith('ladder_'): #get all ladder files
            list_ladder_save_date.append(f_name[13:17]+f_name[10:12]+f_name[7:9]) #convert dates to YYYYMMDD format in a list for easy comparison

    retrieve_day = date[0:2] #gets the day in the argument
    retrieve_month = date[3:5] #gets the month in the argument
    retrieve_year = date[6:10] #gets the year in the argument

    retrieve_date = ""
    query_date = date[6:10]+date[3:5]+date[0:2] #get the query date in the YYYYMMDD format

    list_data_save_date.sort(reverse = True) #sort the list in order of the date

    #gets the most recent file before the argument date, this works as the list of dates are sorted
    if query_date in list_data_save_date:
        retrieve_date = query_date
        
    else:
        for data_date in list_data_save_date:
            if retrieve_date == "":
                if query_date > data_date:
                        retrieve_date = data_date
            else:
                if retrieve_date < data_date:
                    retrieve_date = data_date
                    break
            

    if retrieve_date == "": #if there are no save states, retrieve the earliest save state
        retrieve_date = list_data_save_date[-1] #get earliest save state
        retrieve_date = "_"+retrieve_date[6:8]+"-"+retrieve_date[4:6]+"-"+retrieve_date[0:4]
        return savetype+retrieve_date+".txt"
    else:   
        retrieve_date = "_"+retrieve_date[6:8]+"-"+retrieve_date[4:6]+"-"+retrieve_date[0:4] #convert back to original fomrmat
        return savetype+retrieve_date+".txt"

    #Example function call  
    #print(retrieve_save_state("25-07-2021", "data"))

def withdraw_ladder(player, date):
    """
    The function finds the relevant player and withdraws him from the ladder.
    The function also finds the player ranking and updates the ladder accordingly

    """
    ladder = open("ladder.txt", "r")
    player_list = ladder.readlines()

    if player+"\n" in player_list: #check if the player is a valid player to remove
        placing = 1 + player_list.index(player+"\n")
        player_list.remove(player+"\n")
        ladder.close()

        data = open("data.txt", "a+") #update the data file with this withdrawal
        data.write("-" + player + " " + str(placing) + "/" + date + "\n")
        data.close()

        
        ladder = open("ladder.txt", "w")
        ladder.writelines(player_list) #overwrite with updated data without player
        ladder.close()

    data = open("data.txt", "r")
    save_state = data.read() #saves the data in a string
    data.close()

    data = open("data_"+date+".txt", "w")
    data.write(save_state) #saves the string into a new file to provide a save state for retrieval when querying
    data.close()

    data = open("ladder.txt", "r")
    save_state = data.read() #saves the data in a string
    data.close()

    data = open("ladder_"+date+".txt", "w")
    data.write(save_state) #saves the string into a new file to provide a save state for retrieval when querying
    data.close()  

    #test function call
    #withdraw_ladder("D Lin", "09-09-2021")

def retrieve_matches_in_range(startdate, enddate):
    """
    This function retrieves the list of dates given the start and end dates
    Date is in the format DD-MM-YYYY
    Function returns a string of the matches within the range of startdate and enddate
    """
    global write_pos #define this global variable which will be used by Turtle to determine where to write the output based on the number of lines it uses
    
    data = open("data.txt", "r")
    data_text = data.readlines()
    data.close()

    def DMY(date): #this function takes in a string DD-MM-YYYY and gives the date in YYYYMMDD
        day = str(date[0:2])
        month = str(date[3:5])
        year = str(date[6:10])
        return year+month+day

    list_of_matches = "" #This stores all the matches that are within the startdate and the enddate
    
    for i in data_text:
        if not i[0] == "-" and not i[0] == "+": #check that it is not a player addition or player withdrawal data
            x = i.find("-") #uses the dash to find the date in string
            match_date = i[x-2:x+8]
            if DMY(match_date) > DMY(startdate) and DMY(match_date) < DMY(enddate): #check within range
                list_of_matches += i
                write_pos -= 15

    return list_of_matches
   

#initialise the turtle screen and set style choices
screen = turtle.Screen() #initialise Turtle screen
screen.title("Badminton Ladder") #title of window
screen.setup(1200,600) #use a 1200x600 screen
screen.bgcolor("white")
style = ('Times New Roman', 15)
turtle.penup()
turtle.hideturtle()

#begin drawing
t0 = turtle.Turtle() #define another turtle, turtle t0 is used for writing the welcome message that does not change
t0.penup()
t0.hideturtle()
t0.setpos(-550,260)
t0.write("Welcome to the Badminton Ladder Main Page!", font=style)


#generate list to display ladder for first 10 and button to show next 10
ladder = open("ladder.txt", "r")
ladder_text = ladder.readlines()
number_of_players = str(len(ladder_text))
ladder.close()
ladder_string = ''
sets = 0 #counts the number of sets so the refresh cycle knows the cycle, this will be used with the modulus function
ladder_list = [] #stores the ladder_strings for set of 10 players
for j in range(1, len(ladder_text)+1, 10):
    ladder_string = ""
    sets += 1
    for i in range(0, 10):
        if i+j <= len(ladder_text):
            ladder_string += (str(i+j)+") ")
            ladder_string += ladder_text[i+j-1]
        if not ladder_string.endswith("\n"):
            ladder_string += "\n"
    ladder_list.append(ladder_string) #stores the string in a list by set of 10 players

        
style = ('Times New Roman', 10)
turtle.setpos(-550,-280)
instructions1 = "\
Press 'r' to show the next 10 challengers in the ladder\n"

instructions2 = "\
Instructions for Challengers:\n\
1) Press '1' to query the order of the ladder on a specified date\n\
2) Press '2' to query the data of a specific challenge based on the player names\n\
3) Press '3' to query the data of a specific challenge based on the date\n\
4) Press '4' to query the list of matches a player has played\n\
5) Press '5' to query the most active player\n\
6) Press '6' to query the least active player\n\
7) Press '7' to query the list of matches played in a specific date range\n\
\n\
Instructions for Admins:\n\
1) Press 'A' to record a challenge\n\
2) Press 'B' to record the result of a challenge\n\
3) Press 'C' to register a new player\n\
4) Press 'D' to withdraw a player from the ladder"

instructions3 = "Press 't' to clear the screen in the event that the outputs overlap each other"

#Display recent 2 matches and current ladder for first 10 by default
data = open("data.txt", "r")
data_text = data.readlines()
data.close()
count = 0
pos = -1
data_string = ''
while count < 2:
    i = data_text[pos]
    pos -= 1
    if not i.startswith("+") and not i.startswith("-") and not i.endswith("/\n"): #this is so that we show matches that are completed and not player addition or withdrawal entries
        data_string += i
        count += 1
    
t1 = turtle.Turtle() #define another t1 turtle this is used for writing the ladder and recent 2 matches
t1.penup()
t1.hideturtle()
t1.setpos(-550,-250)
t1.write("Current Ladder of " + number_of_players + " Players:\n"+ ladder_list[0] +"\n"+ instructions1 + "\nRecent 2 Matches:\n" + data_string + "\n" + instructions2, font=style)


t3 = turtle.Turtle() #the turtle t3 is used to write instructions and other premanent/static text that do not change
t3.penup()
t3.hideturtle()

t3.setpos(-550, -290)
style = ('Times New Roman', 10)
t3.write(instructions3, font=style)


t3.setpos(-100,300)
t3.pendown()
t3.setpos(-100,-300)
t3.penup()

t3.setpos(-90, 280)
t3.write("My Dashboard", font=style)

t3.setpos(-100,275)
t3.pendown()
t3.setpos(600,275)
t3.penup()

#Function 'r' to refresh the ladder to next 10
refresh_var = 1
def show_next_ten():
    global refresh_var #this global variable is used in conjunction with sets defined above
    t1.clear()
    t1.setpos(-550,-250)
    style = ('Times New Roman', 10)
    t1.write("Current Ladder of " + number_of_players + " Players:\n"+ ladder_list[refresh_var%sets] +"\n"+ instructions1 + "\n\nRecent 2 Matches:\n" + data_string + "\n" + instructions2, font=style)
    refresh_var += 1 #increments refresh_var by 1 to show next set of 10 players
    #we see that the refresh_var%set global variable allows us to toggle between a cycle of set of 10 players

#Initialise pos to know where to write the outputs
write_pos = 270

#Function to clear the screen, will be called for turtle.write functions to make way for outputs
def clear_screen():
    turtle.clear()
    global write_pos
    write_pos = 270 #define the global variable to reposition the turtle to default position whenever the screen is cleared

#Challenger Function 1
import re #We import the Python Regular Expression module to ensure a wrong input does not crash the program

def query_ladder():
    clear_screen() #clear the dashboard to allow output
    global write_pos 
    date = turtle.textinput("Input date.", "Input query date in DD-MM-YYY format:")
    file_retrieve = retrieve_save_state(date, "ladder") #We call the retrieve_save_state function defined above to retrieve the most recent ladder file to get the state the ladder at that time
    print(file_retrieve)
    ladder = open(file_retrieve, "r") #called the file_retrieve function to retrieve the correct file to display the query
    ladder_text = ladder.readlines()
    ladder.close()
    write_pos -= 30 #positioning for writing the output, arbitrary value
    ladder_string = ''
    for i in range(1, len(ladder_text)+1):
        ladder_string += (str(i)+") ")
        ladder_string += ladder_text[i-1]
        write_pos -= 15 #makes space for the output by counting the lines of output
    style = ('Times New Roman', 10)
    turtle.setpos(-90,write_pos)
    turtle.write("Current Ladder on " + date + ":\n" + ladder_string, font=style)

#Challenger Function 2
def query_name():
    clear_screen()
    global write_pos
    name1 = turtle.textinput("Input Name of First Player", "Input Name of First Player. Refer to ladder for accurate input.")
    name2 = turtle.textinput("Input Name of Second Player", "Input Name of Second Player. Refer to ladder for accurate input.")
    data = open("data.txt", "r")
    data_text = data.readlines()
    data.close()
    data_string = ''
    write_pos -= 45
    for i in data_text:
        if name1 in i and name2 in i:
            data_string += i
            write_pos -= 15
            print(data_string)
    style = ('Times New Roman', 10)
    turtle.setpos(-90, write_pos)
    turtle.write("Challenges involving "+name1+" and "+name2+ ":\n" + data_string, font=style)

#Challenger Function 3
def query_date():
    clear_screen()
    global write_pos
    date = turtle.textinput("Input date.", "Input query date in DD-MM-YYY format:")
    data = open("data.txt", "r")
    data_text = data.readlines()
    data.close()
    data_string = ''
    write_pos -= 45
    for i in data_text:
        if date in i:
            data_string += i
            write_pos -= 15
            print(write_pos)
    style = ('Times New Roman', 10)
    turtle.setpos(-90,write_pos)
    turtle.write("Challenges on "+date+":\n" + data_string, font=style)

#Challenger Function 4
def query_name_single():
    clear_screen()
    global write_pos
    name = turtle.textinput("Input Name of Player", "Input Name of Player. Refer to ladder for accurate input.")
    data = open("data.txt", "r")
    data_text = data.readlines()
    data.close()
    data_string = ''
    write_pos -= 45
    for i in data_text:
        if name in i:
            data_string += i
            write_pos -= 15
    style = ('Times New Roman', 10)
    turtle.setpos(-90,write_pos)
    turtle.write("Challenges involving "+name+":\n" + data_string, font=style)

#Challenger Function 5
def query_most_active():
    clear_screen()
    global write_pos
    write_pos -= 30
    style = ('Times New Roman', 10)
    turtle.setpos(-90, write_pos)
    turtle.write("Most active player: "+player_match(True)[0]+"with "+player_match(True)[1]+" matches.", font=style)
    #calls on player_match(True) for the most active player

#Challenger Function 6
def query_least_active():
    clear_screen()
    global write_pos
    write_pos -= 30
    style = ('Times New Roman', 10)
    turtle.setpos(-90, write_pos)
    turtle.write("Most active player: "+player_match(False)[0]+"with "+player_match(False)[1]+" matches.", font=style)
    #calls on player_match(False) for least active player

#Challenger Function 7
def query_date_range():
    clear_screen()
    global write_pos
    write_pos -= 45
    startdate = turtle.textinput("Input start date", "Input start date in DD-MM-YYY format:")
    enddate = turtle.textinput("Input end date", "Input end date in DD-MM-YYY format:")
    style = ('Times New Roman', 10)
    text = retrieve_matches_in_range(startdate, enddate) #calls the matches_in_range function defined above to get the string required
    if write_pos < -290:
        turtle.setpos(-90, 240)
        turtle.write("Query size too large, try a smaller date range!", font=style)
    else:
        turtle.setpos(-90, write_pos)
        turtle.write("Matches played between "+ startdate + " and " + enddate + ":\n" + text, font=style)
    #We see in the above line we call the retrieve_matches_in_range function to obtain the matches within the defined start date and end date to be output
    
#Admin Function A
def record_challenge_screen():
    p1 = turtle.textinput("Input Current Rank of Challenger", "Input Current Rank of Challenger. Refer to ladder for accurate input.")
    p2 = turtle.textinput("Input Current Rank of Challenged", "Input Current Rank of Challenged. Refer to ladder for accurate input.")
    date= turtle.textinput("Input Date", "Input date in DD-MM-YYY format:")
    issue_challenge(int(p1), int(p2), date)
    clear_screen()
    turtle.setpos(-90, 240)
    style = ('Times New Roman', 10)
    if int(p1) - int(p2) <= 3: #check for forbidden challenge
        turtle.write("Challenge issued between #"+ p1 +" and #"+p2+" on "+date, font=style)
    else: #if forbidden challenge, inform the user
        turtle.write("Forbidden Challenge.", font=style)

#Admin Function B
def record_result_screen():
    p1 = turtle.textinput("Input Current Rank of Challenger", "Input Current Rank of Challenger. Refer to ladder for accurate input.")
    p2 = turtle.textinput("Input Current Rank of Challenged", "Input Current Rank of Challenger. Refer to ladder for accurate input.")
    date = turtle.textinput("Input Date", "Input date in DD-MM-YYY format:")
    scores = turtle.textinput("Input Scores", "Input scores in XX-XX XX-XX XX-XX format, where it is challenger-challenged")
    record_result(int(p1), int(p2), date, scores)
    clear_screen()
    turtle.setpos(-90, 240)
    style = ('Times New Roman', 10)
    turtle.write("Result recorded for challenge between #"+ p1 +" and #"+p2+" on "+date, font=style)


#Admin Function C
def join_ladder_screen():
    name = turtle.textinput("Input Player Name", "Input Player Name. Advised to follow naming conventions of ladder. Do not input - or /.")
    date = turtle.textinput("Input Date", "Input join date in DD-MM-YYY format:")
    join_ladder(name, date)
    clear_screen()
    turtle.setpos(-90, 240)
    style = ('Times New Roman', 10)
    turtle.write(name + " has joined the ladder!", font=style)

#Admin Function D
def withdraw_ladder_screen():
    name = turtle.textinput("Input Player Name", "Input Player Name. Refer to the exact name shown in the ladder.")
    date = turtle.textinput("Input Date", "Input withdraw date in DD-MM-YYY format:")
    withdraw_ladder(name, date)
    clear_screen()
    turtle.setpos(-90, 240)
    style = ('Times New Roman', 10)
    turtle.write(name + " has been withdrawn from the ladder.", font=style)

#Turtle to listen for the various keys to execute the defined function
#Define both upper and lowercase for alphabhet keys so users do not have to change caps lock to access the functions
screen.onkey(show_next_ten, "r")
screen.onkey(show_next_ten, "R")
screen.onkey(clear_screen, "t")
screen.onkey(clear_screen, "T")
screen.onkey(query_ladder, "1")
screen.onkey(query_name, "2")
screen.onkey(query_date, "3")
screen.onkey(query_name_single, "4")
screen.onkey(query_most_active, "5")
screen.onkey(query_least_active, "6")
screen.onkey(query_date_range, "7")
screen.onkey(record_challenge_screen, "A")
screen.onkey(record_challenge_screen, "a")
screen.onkey(record_result_screen, "B")
screen.onkey(record_result_screen, "b")
screen.onkey(join_ladder_screen, "C")
screen.onkey(join_ladder_screen, "c")
screen.onkey(withdraw_ladder_screen, "D")
screen.onkey(withdraw_ladder_screen, "d")
screen.listen()

turtle.done()
