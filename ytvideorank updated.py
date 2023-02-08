from googleapiclient.discovery import build
import pprint
from datetime import date, datetime
from tabulate import tabulate
import requests
query_count = 0
url_base = "https://www.googleapis.com/youtube/v3"
API_KEY = 'AIzaSyCaFODfXN5L3kw8uQhWObyAExLlwS8HqjE'
#youtube = build('youtube', 'v3', developerKey=API_KEY)

def id_to_rank(channel_id, max_age): #used
    vid_id_list = get_playlist_vid_id_list(channel_id)
    vid_info_list = get_vid_info_list(vid_id_list, max_age)
    rank_video_views(vid_info_list, max_age)

def elem1_func(vid):
    return vid[1]

def rank_video_views(vid_info_list, max_age): #used 3
    vid_info_list.sort(reverse=True, key = elem1_func)
    for i in range(len(vid_info_list)):
        vid_info_list[i][1] = "{:,}".format(vid_info_list[i][1])
        vid_info_list[i][2] = "youtube.com/watch?v=" + vid_info_list[i][2]
        vid_info_list[i].insert(0, i+1)
        
        
    end_time = datetime.now()
    print('Ranking complete: {} \n'.format(end_time - start_time))
    if max_age == 'all':
        print("Top videos:")
    else:
        print("Top videos from the past {} day{}:".format(max_age, '' if max_age == 1 else ''))
    print(tabulate(vid_info_list, headers=["Name", "Views", "Link", "Age in Days", "Release Date"]))
    print("Query count: ", query_count)



def get_vid_info_list(vid_id_list, max_age): #ACTIVE (2) used 2
    vid_info_list = []
    url = f'{url_base}/videos'
    
    params = {
        'key': API_KEY,
        'part' : ['statistics', 'snippet']
        #'id' : elem
        }
    for elem in vid_id_list:
        params['id'] = elem
        data = requests.get(url, params = params).json()
        #item = youtube.videos().list(part=['statistics', 'snippet'], id = elem).execute() #------------
        global query_count
        query_count += 1

        try:
            index_view_count = int(data['items'][0]['statistics']['viewCount'])
        except: #if youtube original, no view count
            continue
        
        index_title = data['items'][0]['snippet']['title']
        i_date = data['items'][0]['snippet']['publishedAt']
        
        converted_date = date(int(i_date[0:4]), int(i_date[5:7]), int(i_date[8:10]))
        age_in_days = (date.today() - converted_date).days

        if max_age != 'all':
            if age_in_days > max_age:
                break

        vid_info_list.append([index_title, index_view_count, elem, age_in_days, converted_date])

    end_time = datetime.now()
    print('All video data: {}'.format(end_time - start_time))
    
    return vid_info_list

    
def get_playlist_vid_id_list(playlistId): #ACTIVE (1) also used 2

    next_page_token = None
    vid_id_list = []
    params = {"key" : API_KEY,
    'part' : 'snippet',
    'playlistId' : playlistId,
    'max_results' : 50,
    }
    url = f'{url_base}/playlistItems'
    
    while True:
        params['pageToken'] = next_page_token
        data = requests.get(url, params = params).json()
        
        '''
        data = youtube.playlistItems().list(part='snippet',
                                           playlistId = playlistId,
                                           maxResults = 50,
                                           pageToken = next_page_token).execute() #1 QUOTA
        '''
        global query_count
        query_count += 1
        for i in range(len(data['items'])):
            vid_id_list.append(data['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = data.get('nextPageToken')
        
        if next_page_token == None:
            break
                   
    end_time = datetime.now()
    print('All video links: {}'.format(end_time - start_time))
    return vid_id_list

'''
def get_channel_info(channel_id):
    url = f'{url_base}/channels'
    params = {
        'key' : API_KEY,
        'part' : 'contentDetails',
        'id' : 'UCDogdKl7t7NHzQ95aEwkdMw'
    }
    data = requests.get(url, params = params).json()
    print(data)
'''
    
def get_channel_id_from_vid_id(vid_id):
    url = f'{url_base}/videos'
    params = {"key": API_KEY,
    'part': 'snippet',
    'id': vid_id
    }
    data = requests.get(url, params = params).json()
    channel_id = data['items'][0]['snippet']["channelId"]
    print(channel_id)
    playlist_id = channel_id[0] + "U" + channel_id[2:]
    return playlist_id

def main():
    vid_id = input('To select a channel, please input the video ID for one of their videos:\n')
    playlist_id = get_channel_id_from_vid_id(vid_id)
    valid_age = False
    while not valid_age:
        max_age = input("How old in days is the last video? Type 'all' for all:\n")
        if max_age.isnumeric():
            max_age = int(max_age)
            valid_age = True
        elif max_age == 'all':
            valid_age = True
            
        else:
            print("Invalid age")
    global start_time
    start_time = datetime.now()
    id_to_rank(playlist_id, max_age)
main()

'''
Test link: fklHBWow8vE
'''
