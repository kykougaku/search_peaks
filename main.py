import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
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

def peakimaging():
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

def imaging():
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
        for filename in os.listdir(os.path.join(folder_path, foldername)):
            if filename == '.DS_Store' or filename == 'log.txt':
                continue
            filepath = os.path.join(folder_path, foldername, filename)
            try:
                df = pd.read_csv(filepath, sep='\t', comment='#', header=None)
            except:
                print(f"{filepath}はCSVファイルではありません。次のファイルを読み込みます")
                continue
            data = df[1].to_numpy()
            map.append(data)
            break
    map = np.array(map)
    map = map.T
    fig = plt.figure(figsize=(10, 7), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    c = ax.imshow(map, cmap='jet', aspect='auto')
    plt.colorbar(c, cax=cax)
    plt.show()

# reverse background imaging
def bgimaging():
    print("ihr320分光器の中心波長を入力してください")
    try:
        center_wl = float(input())
    except:
        print("数字を入力してください。最初に戻ります!!\n")
        return
    print("backgroundファイルのパスを入力してください")
    try:
        bg_path = str(input())
        bg_df = pd.read_csv(bg_path, sep='\t', comment='#', header=None)
    except:
        print("backgroundファイルが存在しません。最初に戻ります!!\n")
        return
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
        for filename in os.listdir(os.path.join(folder_path, foldername)):
            if filename == '.DS_Store' or filename == 'log.txt':
                continue
            filepath = os.path.join(folder_path, foldername, filename)
            try:
                df = pd.read_csv(filepath, sep='\t', comment='#', header=None)
            except:
                print(f"{filepath}はCSVファイルではありません。次のファイルを読み込みます")
                continue
            df[1] = df[1] - bg_df[1]
            df_reverse = df.iloc[::-1]
                    #x軸にラフな値を代入する処理
            list_wl = []
            # start_wl = center_wl - 319 #319は過去の結果からの概算結果
            start_wl = center_wl - 246  #246は過去の結果からの概算結果
            delta_wl = 509.5 / 511
            for j in range(512):
                list_wl.append(start_wl + delta_wl * j)
            df_reverse[0] = list_wl
            data = df_reverse[1].to_numpy()
            map.append(data)
            break
    map = np.array(map)
    map = map.T
    fig = plt.figure(figsize=(10, 7), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    c = ax.imshow(map, cmap='jet', aspect='auto')
    plt.colorbar(c, cax=cax)
    plt.show()

if __name__ =='__main__':
    while True:
        print('フォルダ内を探索してピーク値が高いファイルを表示する場合はs\nピーク値でイメージングを行う場合はmax\n先頭ファイルでイメージングする場合はi\n終了するときはq\nを入力してください．')
        try:
            mode = str(input())
        except:
            print('s，max，iを入力してください。')
        else:
            if mode == 'i':
                imaging()
            elif mode == 'bgi':
                bgimaging()
            elif mode == 's':
                searchpeaks()
            elif mode == 'max':
                peakimaging()
            elif mode == 'q':
                break
            else:
                print('sまたはiを入力してください。')
        time.sleep(1)