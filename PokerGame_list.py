# -*- coding: utf-8 -*-

design_list = ["♡", "♢" ,"♤" ,"♧"]
hand_list = ["ブタ","ワンペア","ツーペア","スリーカード","ストレート","フラッシュ","フルハウス","フォーカード","ストレートフラッシュ","ロイヤルストレートフラッシュ","ファイブカード"]

card_list = []
for num in range(1,14):
    for design in design_list:
        card_list.append(str(num) + design)

rate_list_1 = [30,55,5,8,2,2,2,1,0,0,0]
rate_list_2 = [20,45,8,10,2,2,3,1,0,0,0]
rate_list_3 = [5,25,7,15,3,3,6,1,1,1,1]
rate_list_4 = [0,1,5,10,15,15,35,5,5,5,5]
rate_list = [rate_list_1,rate_list_2,rate_list_3,rate_list_4]