from gtts import gTTS
import pygame
import os


def final_play_sound(text):
    save_mp3_name = "temp.mp3"
    tts = gTTS(text, lang='zh-CN')
    tts.save(save_mp3_name)

    pygame.mixer.init()
    sound = pygame.mixer.Sound(save_mp3_name)
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)

    pygame.quit()

    if os.path.exists(save_mp3_name):
        os.remove(save_mp3_name)
        print(f"文件 {save_mp3_name} 已删除")
    else:
        print(f"文件 {save_mp3_name} 不存在")
