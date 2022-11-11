import requests
import json
import os
import time
import glob


def inputYOrN(prompt):
    while(True):
        yOrN = input(prompt + ' y or n: ')
        if yOrN == 'y' or yOrN == 'n':
            print('알았다잉')
            if(yOrN == 'y'):
                return True
            else:
                return False
        else:
            print('마! 똑바로 입력 해라')
def searchBeatmapsetId(id):
    headers = {'Content-Type' : 'application/json'}
    response = requests.get(f'https://api.nerinyan.moe/search?option=s&q={id}', headers=headers)
    return response
def downloadBeatmap(beatmapInfo, id):
    global video
    artist = beatmapInfo[0]['artist']
    title = beatmapInfo[0]['title']
    filename = str(id) + ' ' + artist + ' - ' + title
    if glob.glob(f'songs\\{id}*'):
        print(filename, '이미 있어서 스킵!!!!')
        return
    headers = {'Content-Type' : 'application/json'}
    response = requests.get(f'https://api.nerinyan.moe/d/{id}?nv={video}', headers = headers)
    if response.status_code == 200:
        try:
            with open('songs\\' + filename + '.osz', 'wb') as f:
                f.write(response.content)
            time.sleep(0.5)
            print(filename, '다운로드 오와리다')
        except:
            print(filename, '다운로드 실패!')
    elif response.status_code == 404:
        print(filename, '비트맵 파일이 없어요!')
    elif response.status_code == 500:
        print('인터넷이 이상한 거 같아요')


min  = int(input('비트맵 셋 아이디 최소값을 입력해요: '))
max = int(input('비트맵 셋 아이디 최댓값을 입력해요 : '))
loved = inputYOrN('럽드도 받을꺼냐?')
video = inputYOrN('배경동영상 받을꺼냐?')

for id in range(min, max + 1):
    response = searchBeatmapsetId(id)
    if response.status_code == 404:
        continue
    elif response.status_code == 500:
        print('인터넷 연결이 이상해요오오오')
        continue
    elif response.status_code == 200 :
        beatmapInfo = json.loads(response.content)
        if beatmapInfo[0]['ranked'] == 1 or (beatmapInfo[0]['ranked'] == 4 and loved == True):
            downloadBeatmap(beatmapInfo, id)
                
        
        

