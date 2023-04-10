import pandas as pd
import json
import unicodedata


def encode_utf8(x):
    return unicodedata.normalize('NFKD', x)

personality_careers = pd.read_excel('personality careers.xlsx', 
                                    sheet_name=None, header=None)


sheet_esfp = personality_careers.get('ESFP')
# preprocess data
sheet_esfp = sheet_esfp.applymap(encode_utf8)
sheet_esfp.drop_duplicates(subset=[0], inplace=True)

careers = set(sheet_esfp[1].values)

# careers grouped by keywords found in the esfp datasheet
careers_dict = {
"Music and Singing" : ["Jazz & Blues", "Pop & Contemporary", "Brazil, Musicians", "Asia, Musicians", "Actors & Actresses (Latin America)", "Latin American, Musicians", "European, Musicians", "World, Musicians", "Turkish, Musicians", "Classic Funk, Soul & R & B", "Hip Hop, Rap, Soul & R&B", "Kpop", "Country & Folk", "Alternative, Grunge, Punk, & New Wave", "Electronic and Experimental", "Musicians & Music Critics", "Session Musicians", "Musical Theater", "Africa, Musicians", "Indie and Other", "Rock (Other)", "Classical", "Classic Rock", "Music Producers & Engineers", "Hard Rock & Heavy Metal", "Classic Pop & Contemporary"],
"Politics" : ["Government (Europe)", "Government (Middle East)", "Government (USA)", "Government (Africa)", "Government (Latin America)", "Government (Asia)", "Government (World)", "Presidents of the USA", "Political Commentators", "Umpires and Referees ", "Other Contemporary Political Figures", "Historical Figures (1000s)", "Historical Figures (100's)", "Royal Family (World)"],
"Sports and Games" : ["Ice skating", "Frisbee", "Climbing", "Track & Field", "Skiing & Snowboarding", "Cycling", "Rugby", "Boxing", "Snooker", "Table Tennis", "Motorsport", "Weightlifting & Strongmen", "Hockey", "Tennis", "Swimming & Diving", "Skateboarding", "Volleyball", "Wrestling (The Performers)", "Gymnastics", "Cricket", "Baseball", "Football (American)", "Football (Soccer)", "Martial Arts", "Wrestling", "Bodybuilding", "MMA", "Basketball", "Autosport", "Umpires and Referees", "Gaming", "Other Talented Individuals", "Poker"],
"Philosophy" : ["Western Philosophy"],
"Literature" : ["Writers (Literature, Modern)", "Writers (Literature, Classic)"],
"Architecture" : ["Architects & Designers"],
"Physics" : ["Physics & Astronomy"],
"Software Development" : ["Game Development", "Computer Science"],
"Graphic Designers" : ["Artists (Animators)", "Artists (Comics)"],
"Culinary" : ["Culinary Arts"],
"Journalism" : ["News & Journalists"],
"Content Creation" : ["Niche Content Creators", "Scientists, Technology & Educators","General Vloggers", "Virtual Youtubers"],
"Religion" : ["Christian and Other Religious", "New Religious Movements", "Christianity", "Buddhism", "Hinduism", "Religion & Spirituality"],
"Social Commentary" : ["Social, Cultural & Political Commentators"],
"Psychology" : ["Psychology & Neuroscience", "Psychology & Personal Development"],
"Biology and Medicine" : ["Biology & Medicine "],
"Teaching" : ["Educators"],
"Fashion" : ["Fashion Designers", "Health, Food, Beauty, Fashion & Lifestyle"],
"Business" : ["Business"],
"Other" : ["Renaissance Men", "Native American", "Tycoons of the Past", "Shinto", "Mystery, Horror & True Crime"],
"Modeling" : ["Models"],
"Acting and Entertainment" : ["Actors and Actresses (UK & Ireland)", "Artists", "People of Classic Hollywood", "TikTok Stars", "Artists & Animators", "ASMR Artists", "Buzzfeed Employees", "Voice Acting", "Actors & Actresses (Canada)", "Actors & Actresses (Oceania)", "Actors & Actresses (Europe)", "Actors and Actresses (USA)", "Actors & Actresses (Asia)", "Characters of Brandon Rogers", "Hosts, Critics, Producers & Editors", "Hosts, Analysts & Commentators", "Hosts & Presenters", "Performers", "Actors & Actresses (World)", "Comedians", "Comedy & Novelty", "Movie Composers", "Film Directors", "Film & TV Crew"],
"REPLACE THIS Historical Figure" : ["Historical Figures (1100s)", "Historical Figures (1700s)","Historical Figures (600s)","Historical Figures (1200s)","Nordic-Scandinavian","Historical Figures (1800s)","Historical Figures (700s)","Missionaries & Preachers","Historical Figures (1st Millenium BCE)","Historical Figures (500s)","Historical Figures (1st Century CE)","Historical Figures (1600s)","Historical Figures (1400s)","Historical Figures (1300s)","Early Islamic Figures","Greco-Roman","Biblical Figures","Historical Figures (200's)","Historical Figures (1500s)","Biographical"],
"DROP IT" : ["VOCALOID","Internet Personalities (Other)","Famous For Being Famous", "Welsh, Gaelic or Celtic", "International Leaders", "Indo-European", "Robin Hood Mythos", "Online Fictional Characters", "Animated/Fictional Musicians", "Without a Category", "Mesopotamian", "Egyptian"]
}


# print(sheet_esfp[1].where(sheet_esfp[1].values=='Hip Hop, Rap, Soul & R&B'))

def simplify_career_names(x, careers:dict):
    """Replace career names with general/simplified name provided."""
    
    for simplified_name, related_careers in careers.items():
        if x in related_careers:
            return simplified_name
    return x

# simplify career names
sheet_esfp[1] = sheet_esfp[1].apply(simplify_career_names, args=(careers_dict,))

# find words that are not present in career dictionary
present_in_dict = []
for career_in_sheet in careers:
    for careers_list in careers_dict.values():
        if career_in_sheet in careers_list:
            present_in_dict.append(career_in_sheet)
            break

not_present_in_dict = list( careers - set(present_in_dict) )


# add individuals' data
with open('individuals data.json','r') as f:
    individuals_data = json.load(f)
    
for person, career in individuals_data.items():
    sheet_esfp.loc[sheet_esfp[0]==person, 1] = career

# drop rows with specific career names
drop_rows_filter = (sheet_esfp[1]=="REPLACE THIS Historical Figure") | (sheet_esfp[1] == "DROP IT")
sheet_esfp.drop(index = sheet_esfp[drop_rows_filter].index, inplace=True)


sheet_esfp.to_excel('esfp data.xlsx', header=False, index=False)

# =============================================================================
# Find extra elements
# all_careers_in_dict = []
# for careers in careers_dict.values():
#     all_careers_in_dict.extend(careers)
#     
# diff = set(all_careers_in_dict).difference(set(present_in_dict))
# print(diff)
# 
# =============================================================================




    
