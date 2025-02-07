import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from matplotlib.colors import Normalize
import re

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

def lenimaging():
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

    print('当該フォルダには以下のようにファイルが格納されています。')
    for id, foldername in folderdict.items():
        ex_ind = 1
        for fn in os.listdir(os.path.join(folder_path, foldername)):
            if fn == '.DS_Store' or fn == 'log.txt':
                continue
            print(f'{ex_ind}番目: {fn}')
            ex_ind += 1
        break
    print('何番目のファイルをイメージングに使用しますか？')
    ind = int(input())

    #フォルダ名から測定地点の順番と座標を取得
    xlist = []
    for id, foldername in folderdict.items():
        listfoldername = foldername.split('_')
        pos_ind = int(re.sub(r'pos', '', listfoldername[0]))
        if pos_ind == 0:
            gx = int(re.sub(r'x', '', listfoldername[1]))
            gy = int(re.sub(r'y', '', listfoldername[2]))
            break

    map = []
    for id, foldername in folderdict.items():
        fnlist = []
        for fn in os.listdir(os.path.join(folder_path, foldername)):
            if fn == '.DS_Store' or fn == 'log.txt':#macの不要ファイルや測定のログファイルを除外
                continue
            fnlist.append(fn)
        fnlist = sortbylength(fnlist)
        filename = fnlist[ind-1]
        filepath = os.path.join(folder_path, foldername, filename)
        try:
            df = pd.read_csv(filepath, comment='#', header=None)
        except:
            print(f"{filepath}はCSVファイルではありません。次のファイルを読み込みます")
            continue
        data = df[1].to_numpy()
        map.append(data)

        listfoldername = foldername.split('_')
        x = int(re.sub(r'x', '', listfoldername[1]))
        y = int(re.sub(r'y', '', listfoldername[2]))
        xlist.append(np.linalg.norm(np.array([x-gx, y-gy])) / 100) #現段階ではpriorの内部単位をフォルダ名に用いている．100[internal unit] = 1[um]
    #x = np.arange(len(map))
    x = np.array(xlist)
    y = df[0].to_numpy()
    X, Y = np.meshgrid(x, y)
    map = np.array(map)
    Z = map.T

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, aspect='equal')
    contour = ax.pcolormesh(X, Y, Z, cmap='jet', shading='nearest', norm=Normalize(vmin=0, vmax=1300))

    # カラーバー調整用
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    pp = fig.colorbar(contour, cax=cax, orientation='vertical')

    ax.set_xlabel('distance from start point [$\mu$m]')
    ax.set_ylabel('Emission Wavelength [nm]')
    #ax.grid()
    plt.show()

def sortbylength(strlist: list) -> list:
    return sorted(strlist, key=len)

if __name__ =='__main__':
    while True:
        print('フォルダ内を探索してピーク値が高いファイルを表示する場合は「s」\nピーク値でイメージングを行う場合は「max」\n先頭ファイルでイメージングする場合は「i」\nバックグラウンドを引いてイメージングをする場合は「bgi」を\nフォルダ内におけるファイル名の長さの順番を指定してイメージングする時は「leni」を終了するときはq\nを入力してください．')
        try:
            mode = str(input())
        except:
            print('s，max，i, bgiを入力してください。')
        else:
            if mode == 'i':
                imaging()
            elif mode == 'bgi':
                bgimaging()
            elif mode == 's':
                searchpeaks()
            elif mode == 'max':
                peakimaging()
            elif mode == 'leni':
                lenimaging()
            elif mode == 'q':
                break
            else:
                print('sまたはiを入力してください。')
        time.sleep(1)