コードサンプル

```python
# -*- coding:utf-8 -*-

"""
Created on Nov. 16. 2018
@author: Takehiro Matsuda

機能：
動画リストファイル(txt)に記載されたファイルに対して、評価に用いるための教師データ(正解枠)の情報が
存在するかを確認する。

履歴：
ver.0.2 : 2018.12.13
教師データ(正解枠)があるファイル名のみの動画リストファイルを新たに作成する機能を追加する。

ver.0.1 : 2018.11.16
初期バージョン作成
"""

import os
import sys
import configparser
import csv

args = sys.argv
if len(args) == 1:
    paramFile = './ParamCheckTeacherDataExist.ini'
else:
    paramFile = args[1]

# 処理設定ファイルを読み出す
inifile = configparser.ConfigParser()
inifile.read(paramFile, 'utf-8')

# 入力の動画ファイル名リスト
inputListFile = inifile['Files']['inputListFile']

# 探索対象の教師データファイルが保存されているフォルダの個数
teacherDataFolderNum = int(inifile['Files']['teacherDataFolderNum'])

# 教師データファイルが保存されているフォルダ
teacherDataFolders = []
for i in range(1, teacherDataFolderNum+1):
    teacherDataFolderName = 'teacherDataFolder' + str(i)
    teacherDataFolders.append(inifile['Files'][teacherDataFolderName])

# リストの動画ファイルに教師データのあるなしのチェックをつけた出力ファイル
outputListCheckFile = inifile['Files']['outputListCheckFile']

outputFolder, _ = os.path.split(outputListCheckFile)
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# リストの動画ファイルについて、いくつ教師データが存在したか記載する出力ファイル
outputTeacherExistNumFile = inifile['Files']['outputTeacherExistNumFile']

outputFolder, _ = os.path.split(outputTeacherExistNumFile)
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# 教師データがあるファイルのみの動画ファイルリストを新たに出力するときの出力ファイル名
outputExistListFile = inifile['Files']['outputExistListFile']

outputFolder, _ = os.path.split(outputExistListFile)
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

existListFile = open(outputExistListFile, 'w', encoding='shift-jis')

with open(inputListFile, 'r', encoding='shift-jis') as f:
    listData = f.readlines()
    teacherExistNum = 0
    # チェックした結果を出力するファイルを開く
    with open(outputListCheckFile, 'w', encoding='shift-jis') as writeListFile:
        # リストはスペース区切りで記載されており、「ファイルパス　開始フレーム番号　終了フレーム番号」となっている
        for line in listData:
            fileInfo = line.split()
            filePath = fileInfo[0]
            # ファイル名を取得する
            folderPath, fileName = os.path.split(filePath)
            # ファイル名を拡張子と分離する
            fileNoExtName, fileExtName = os.path.splitext(fileName)

            # 教師データファイルの名前
            teacherFileName = fileNoExtName + '_Cor.csv'

            # 入力リストデータを出力データに記述する
            writeListFile.write(line.strip('\r\n'))

            # 教師データファイルが存在するか確認する
            teacherExistFlg = False
            for teacherFolder in teacherDataFolders:
                teacherFilePath = os.path.join(teacherFolder, teacherFileName)
                if os.path.isfile(teacherFilePath):
                    teacherExistFlg = True

            # チェックした結果を出力する
            if teacherExistFlg:
                writeListFile.write(' o\n')
                teacherExistNum += 1
                existListFile.write(line)

            else:
                writeListFile.write(' x\n')

    with open(outputTeacherExistNumFile, 'w', encoding='shift-jis') as writeNumFile:
        outputStr = '教師データ存在数: {exist} / {all}\n'.format(exist=teacherExistNum, all=len(listData))
        writeNumFile.write(outputStr)

existListFile.close()
print('Process done.')
```


