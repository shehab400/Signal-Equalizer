from pydub import AudioSegment
import pydub
# enter the path of your audio file
sound1 = AudioSegment.from_mp3("Metro Boomin, A$AP Rocky, Roisee - Am I Dreaming Piano Tutorial.mp3")
sound2 = AudioSegment.from_mp3("Metro Boomin - Am I Dreaming (Instrumental)_other_mixed.mp3")
sound3 = AudioSegment.from_mp3("Metro Boomin - Am I Dreaming (Instrumental)_bass_mixed.mp3")
sound4 = AudioSegment.from_mp3("Metro Boomin - Am I Dreaming (Instrumental)_drums_mixed.mp3")

def choose_option():
	print("Audio file editing by pydub Package\n")
	print("1. Audio Cut ") 
	print("2. Sound Increase and Decrease") 
	print("3. Merge Two Songs") 
	choose = int(input("Choose Option = "))
	if choose == 1:
		audio_cut()
	elif choose == 2:
		sound_Increase() 
	elif choose == 3:
		merge_two_songs()
	elif choose >3:
		print("You Choose Wrong Input") 

def audio_cut():

	StrtMin = int(input("Enter the Start Min " ))
	StrtSec = int(input("Enter the Start Sec ")) 

	EndMin = int(input("Enter the End Min "))
	EndSec = int(input("Enter the End Sec "))

	sound2 = int(input("Sound Increase or Sound Decrease example 5 or -5 "))

	StrtTime = StrtMin*60*1000+StrtSec*1000
	EndTime = StrtMin*60*1000+EndSec*1000

	print("Extracting Sound from your audio file")
	extract = sound[StrtTime:EndTime]

# Saving file in required location
def sound_Increase():
	if sound2>=0:
		loudmusic = extract + sound2 
		loudmusic.export("/home/dachman/Desktop/walker2.mp3", format="mp3")
	else:
		lowmusic = extract - sound2 
		lowmusic.export("/home/dachman/Desktop/walker2.mp3",format="mp3")

# merge two audio
def merge_two_songs():
	print("Sound Overlay")
	sound1 = sound1 + 10
	sound5 = sound1.overlay(sound2,position=0)
	sound5 = sound5.overlay(sound3,position=0)
	sound5 = sound5.overlay(sound4,position=0)
	sound5.export("merge_sound.mp3",format="mp3")

choose_option()
