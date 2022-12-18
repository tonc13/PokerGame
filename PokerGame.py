# -*- coding: utf-8 -*-
import random
import time
import PokerGame_list

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    #山札の生成
    def create_deck(self):
        for num in range(1,14):
            for design in PokerGame_list.design_list:
                self.cards.append(str(num) + design)

    #ジョーカーの追加
    def add_joker(self,num):
        for _ in range(num):
            self.cards.append("Joker")

class Hand:
    def __init__(self):
        self.only_hand = "ブタ" #手役
        self.only_num = 0 #役の数
        self.hand = "" #手役+数

class PlayerHand(Hand):
    def __init__(self):
        self.cards = [] #手札
        super().__init__()
        self.add_cards(5)

    #手札の追加
    def add_cards(self, num):
        for _ in range(num):
            i = random.randint(0,len(deck.cards)-1)
            self.cards.append(deck.cards[i])
            deck.cards.pop(i)
        self.organize_cards()

    #手札の削除
    def del_cards(self, loc_list): #loc_listの例:[1,2,4](1,2,4番目のカードを捨てる)
        loc_list = [i-1 for i in loc_list] #pythonの添字は0から始まるため
        for loc in reversed(loc_list): #前から削除すると後ろの位置(添字)がずれるため
            self.cards.pop(loc)

    #手札の整理
    def organize_cards(self):
        cards_1 = sorted([card for card in self.cards if len(card) == 2]) #数字が1桁のカード
        cards_2 = sorted([card for card in self.cards if len(card) == 3]) #数字が2桁のカード
        cards_loker = [card for card in self.cards if len(card) == 5] #ジョーカーのカード
        self.cards = cards_1 + cards_2 + cards_loker

    #手札の交換
    def change_cards(self,loc_list):
        num = len(loc_list)
        self.del_cards(loc_list)
        self.add_cards(num)
        self.organize_cards()
    
    #手札から役を判断する
    def confirm_hand(self):
        if self.cards.count("Joker") == 0:
            self.confirm_hand_no_joker()
        elif self.cards.count("Joker") == 1:
            self.cards.pop(4)
            for card in PokerGame_list.card_list:
                self.cards.append(card)
                self.organize_cards()
                self.confirm_hand()
                self.cards.remove(card)
        elif self.cards.count("Joker") == 2:
            self.cards.pop(4)
            self.cards.pop(3)
            for card_1 in PokerGame_list.card_list:
                for card_2 in PokerGame_list.card_list:
                    self.cards.append(card_1)
                    self.cards.append(card_2)
                    self.organize_cards()
                    self.confirm_hand()
                    self.cards.remove(card_1)
                    self.cards.remove(card_2)

    #手札から役を判断する(ジョーカーがない場合)
    def confirm_hand_no_joker(self):
        designs = []
        numbers = []
        hand_record = [True, False, False, False, False, False, False, False, False, False, False]
    
        #手札のカードを数と絵柄に分ける
        for card in self.cards:
            design = card[-1]
            number = int(card[:-1])
            designs.append(design)
            numbers.append(number)
        num = max(numbers)

        #フラッシュかどうかを判断する
        for design in designs:
            confirm_list = [design] * 5
            if designs == confirm_list:
                hand_record[5] = True
        
        #ストレートかどうかを判断する
        for a in range(1,14):
            confirm_list = []
            for b in range(5):
                c = a + b
                if c > 13:
                    c = c - 13
                confirm_list.append(c)
            if sorted(numbers) == sorted(confirm_list):
                hand_record[4] = True

        #(ロイヤル)ストレートフラッシュかどうかを判断する
        if (hand_record[4] and hand_record[5]) == True:
            if (10 in numbers) and (1 in numbers) == True:
                hand_record[9] = True
            else:
                hand_record[8] = True

        #数字のダブりがあるかどうかを判断する
        same_count = 1
        for i in range(1,14):
            if same_count < numbers.count(i):
                same_count = numbers.count(i)
                num = i
        if same_count == 2:
            hand_record[1] = True
        if same_count == 3:
            hand_record[3] = True
        if same_count == 4:
            hand_record[7] = True
        if same_count == 5:
            hand_record[10] = True

        #スリーカードがある場合に、フルハウスかどうか判断する
        if hand_record[3] == True:
            for i in range(1,14):
                if numbers.count(i) == 2:
                    hand_record[6] = True

        #ワンペアがある場合に、ツーペアかどうかを判断する
        if hand_record[1] == True:
            pair_count = 0
            for i in range(1,14):
                if numbers.count(i) == 2:
                    pair_count += 1
                    if i > num : num = i
            if pair_count == 2:
                hand_record[2] = True

        #hand_recordから役を判断する
        for i in reversed(range(11)):
            if hand_record[i] == True:
                if i == 9:
                    self.only_hand = PokerGame_list.hand_list[9]
                    self.hand = PokerGame_list.hand_list[9]
                    return
                else:
                    if i > PokerGame_list.hand_list.index(self.only_hand):
                        self.only_hand = PokerGame_list.hand_list[i]
                        self.only_num = num
                        self.hand = str(num) + "の" + PokerGame_list.hand_list[i]
                    elif i == PokerGame_list.hand_list.index(self.only_hand):
                        if num > self.only_num:
                            self.only_num = num
                            self.hand = str(num) + "の" + PokerGame_list.hand_list[i]
                    return

class CpuHand(Hand):
    def __init__(self):
        super().__init__()
    
    #CPUの役決め
    def decide_hand(self, level):
        rate_list = PokerGame_list.rate_list[level-1]
        hand = self.gen_prop(PokerGame_list.hand_list, rate_list)
        if hand == "ロイヤルストレートフラッシュ":
            self.only_hand = hand
            self.hand = hand
        else:
            if hand == "ストレートフラッシュ" or "ストレート" or "フラッシュ": #この三つの役の場合は五枚のカードの中で一番高い数字で競うため
                num = random.randint(6,13)
            else:
                num = random.randint(1,13)
            self.only_hand = hand
            self.only_num = num
            self.hand = str(num) + "の" + hand

    #役の割合を示すリストから乱数によって役を決定
    def gen_prop(self, hand_list, rate_list):
        r = random.uniform(0,sum(rate_list))
        S = 0
        for i in range(0,len(rate_list)):
            S += rate_list[i]
            if r < S:
                return hand_list[i]
        return hand_list[-1]

class Host:
    def __init__(self):
        self.mode_flag = 0 #プレイするモード
        self.flag = 0 #プレイヤーの入力による「するかしないか」の条件分岐
        self.first = True #初回かどうかの判定

        self.level = -1 #cpuのレベル
        self.change = -1 #手札の交換回数
        self.joker = -1 #ジョーカーの枚数
        self.count = 0 #手札交換をした回数

    #起動時のメッセージ
    def PokerGame(self):
        print("ポーカーゲームにようこそ!")
        print()
        self.choice_mode()

    #モード選択
    def choice_mode(self):
        while self.mode_flag not in [1,2,3,4,5]:
            try:
                time.sleep(0.8)
                print("モードを選択してください。")
                print(" 1.ポーカーをプレイ(通常)")
                print(" 2.ポーカーをプレイ(勝ち抜き戦)")
                print(" 3.クレジットを表示")
                print(" 4.モードの説明を表示")
                print(" 5.終了")
                self.mode_flag = int(input("入力:"))
            except:
                print("正しい入力ではありません")
            else:
                if self.mode_flag == 1:
                    print("分かりました")
                    print()
                    self.simple_poker()
                elif self.mode_flag == 2:
                    print("分かりました")
                    print()
                    self.tournament_poker()
                elif self.mode_flag == 3:
                    print("分かりました")
                    print()
                    self.credit()
                elif self.mode_flag == 4:
                    print("分かりました")
                    print()
                    self.ex_mode()
                elif self.mode_flag == 5:
                    print("分かりました")
                    print()
                    print("プレイしてくれてありがとうございました!")
                    return
                else:
                    print("正しい入力ではありません")

    #ポーカーをプレイ(通常)
    def simple_poker(self):
        continue_flag = True
        while continue_flag:
            host_poker.main()
            result.cul_winrate()
            print("現在の勝率は、{}%です({}勝{}負{}分)".format(100*result.win_rate, result.victory_count, result.defeat_count, result.drow_count))
            continue_flag = self.confirm_retry()
        result.__init__()
        self.choice_mode()

    #ポーカーをプレイ(勝ち抜き戦)
    def tournament_poker(self):
        self.change = 3
        self.joker = 2
        for i in range(1,5):
            self.level = i
            if i==1:print("まずはレベル1の相手です")
            elif i==2:print("次はレベル2の相手です")
            elif i==3:print("次はレベル3の相手です")
            elif i==4:print("最後はレベル4の相手です")
            time.sleep(1)
            print()
            host_poker.main()
            self.count = 0
            self.first = False
            if result.match_count != result.victory_count:
                print("残念!また挑戦してね")
                print()
                self.__init__()
                result.__init__()
                self.choice_mode()
                break
        if self.mode_flag == 2:
            print("クリアです!おめでとう!!")
            print()
            self.__init__()
            result.__init__()
            self.choice_mode()

    #クレジットを見る
    def credit(self):
        print("#####################################")
        print()
        print("<作成者>")
        print("tonc13")
        print()
        print("<デバッカー>")
        print("4ra")
        print()
        print("<開発環境>")
        print("OS: MacOS 13.1")
        print("IDE: Visual Studio Code 1.71.2")
        print("言語: Python 3.9.13")
        print()
        print("#####################################")
        print()
        self.mode_flag = 0
        self.choice_mode()

    #モードの説明を表示
    def ex_mode(self):
        print("#####################################")
        print()
        print("「1.ポーカーをプレイ(通常)」: ルールや対戦相手のレベルを自分で決めて対戦できます。")
        print("「2.ポーカーをプレイ(勝ち抜き戦)」: レベル1から4の相手と順番に戦い、全員に勝てたらクリアです。\n(手札交換は3回まで,ジョーカーは2枚です。、また引き分けは敗北とします。)")
        print("「3.クレジットを表示」: クレジットを表示します")
        print()
        print("#####################################")
        print()
        self.mode_flag = 0
        self.choice_mode()


    #もう一度やるか確認
    def confirm_retry(self):
        while self.flag not in [1,2]:
            try:
                self.flag = int(input("もう一度プレイしますか?(はい:1, いいえ:2)"))
            except:
                print("正しい入力ではありません")
            else:
                if self.flag == 1:
                    print("分かりました")
                    print()
                    rule_flag = 0
                    while rule_flag not in [1,2]:
                        try:
                            rule_flag = int(input("ルールを変更しますか?(はい:1, いいえ:2)"))
                        except:
                            print("正しい入力ではありません")
                        else:
                            if rule_flag == 1:
                                print("分かりました")
                                print()
                                host.__init__()
                                self.first = False
                                self.mode_flag = 1
                                return True
                            elif rule_flag == 2:
                                print("分かりました")
                                print()
                                self.first = False
                                self.count = 0
                                self.flag = 0
                                return True
                            else:
                                print("正しい入力ではありません")
                elif self.flag == 2:
                    print("分かりました")
                    print()
                    host.__init__()
                    result.__init__()
                    return False
                else:
                    print("正しい入力ではありません")

class HostPoker:
    def __init__(self):
        pass

    #ポーカーゲーム
    def main(self):
        if host.first: #初回はルール説明を表示
            if host.mode_flag == 1:
                print("ポーカーゲームを始めます。")
                print()
            self.ex_rule()
            self.initialization_flag()
            print()

            self.ex_hand()
            self.initialization_flag()
            print()

        if host.level == -1:
            self.decide_level()
            print()

        if host.change == -1:
            self.decide_change()
            print()

        if host.joker == -1:
            self.decide_joker()
            print()

        print("では始めます。")
        print("まずあなたの手札を配ります。")
        print()
        print(p_hand.cards)

        while host.change != host.count:
            self.change_cards()
            self.initialization_flag()
        print()

        print("では、この手札で確定します。")
        p_hand.confirm_hand()
        c_hand.decide_hand(host.level)

        self.compete_cpu()
        self.initialization_flag()
        self.shuffle_card()

    #flagの初期化(0にする)
    def initialization_flag(self):
        host.flag = 0

    #デッキ、プレーヤーの手札、CPUの手札をリセットする
    def shuffle_card(self):
        deck.__init__()
        p_hand.__init__()
        c_hand.__init__()

    #ルール説明
    def ex_rule(self):
        while host.flag not in [1,2]: #正しい入力が行われるまで繰り返す
            try:
                host.flag = int(input("ルール説明を見ますか?(はい:1,いいえ:2)"))
            except:
                print("正しい入力ではありません。")
            else:
                if host.flag == 1:
                    print()
                    print(" <ルール説明>")
                    print("ポーカーは、5枚の手札の組み合わせでカードの強さを競うトランプゲームです。")
                    print("・最初に、トランプカードが5枚配られます。")
                    print("・その後手札を見て、決められた組み合わせを作るためにカードを山札と交換します。")
                    print("・1回に交換するカードの枚数は任意ですが、交換の回数には上限があります。")
                    print("・交換をやめる,または交換の上限に達したら、役を見せ合い勝敗を決定します。")
                    print("・お互いに役が同じの場合は、数字の大きさで勝敗を決める事とします。数字の強さは1が最弱、13が最強とします。")
                    print("・ただし、プレイヤーとCPUは山札を共有していません。")
                elif host.flag == 2:
                    print("分かりました。")
                else:
                    print("正しい入力ではありません。")

    #役の説明
    def ex_hand(self):
        while host.flag not in[1,2]:
            try:
                host.flag = int(input("役一覧を見ますか?(はい:1,いいえ:2)"))
            except:
                print("正しい入力ではありません。")
            else:
                if host.flag == 1:
                    print()
                    print(" <役一覧(弱い順)>")
                    print("「ブタ」：何も役が揃ってない状態。ブタ同士は五枚の中で一番強い数で勝負。/[*,*,*,*,*]")
                    print("「ワンペア」：同じ数が二枚ある状態。数字の強さ勝負になりがち。/[♡1,♢1,*,*,*]")
                    print("「ツーペア」：ワンペアが二組ある状態。そんなに見ない。/[♡1,♢1,♡4,♢4,*]")
                    print("「スリーカード」：同じ数が三枚ある状態。上位の役を狙いやすい。/[♡2,♢2,♤2,*,*]")
                    print("「ストレート」：五枚の数字が続いてる状態。下手に狙うとブタになる。/[♡12,♤13,♧1,♡2,♢3]")
                    print("「フラッシュ」：五枚の模様が揃ってる状態。下手に狙うとブタになる。/[♡1,♡3,♡7,♡8,♡11]")
                    print("「フルハウス」：ワンペア＋スリーカード。意外とみる。/[♡2,♢2,♤2,♡5,♧5]")
                    print("「フォーカード」：同じ数が四枚ある状態。ジョーカーがあると割と出る。/[♡2,♢2,♤2,♧2,*]")
                    print("「ストレートフラッシュ」：ストレート＋フラッシュ。名前かっこいい。/[♡3,♡4,♡5,♡6,♡7]]")
                    print("「ロイヤルストレートフラッシュ」:5枚が10・J・Q・K・Aのフラッシュ。帰り道に気をつけたほうがいい。/[♡10,♡11,♡12,♡13,♡1]")
                    print("「ファイブカード」:同じ数が五枚ある状態。ジョーカーが必須。/[♡2,♢2,♤2,♧2,Joker]")
                elif host.flag == 2:
                    print("分かりました。")
                else:
                    print("正しい入力ではありません。")

    #cpuのレベルのを決定
    def decide_level(self):
        while host.level not in [1,2,3,4]:
            try:
                host.level = int(input("cpuのレベルはどうしますか?(1~4)"))
            except:
                print("正しい入力ではありません。")
            else:
                if host.level in [1,2,3,4]:
                    print("分かりました。")
                else:
                    print("正しい入力ではありません。")

    #手札の交換回数を決定
    def decide_change(self):
        while not (0 <= host.change <= 9 and isinstance(host.change, int)):
            try:
                host.change = int(input("手札の交換の上限をいくつにしますか?(0〜9)"))
            except:
                print("正しい入力ではありません。")
            else:
                if 0 <= host.change <= 9:
                    print("分かりました。")
                else:
                    print("正しい入力ではありません。")

    #山札に入れるジョーカーの数を決定
    def decide_joker(self):
        while host.joker not in [0,1,2]:
            try:
                host.joker = int(input("山札のジョーカーの枚数をいくつにしますか?(0〜2)"))
            except:
                print("正しい入力ではありません。")
            else:
                if host.joker in [0,1,2]:
                    print("分かりました。")
                    deck.add_joker(host.joker)
                else:
                    print("正しい入力ではありません。")

    #上限が来るまで手札を交換
    def change_cards(self):
        while host.flag not in [1,2]:
            try:
                host.flag = int(input("手札を交換しますか?(残り回数は{}回)(はい:1,いいえ:2)".format(host.change-host.count)))
            except:
                print("正しい入力ではありません。")
            else:
                if host.flag == 1:
                    change_loc_list = []
                    while (len(change_loc_list) <= 0):
                        print()
                        print("交換したいカードの順番を入力して下さい。(交換したくない場合は0を入力)")
                        print("(例：[1♧, 4♢, 11♢, 12♡, 12♢]で[1♧, 11♢, 12♡]を交換する場合、1,3,4と入力)")
                        try:
                            change_loc = input("現在の手札：{}".format(p_hand.cards))
                            change_loc_list = change_loc.split(",")
                            change_loc_list = [int(val) for val in change_loc_list]
                        except:
                            print("正しい入力ではありません。")
                        else:
                            #要素が1から五の数字でかつ重複がないか判定
                            if all([1 <= val <= 5 for val in change_loc_list]) and not [x for x in set(change_loc_list) if change_loc_list.count(x) != 1]:
                                p_hand.change_cards(change_loc_list)
                                print()
                                print("交換した結果はこちらです。")
                                print(p_hand.cards)
                                host.count += 1
                                print()
                            elif len(change_loc_list) == 1 and change_loc_list[0] == 0:
                                print("分かりました")
                                host.flag = 2
                                host.count = host.change
                            else:
                                print("正しい入力ではありません。")
                elif host.flag == 2:
                    host.count = host.change
                else:
                    print("正しい入力ではありません。")

    #勝敗判定
    def compete_cpu(self):
        while host.flag != 1:
            try:
                host.flag = int(input("祈りの時間が終わったら、1を押してください。"))
            except:
                print("正しい入力ではありません")
            else:
                if host.flag == 1:
                    print("分かりました")
                    print()
                    time.sleep(1)
                    print("あなたの役は、{}です。".format(p_hand.hand))
                    time.sleep(1.2)
                    print("cpuの役は、{}です。".format(c_hand.hand))
                    time.sleep(1.2)
                    print()

                    if PokerGame_list.hand_list.index(p_hand.only_hand) > PokerGame_list.hand_list.index(c_hand.only_hand):
                        print("You Win! あなたの勝ちです!")
                        result.match_count += 1
                        result.victory_count += 1
                        print()
                    elif PokerGame_list.hand_list.index(p_hand.only_hand) < PokerGame_list.hand_list.index(c_hand.only_hand):
                        print("You Lose! あなたの負けです!")
                        result.match_count += 1
                        result.defeat_count += 1
                        print()
                    elif PokerGame_list.hand_list.index(p_hand.only_hand) == PokerGame_list.hand_list.index(c_hand.only_hand):
                        if p_hand.only_num > c_hand.only_num:
                            print("You Win! 接戦でしたがあなたの勝ちです!")
                            result.match_count += 1
                            result.victory_count += 1
                            print()
                        elif p_hand.only_num < c_hand.only_num:
                            print("You Lose! 惜しいですがあなたの負けです!")
                            result.match_count += 1
                            result.defeat_count += 1
                        elif p_hand.only_num == c_hand.only_num:
                            print("なんと引き分けです!")
                            result.match_count += 1
                            result.drow_count += 1
                    time.sleep(2)
                else:
                    print("正しい入力ではありません")

class Result:
    def __init__(self):
        self.match_count = 0
        self.victory_count = 0
        self.drow_count = 0
        self.defeat_count = 0
        self.win_rate = "-"
    
    def cul_winrate(self):
        if self.match_count != 0:
            self.win_rate = round(self.victory_count / (self.match_count - self.drow_count), 2)


deck = Deck()
p_hand = PlayerHand()
c_hand = CpuHand()
result = Result()

host = Host()
host_poker = HostPoker()

host.PokerGame()