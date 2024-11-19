from pyfiglet import Figlet
import random
import time
import sys
import select 
import inflect
import re


def return_key_dictionary(mode):
    if mode == "m":
        m_mode = {
            'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
            'Am': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            'Ab': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
            'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
            'Bm': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
            'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
            'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
            'Cm': ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'],
            'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
            'Dm': ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'],
            'Db': ['Df', 'Eb', 'F', 'Gb', 'Af', 'Bb', 'C'],
            'D#m': ['D#', 'F', 'F#', 'G#', 'A#', 'B', 'C#'],
            'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
            'Em': ['E', 'Fs', 'G', 'A', 'B', 'C', 'D'],
            'Eb': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
            'Ebm': ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'Cb', 'Db'],
            'F': ['F', 'G', 'A', 'Bf', 'C', 'D', 'E'],
            'Fm': ['F', 'G', 'A', 'Bf', 'C', 'D', 'E'],
            'F#m': ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'],
            'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
            'Gm': ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'],
            'G#m': ['G#', 'A#', 'B', 'C#', 'D#','E','F#'],
            'Gb': ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'],
        }
        return m_mode
    else:
        b_mode = {
            'Am': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            'Bm': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
            'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
            'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
            'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
            'Dm': ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'],
            'Em': ['E', 'Fs', 'G', 'A', 'B', 'C', 'D'],
            'F': ['F', 'G', 'A', 'Bf', 'C', 'D', 'E'],
            'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
            'Gm': ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'],
        }
        return b_mode

#hey i got the following function from statck overflow although i adjusted it a tad by making it raise a ValueError instead, which
#ultimately got it to work. I tried for quite a long time to get it to work using python's threading library but had difficulties. 
#I will try to come back to this some day because it is an interesting problem
def input_with_timeout(user_input_string, timeout):
    sys.stdout.write(user_input_string)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n') 
    raise ValueError


def quiz(key_table, n, m):
   
    strikes = 0 
    print("If you get a question wrong...")
    time.sleep(1)
    print("OR if you take too long to answer... you will get a STRIKE!")
    time.sleep(1)
    print("And Three Strikes you're out!")
    time.sleep(1)
    print("Ready....Set..........Go!!!!")
   
    i = 0 
    while i < n:
        key_to_test = random.choice(key_table)
        number = random.randint(2,7)
        try:
            p = inflect.engine()
            answer = input_with_timeout(f"What is the {p.number_to_words(p.ordinal(number))} note in the key of {key_to_test}??", 3).capitalize()
            if answer != return_key_dictionary(m)[key_to_test][number-1]:
                strikes += 1
                print("Incorrect!!! STRIKE!!!!!")
                print("STRIKE")
                print(f"Strike {strikes}!!!") 
                i-=1   
        except ValueError:
            strikes +=1 
            print("Took Too Long!! Sooo, that's a STRIKE!!")
            print(f"Strike {strikes}!!!")
            i-=1 
        if strikes == 3:
            time.sleep(1)
            print("3 STRIKES, YOU'RE OUT! Goodbye. Please try again!")
            time.sleep(1)
            return False
        i += 1 
    return True
   
def main(): 

    #I added this try block so that my program exits gracefully when the user presses control-c 
    try:
        #Pring out a Greeting to the User
        figlet = Figlet()
        figlet.getFonts()
        figlet.setFont(font="slant")
        print(figlet.renderText("Musician Multiplication"))
        print("👽  🤖  🎹  🎼  🎸  👽  🤖  🎹  🎼  🎸  🤖  🎹  🎼  🎸  🎸")   

        #Find out from the user if they want to play in beginner mode, master mode, or the user can also quit here
        #Just using regex so that it doesn't matter if user input b or beginner, M or Master
        user_mode = input("Beginner(B) mode or Master(M) mode? or Quit(Q) ").strip()
        matches = re.search(r"([mMbBqQ])(.+)?",user_mode)
        if matches:
            if matches.group(1).lower() == "q":
                sys.exit("Goodbye!")
            else:
                mode = matches.group(1).lower()
        else:
            print("Sorry, that mode is not available")
            time.sleep(1)
            main()

        # the following logic figures out the details of the game, and eventually calls the quiz() function
        key_table = []
        count = 1 
        while True:
            if count == 1: 
                print("Keys to chose from: " , end = " ")
                for key in return_key_dictionary(mode):
                    print(key,end = " ")
                print()
                count = 2
            if len(key_table) == 0:
                print("Your Key Table: EMPTY")
            selected_key = input("pick a key to add to your key table! ").capitalize()
            if selected_key in key_table:
                print("you already picked that key!")
                continue
            if selected_key not in return_key_dictionary(mode):
                print("sorry, that key does not exist in this mode or in the universe")
                continue
            key_table.append(selected_key)
            print("Your Key Table: ", key_table)
            print()
            question = input("Just press Enter to start the game. Or Press A to add anther key to your key table ")
            print()
            if question == "A":
                continue
            if question == "":
                while True:
                    try:
                        number_of_questions = int(input("how many correct answers (min: 1, max: 99) are necesary to pass?  "))
                        if 0 < number_of_questions < 100:
                            if quiz(key_table, number_of_questions, mode) is True:
                                time.sleep(1)
                                print("WOWW SHOULD I CALL YOU MOZART?")
                                time.sleep(.05)
                                print(figlet.renderText("CONGRATS!!!"))
                                time.sleep(1)
                                main()
                            else:
                                main()
                        else:
                            print("pick a reasonable ammount of questions")
                    except ValueError:
                        pass
    except KeyboardInterrupt:
        sys.exit("     Goodbye!     Hope you play again!")

                    
if __name__ == "__main__":
    main()
    

    

    

