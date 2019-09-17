import os
import pydub
from pydub import AudioSegment
from pydub.utils import mediainfo

def normalize(sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        print("The dBFS is", sound.dBFS)
        if (abs(change_in_dBFS) < 1):
            return sound
        return sound.apply_gain(change_in_dBFS)

def dbfs(file, sec = 0):
        sound = AudioSegment.from_file(file, "mp3")
        if (sec != 0):
            sound = sound[:(sec * 1000)]
        print(sound.dBFS)

silence = AudioSegment.silent(2000)

if(os.path.exists("Music")):
    if (not os.path.exists("Edited")):
        os.mkdir("Edited")
    db = float(input("Now load do you want your music? (-10 to -15 is normal)? "))
    for file in os.listdir("Music"):
        if file.endswith(".mp3"):
            print(file)
            original_bitrate = mediainfo("Music/" + file)['bit_rate']
            print("Bit rate is", original_bitrate)
            sound = AudioSegment.from_file("Music/" + file, "mp3")
            temp = sound[:2000]
            if (temp.dBFS < -500):
                for sec in range(2000, 8000, 500):
                    temp = sound[:sec]
                    if (temp.dBFS > -50):
                        sound = sound[sec - 500:]
                        print((sec - 500)/1000.0, "seconds have been edited off the beginning")
                        break
            temp = sound[-100:]
            if (temp.dBFS < -50):
                for sec in range(100, 8000, 50):
                    temp = sound[-sec:]
                    if (temp.dBFS > -80):
                        sound = sound[:-(sec - 50)]
                        print((sec + 50)/1000.0, "seconds have been edited off the end")
                        break
            sound = sound + silence
            sound = normalize(sound, db)
            sound.export("Edited/" + file, "mp3")
            print(file + " is done\n")

    print("Everything is done")
else:
    os.mkdir("Music")
    print("The Music folder has been created")
input()
