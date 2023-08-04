import shutil
import os
import sys
import re

def copyFile(commonOrClientPath,oldPath,newPath):
    tempOldPath = (commonOrClientPath + oldPath).replace('\\','/')
    tempNewPath = (commonOrClientPath + newPath).replace('\\','/')
    if not os.path.exists(tempOldPath):
        print("原始文件不存在：" + tempOldPath)
        return False
    if os.path.exists(tempNewPath) :
        print("新文件已存在：" + tempNewPath)
        return False
    shutil.copyfile(tempOldPath,tempNewPath)
    return True

themeId = input("请输入老的themeId:\n")
isReprint = input("是否是转换成reprint?Y or N to dark?\n")
if themeId.isdigit() :
    if int(themeId) < 150:
        print("themeId 必须大于150")
        os.system("pause")
else:
    print("必须输入一个数字")
    os.system("pause")

path = os.path.abspath("..")

stringCommonPath = path + '/Assets/ROT2Code/Lua/Common/Dungeon'
stringClientPath = path + '/Assets/ROT2Code/Lua/Client/Dungeon'

suffix = '.lua'

if isReprint.upper() == 'Y' :
    newThemeId = int(themeId) + 10
else:
    newThemeId = int(themeId) % 100
    
stringOldScene = '/DungeonScene/Scene/Scene' + themeId + suffix
stringOldAchievement = '/Achievement/Achievement' + themeId + suffix
stringOldReset = '/Theme/Reset/Reset' + themeId + suffix
stringOldTheme = '/Theme/Theme' + themeId + suffix

stringNewScene = '/DungeonScene/Scene/Scene' + str(newThemeId) + suffix
stringNewAchievement = '/Achievement/Achievement' + str(newThemeId) + suffix
stringNewReset = '/Theme/Reset/Reset' + str(newThemeId) + suffix
stringNewTheme = '/Theme/Theme' + str(newThemeId) + suffix

copyFile(stringClientPath,stringOldScene,stringNewScene)
copyFile(stringCommonPath,stringOldAchievement,stringNewAchievement)
copyFile(stringCommonPath,stringOldReset,stringNewReset)
copyFile(stringCommonPath,stringOldTheme,stringNewTheme)

createReplayPath = path + '/Assets/Editor/WorldDungeon/Test/Replay/T' + str(newThemeId)
createReplayPath = createReplayPath.replace('\\','/')
os.mkdir(createReplayPath)

os.system("pause")
