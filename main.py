import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import numpy as np

def searchpeaks():
    print('データが保存されているフォルダのパスを入力してください：')
    folder_path = str(input())
    if (not os.path.exists(folder_path)) or (not os.path.isdir(folder_path)):
        print("フォルダが存在しません。最初に戻ります!!\n")
        return

    peakdictlist = []
    for root, _, filelist in os.walk(folder_path):
        if len(filelist):
            for filename in filelist:
                if filename == '.DS_Store' or filename == 'log.txt':
                    continue
                filepath = os.path.join(root, filename)
                try:
                    df = pd.read_csv(filepath, sep='\t', comment='#', header=None)
                except:
                    print(f"{filepath}はCSVファイルではありません。次のファイルを読み込みます")
                    continue
                peakdictlist.append({'filepath': filepath, 'peak': df[1].max()})
        else:
            print(f"{root}にファイルが存在しません。次のフォルダを読み込みます")
            continue

    sorted_peakdictlist = sorted(peakdictlist, key=lambda x: x['peak'])
    sorted_peakdictlist = sorted_peakdictlist[::-1]

    print("何番目までのピークを表示しますか？")
    while True:
        try :
            num_peaks = int(input())
            break
        except:
            print('数字だけを正しく入力してください。')
    num_peaks = min(num_peaks, len(sorted_peakdictlist))

    for i, peakdict in enumerate(sorted_peakdictlist[:num_peaks]):
        print(f"{i+1}番目にピークが高いファイル：{peakdict['filepath']}，ピーク値：{peakdict['peak']}")

def pekaimaging():
    print('データが保存されているフォルダのパスを入力してください：')
    folder_path = str(input())
    if (not os.path.exists(folder_path)) or (not os.path.isdir(folder_path)):
        print("フォルダが存在しません。最初に戻ります!!\n")
        return
    folderdict = {}
    for foldername in os.listdir(folder_path):
        if not os.path.isdir(os.path.join(folder_path, foldername)):
            continue
        id = int(foldername.split('_')[0][3:])#_で分けて一番前 → さらに文字列posを飛ばす
        folderdict[id] = foldername

    folderdict = dict(sorted(folderdict.items(), key=lambda x: x[0]))

    map = []
    for id, foldername in folderdict.items():
        maxv = 0
        for filename in os.listdir(os.path.join(folder_path, foldername)):
            if filename == '.DS_Store' or filename == 'log.txt':
                continue
            filepath = os.path.join(folder_path, foldername, filename)
            try:
                df = pd.read_csv(filepath, sep='\t', comment='#', header=None)
            except:
                print(f"{filepath}はCSVファイルではありません。次のファイルを読み込みます")
                continue
            maxv = max(maxv, int(df[1].max()))
        map.append(maxv)
    map = np.array(map)
    map = map[np.newaxis, :]
    plt.imshow(map, cmap='jet')
    plt.colorbar()
    plt.show()

if __name__ =='__main__':
    while True:
        print('フォルダ内を探索してピーク値が高いファイルを表示する場合はsをピーク値でイメージングを行う場合はiを入力してください．')
        try:
            mode = str(input())
        except:
            print('sまたはiを入力してください。')
        else:
            if mode == 'i':
                pekaimaging()
            elif mode == 's':
                searchpeaks()
            else:
                print('sまたはiを入力してください。')
        time.sleep(1)