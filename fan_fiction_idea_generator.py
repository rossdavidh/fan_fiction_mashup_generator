import os
import sys
import csv
import random
from string import Template

CHARACTERS = set(['Pinkie Pie','Nightmare Moon','Gilligan','The Terminator','Santa Claus','Tom Sawyer','James Bond','The Leprechaun','Dr. Who','Sherlock Holmes','Ethel the Aardvark','Paul Bunyan','Popeye','Alice','Ada Lovelace','Old Yeller','Corky the Clown', 'Swamp Thing', 'Jughead','Zelena the Wicked Witch','Ace Ventura','Hermione Granger','Gollum', 'Scout Finch','Charles Darwin','Ishmael','Tom Joad','Keyser Soze','Jack Sparrow','Ellen Ripley','Amélie Poulain','Bruce Lee','Robin Hood','Lady Gaga','Steven Universe','Claudia Kincaid','Mrs. Piggle-wiggle','Mary Poppins','Star Butterfly','HAL 9000','Godzilla','He-Man','Tintin','Paddington Bear','The Six Million Dollar Man','Scheherazade','Snow White','Little Red Riding Hood','Baba Yaga','Tiamat','Babe the pig','Harriet Tubman','Nicola Tesla','Albert Einstein','Jane Goodall','Aaron Burr','John Henry','Captain Nemo','Ibn Khaldun'])

SERIES     = set(["My Little Pony","Gilligan's Island","Star Trek","Star Wars","Grimm's Fairy Tales","X-Files","The Jeffersons","Gremlins","the Olympian Pantheon","Cats","Twilight Zone","Arabian Nights","Friends","Golden Girls","Hogan's Heroes","the Simpsons","the Muppets","The Solid Gold Dancers","Knights of the Round Table","the League of Extraordinary Gentlemen","the Unseelie Court","the Founding Fathers"])


MODIFIERS  = set([' as written by Ian Fleming',' as written by Jane Austen',' with a Greek chorus',' as a silent movie','',' as shadow puppet theater',' in Legos',' as Wagnerian opera', ' as written by William Shakespeare', ' as epic poetry', ' as written by William Burroughs', ' as kabuki theater',' a feminist retelling',' in ASCII art',' where they are secretly vampires', ' as written by Ayn Rand', ' a dadaist retelling', ' as alliterative verse', ' the rock opera', ' as written by Noam Chosmky',' a new Cartoon Network animated series',' as anthropomorphic rocks', ' as anthropomorphic cats', ' as written by Rod Sterling'," (this time, it's personal)",' as written by Dr. Seuss',' as written by Friedrich Nietzsche', ' as painted by Michaelangelo', ' as drawn by Edward Gorey', ' as sculpted by August Rodin', ' as drawn by Escher', ' as a Choose Your Own Adventure paperback', ' heckled by Mystery Science Theater 3000', ' as mockumentary',' as gameshow',' as a trapunto quilt pattern',' as modern dance',' the podcast',' the ballet', ' with audience participation ala Rocky Horror'])

CHAR_MODIFIERS = set(['the ghost of ','mecha-','a holographic simulation of ','zombie ','an android replica of ','son of ','bride of '])

#this hack is forced upon us because a set cannot contains dicts, as dicts are not hashable because they are mutable
def pickGame():
    games = set(['Calvinball','rock paper scissors lizard spock','I spy','Settlers of Catan'])
    return random.sample(games,1)[0]

def pickTeamGame():
    if random.random() < 0.5:
        teamgames = set(['baseball','soccer','rugby','quidditch','curling','speedwalking'])
        return random.sample(teamgames,1)[0]
    else:
        return pickGame()

def pickLocation():
    locations = set(['Shangri-La','Atlantis','Madagascar','Nepal','Mos Eisley','Minas Tirith'])
    return random.sample(locations,1)[0]

def pickIssue():
    issues = set(['drug addiction','alcoholism','teen pregnancy','eating disorders'])
    return ' (about '+random.sample(issues,1)[0] + ')'

def pickYear():
    years = set(['1939','1929','1776','1848','1666','1066'])
    return random.sample(years,1)[0]

def pickConversation():
    topics = set(['life','death','the banality of evil','string theory','what is wrong with kids these days','the absurdity of our existence','birdwatching','how to cook a great quiche','Fermi\'s Paradox'])
    return random.sample(topics,1)[0]

def pickWorkplace():
    workplaces = set(['Once Over coffeeshop','the morgue','Hogwarts','Book People','Santa\'s Workshop','the Big Donut','Willy Wonka\'s Chocolate Factory'])
    return random.sample(workplaces,1)[0]

def pickTrip():
    trips = set(['Oregon Trail','Siberian Railway', 'Orient Express', 'Appalachian Trail','Long March','long flight to Singapore','rocketship to Mars'])
    return random.sample(trips,1)[0]

def pickMonarch():
    monarchs = set(['Queen Victoria','Queen Elizabeth','Julius Caesar','George Washington','Charlemagne','Pericles','Kublai Khan'])
    return random.sample(monarchs,1)[0]

SCENARIOS  = {'chriscarol'  :{'template':Template('$char1 and $series1 Christmas Carol')},
              'agents'      :{'template':Template('$char1 and $char2, secret agents for '),'rule':pickMonarch},
              'bender'      :{'template':Template('$char1 and $char2 on a three-day bender, where they wake up in '),'rule':pickLocation},
              'inspace'     :{'template':Template('$char1 and $series1 In Space')},
              'onisland'    :{'template':Template('$char1 and $char2 Marooned On An Island')},
              'versus'      :{'template':Template('$char1 vs. $char2')},
              'thrutime'    :{'template':Template('$char1 and $char2 Travel Through Time')},
              'debate'      :{'template':Template('$char1 and $char2 debate the thorny issue of '),'rule':pickConversation},
              'lesson'      :{'template':Template('$char1 and $char2 Learn a Lesson')}, 
              'vspecial'    :{'template':Template('A Very Special $series1 Episode with guest $char1'),'rule':pickIssue},
              'zombies'     :{'template':Template('$series1 and $char1 face a zombie apocalypse')},
              'civilwar'    :{'template':Template('$series1: Civil War')},
              'whenmet'     :{'template':Template('When $series1 Met $series2')},
              'tourney'     :{'template':Template('When $series1 and $series2 played a hard-fought game of '), 'rule':pickTeamGame},
              'saveday'     :{'template':Template('$char1 and $char2 Save the Day')},
              'pickyear'    :{'template':Template('$series1 and $char2 in the year '),'rule':pickYear},
              'slayer'      :{'template':Template('$char1, Vampire Hunter')},
              'frankenst'   :{'template':Template('$char1, a modern Prometheus')},
              'deconst'     :{'template':Template('Deconstructing $char1 and $char2')},
              'switch'      :{'template':Template('$series1 as performed by the characters of $series2')},
              'bodyswitch'  :{'template':Template('When $char1 and $char2 Switched Bodies')},
              'busyshift'   :{'template':Template('$char1 and $char2 Work a Busy Shift at '),'rule':pickWorkplace},
              'ontheroad'   :{'template':Template('$char1 and $char2 on the '), 'rule':pickTrip},
              'monetize'    :{'template':Template('$char1 and $char2 monetize it')},
              'talking'     :{'template':Template('$char1 and $char2 Have a Talk about '),'rule':pickConversation},
              'fishing'     :{'template':Template('$char1 and $char2 go fishing, while talking about '),'rule':pickConversation},
              'death'       :{'template':Template('$char1 saves $char2 by beating Death in a game of '),'rule':pickGame},
              'coffeebook'  :{'template':Template('pictures of $series1 taken by $char1, as a coffeetable book')}}


def already_used_today():
    used = {'characters':[],'settings':[],'scenarios':[],'rules':[],'modifiers':[]}
    #TODO: check if file was last edited over an hour ago, and if so delete all rows
    if not os.path.isfile('mashups_used_today.csv'):
        f = open('mashups_used_today.csv','w')
        f.write('"characters","settings","scenarios","rules","modifiers"\n')
        f.close()

    with open('mashups_used_today.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        headers   = []
        for row in csvreader:
            if headers == []:
                headers = row
            else:
                for index,cell in enumerate(row):
                    if len(cell.strip()) < 1:
                        continue
                    elif headers[index] == 'characters':
                        used['characters'].append(row[index])
                    elif headers[index] == 'settings':
                        used['settings'].append(row[index])
                    elif headers[index] == 'scenarios':
                        used['scenarios'].append(row[index])
                    elif headers[index] == 'rules':
                        used['rules'].append(row[index])
                    elif headers[index] == 'modifiers':
                        used['modifiers'].append(row[index])
    message_to_clean_up = 'the file mashup_used_today.csv looks pretty full, especially for '
    if (len(used['characters']) > (len(CHARACTERS)-4)):
        message_to_clean_up += 'characters'
    elif (len(used['settings']) > (len(SERIES)-4)):
        message_to_clean_up += 'settings'
    elif (len(used['scenarios']) > (len(SCENARIOS)-4)):
        message_to_clean_up += 'scenarios'
    elif (len(used['modifiers']) > (len(MODIFIERS)-4)):
        message_to_clean_up += 'modifiers'
    if len(message_to_clean_up) > 65:
        print(message_to_clean_up)
        sys.exit()
    return used

def pick_chars_settings_and_scenario(used):

    while True:
        chars    = random.sample(CHARACTERS,2)
        if chars[0] not in used['characters'] and chars[1] not in used['characters']:
            break
    if random.random() < 0.1:
        chars[1] = random.sample(CHAR_MODIFIERS,1)[0] + chars[1]

    while True:
        settings = random.sample(SERIES,2)
        if settings[0] not in used['settings'] and settings[1] not in used['settings']:
            break

    while True:
        scenario = random.sample(SCENARIOS.keys(),1)[0]
        if scenario not in used['scenarios']:
            break
    return chars,settings,scenario

def pick_idea(chars,settings,scenario,used):
    idea = SCENARIOS[scenario]['template'].substitute(char1=chars[0],char2=chars[1],series1=settings[0],series2=settings[1])
    if 'rule' not in SCENARIOS[scenario]:
        rule_used = ''
    else:
        while True:
            rule_used = SCENARIOS[scenario]['rule']()
            if rule_used not in used['rules']:
                break
        idea = idea + rule_used
    while True:
        modifier = random.sample(MODIFIERS,1)[0]
        if modifier not in used['modifiers']:
            break 
    if (len(modifier)>0):
        return idea + ',' + modifier,modifier,rule_used
    else:
        return idea,None,rule_used

def write_to_used_today_file(chars,idea,settings,scenario,rule_used,modifier):
    with open('mashups_used_today.csv',mode='a') as csvfile:
        writer = csv.writer(csvfile)
        if chars[0] in idea:
            first_new_row = [chars[0]]
        else:
            first_new_row = ['']
        if settings[0] in idea:
            first_new_row.append(settings[0])
        else:
            first_new_row.append('')
        first_new_row = first_new_row + [scenario,rule_used,modifier]
        writer.writerow(first_new_row)
        if (chars[1] in idea or settings[1] in idea):
            if chars[1] in idea:
                second_new_row = [chars[1]]
            else:
                second_new_row = ['']
            if settings[1] in idea:
                second_new_row.append(settings[1])
            else:
                second_new_row.append('')
            next_new_row  = second_new_row + ['','','']
            writer.writerow(next_new_row)

if __name__ == "__main__":
    random.seed()
    used                    = already_used_today()
    chars,settings,scenario = pick_chars_settings_and_scenario(used)
    idea,modifier,rule_used = pick_idea(chars,settings,scenario,used)
    print(idea)
    write_to_used_today_file(chars,idea,settings,scenario,rule_used,modifier)
