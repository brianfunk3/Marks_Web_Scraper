import pandas as pd
from bs4 import BeautifulSoup
import re
import os

def parse_html():
    """the big boi workhouse of this lil project. some beautiful soup magic takes the 
    raw html files saved out from scraping and puts it into a readable dataframe and
    then saves that out to a .csv file that i will use for the main analysis down the road."""
    # create a list of lists that will hold our data
    round_names, round_nums, ids, songs, artists, submitters, voters, votes, comments = ([] for i in range(9))

    # iterate through each round's html file
    for round_file in os.listdir('./tmp/'):
    
        # read the file in as a soup object
        with open(f'./tmp/{round_file}') as f:
            soup = BeautifulSoup(f, 'lxml')

        # now pull the specific div tag that includes all the relevant round data
        round_data = soup.find_all('div', {'class', 'mt-3'})[0].contents[0]

        # first pull the round name and description
        week_name = round_data.find('h5').text
        week_description = round_data.find('p').text
        round_num = re.search('round_(\d+)', round_file).group(1)

        # now loop through all the children of round_data, most of which are songs
        for tag in round_data.contents:
            # first we need to make sure we have a real tag and not a blank string thing
            if tag.name:
                # we need to skip the round name + description container at the top of the page...
                #     i noticed these don't have <span> tags so that's my janky solution to skip them
                if tag.span:
                    # alright, now we can start looping through each song!
                    for elem in tag.contents:
                        # again make sure it's a real tag
                        if elem.name:
                            # we will pull data based on random classes that i discovered
                            # 1. if the div has a class of 'bg-white', we can get the song title/artist
                            if 'bg-white' in elem.attrs['class']:
                                # get all the span tags
                                spans = elem.find_all('span')

                                # now we can pull our the info we want
                                artist = spans[0].text
                                album = spans[2].text
                                song = elem.a.text
                                song_link = elem.a.attrs['href']

                                # get the spotify id from the song link
                                song_id = re.search(pattern = 'https:\/\/open.spotify.com\/track\/(.+)',
                                                    string = song_link).group(1)

                                # we don't want to create a row yet
                                continue

                            # 2. if the div has a class of 'mt-4', it's the person submitting and their description
                            elif 'mt-4' in elem.attrs['class']:
                                # pull out the entire string "Submitted by ..."
                                submitter_raw = elem.select('span.fs-6')[0].text

                                # now regex the name out of that string
                                submitter = re.search('Submitted by (.+)', submitter_raw).group(1)

                                # again we don't want to create a row yet
                                continue

                            # 3. all other rows are people voting and/or commenting
                            elif 'row' in elem.attrs['class']:
                                # get the voter's name
                                voter = elem.select('span.fs-6')[0].text

                                # get how many votes they spent, if any
                                n_votes = elem.find_all('span', {'class', ''})

                                # check if someone left comments but no votes
                                if not n_votes: 
                                    # if so, make that zero
                                    n_votes = 0
                                # if they did vote, get their votes and turn the +x string into an integer
                                else:
                                    n_votes = int(n_votes[0].text[1:])

                                # try and pull any comments they left
                                comment = elem.find_all('span', {'class', 'text-break'})

                                # same thing - check if they voted but left no comments
                                if not comment:
                                    comment = ''
                                # now grab the real comments
                                else:
                                    comment = comment[0].text

                                # we can now add all this data into our lists
                                round_names.append(week_name)
                                round_nums.append(round_num)
                                songs.append(song)
                                ids.append(song_id)
                                artists.append(artist)
                                submitters.append(submitter)
                                voters.append(voter)
                                votes.append(n_votes)
                                comments.append(comment)
                            # 4. else idk what is going on
                            else:
                                print('how did you get here?')

    # make this into a pandas df
    df = pd.DataFrame(list(zip(round_nums, round_names, ids, songs, artists, submitters, voters, votes, comments)), 
                       columns = ['round_num', 'round_name', 'song_id', 'song', 'artist', 'submitter', 'voter', 'votes', 'comments'])

    # save 'er out
    df.to_csv('voting_data.csv', index = False)

    return