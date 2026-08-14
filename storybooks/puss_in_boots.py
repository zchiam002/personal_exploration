"""Puss in Boots -- after Charles Perrault (1697)."""

import math

from art import *          # noqa: F401,F403
from art import _rng, _ol, _sack, _boot, _cat_hat, LINE, LW, P
from scenery import *      # noqa: F401,F403
import layout
from layout import W, H, BASE, bold_left

SLUG = "puss-in-boots"
ACCENT = "#7A3B2E"

TEXT = {
    "en": {'TITLE': 'Puss in Boots',
     'SUBTITLE': 'an old fairy tale, told again',
     'BYLINE': 'after the story by Charles Perrault',
     'BELONGS_TO': 'This book belongs to',
     'PAGES': ['There was once a miller with three sons. When he grew old he '
               'left the mill to the eldest, and the donkey to the second, '
               'and to the youngest, Jack, he left only the cat.',
               '“Oh dear,” said Jack. “What good is a cat to me?”\n'
               'The cat looked up. “A great deal of good,” he said. “Bring '
               'me a sack, and a fine pair of boots, and you shall see.”',
               'Jack was so astonished that he sat straight down in the '
               'straw. But he found the boots — red ones, with turned-down '
               'tops — and the cat pulled them on and stood up tall.',
               'He put a feather in his hat. He looked at himself for a long '
               'moment. Then he purred.\n'
               'And from that day, everybody called him Puss in Boots.',
               'Off went Puss to the meadow. He propped his sack open, '
               'dropped in two fat carrots, and lay so still that a beetle '
               'walked over his paw.\n'
               'Along came a plump young rabbit — and snap went the sack.',
               'Puss marched all the way to the palace and bowed very low '
               'before the King.\n'
               '“A gift for Your Majesty,” he said, “from my master, the '
               'Marquis of Carabas.”',
               'Now, there was no such person as the Marquis of Carabas. '
               'Puss had made him up on the road.\n'
               'But the gifts kept coming — partridges on Monday, fish on '
               'Friday — and the King grew very curious indeed.',
               'One morning Puss heard that the King would ride along the '
               'river, with the Princess beside him.\n'
               'He ran home faster than the wind. “Master! Quick! Go and '
               'swim in the river!”',
               'Jack thought this was a very silly plan. But in he went.\n'
               'And while he splashed about, Puss hid his old clothes under '
               'a stone and began to shout: “Help! Help! My master is '
               'drowning!”',
               'The royal coach stopped at once. Servants pulled Jack out, '
               'dripping wet.\n'
               '“A thief has run off with his fine clothes,” said Puss '
               'sadly. So the King lent him a coat of blue velvet.',
               'The Princess thought he looked rather nice.\n'
               '“Ride with us,” said the King. And Jack climbed into the '
               'golden coach, hardly believing a moment of it.\n'
               'Puss ran on ahead.',
               'He came to great fields of wheat, where the haymakers were '
               'working in the sun.\n'
               '“When the King asks whose land this is,” said Puss, “you '
               'will say it belongs to the Marquis of Carabas.”\n'
               'And so they did.',
               'On ran Puss, until he came to a castle. Inside lived an '
               'Ogre, who owned every field for miles around.\n'
               'Puss knocked politely. “I hear that you can do magic,” he '
               'said. “Is it true?”',
               '“Watch this!” roared the Ogre — and with a POOF he turned '
               'into a lion.\n'
               'Puss leapt to the top of the cupboard. His heart went thump, '
               'thump, thump.\n'
               'But he smiled all the same.',
               '“Very fine,” said Puss. “But a big beast is easy. I don’t '
               'suppose you could manage something tiny? A mouse, perhaps?”\n'
               '“Easy!” squeaked the Ogre. And poof — a mouse.',
               'Puss chased him out of the door, down the steps and away '
               'over the hill, and the Ogre was never seen again.\n'
               'Then Puss dusted off his boots and went to wait at the gate.',
               'When the coach came rumbling up, Puss bowed low.\n'
               '“Welcome, Your Majesty, to the castle of the Marquis of '
               'Carabas!”\n'
               'The King was amazed. The Princess laughed. Jack could not '
               'say a word.',
               'So Jack married the Princess, and Puss was made a lord, with '
               'a red cushion of his own beside the fire.\n'
               'He never had to chase a mouse again — though now and then, '
               'just for the fun of it, he did.'],
     'THE_END': 'The End',
     'COLOPHON': 'A retelling of Charles Perrault’s “Le Maître Chat, ou le '
                 'Chat Botté”, first printed in 1697.\n'
                 'Illustrations drawn as vector art. Made to be read aloud.',
     'BACK_QUOTE': ['“Bring me a sack, and a fine pair of boots,',
                    'and you shall see.”']},
    "zh": {'TITLE': '穿靴子的猫',
     'SUBTITLE': '一个古老的童话',
     'BYLINE': '改编自夏尔·佩罗的故事',
     'BELONGS_TO': '这本书属于',
     'PAGES': ['从前有一个磨坊主，他有三个儿子。他年纪大了，就把磨坊留给老大，把驴子留给老二。留给最小的儿子杰克的，只有一只猫。',
               '“唉，”杰克说，“一只猫有什么用呢？”\n猫抬起头来说：“用处大着呢。给我一个口袋，再给我一双漂亮的靴子，你就知道了。”',
               '杰克惊讶得一屁股坐在了稻草上。不过他还是找来了靴子——红色的，靴口是翻下来的。猫穿上靴子，站得直直的。',
               '他在帽子上插了一根羽毛，对着自己看了好久，然后满意地打起呼噜来。\n从那天起，大家都叫他“穿靴子的猫”。',
               '猫来到草地上。他把口袋撑开，放进两根胖萝卜，然后一动不动地趴着，连甲虫爬过他的爪子都没有动。\n'
               '一只肥肥的小兔子跳了过来——啪的一声，口袋合上了。',
               '猫一路走到王宫，对国王深深地鞠了一躬。\n“陛下，”他说，“这是我的主人卡拉巴斯侯爵送给您的礼物。”',
               '其实，世界上根本没有什么卡拉巴斯侯爵，这是猫在路上编出来的。\n'
               '可是礼物一件接一件地送来：星期一送鹧鸪，星期五送鱼。国王越来越好奇了。',
               '一天早上，猫听说国王要沿着河边出游，公主也一起去。\n他跑回家，跑得比风还快。“主人！快！快到河里去游泳！”',
               '杰克觉得这个主意真傻，可他还是下了水。\n'
               '他在水里扑腾的时候，猫把他的旧衣服藏到了一块石头下面，然后大声喊起来：“救命啊！我的主人快淹死啦！”',
               '王家的马车立刻停了下来。仆人们把浑身湿透的杰克拉了上来。\n'
               '“有个小偷把他漂亮的衣服偷走了。”猫难过地说。于是国王借给他一件蓝色天鹅绒外衣。',
               '公主觉得他看上去挺好看的。\n“跟我们一起坐车吧。”国王说。杰克坐进金马车，简直不敢相信这是真的。\n猫抢先跑到了前面。',
               '他跑到一大片麦田，割麦子的人正在太阳底下干活。\n'
               '“要是国王问这是谁的地，”猫说，“你们就说，是卡拉巴斯侯爵的。”\n'
               '他们真的照做了。',
               '猫一直往前跑，跑到了一座城堡。城堡里住着一个食人魔，方圆几里的田地都是他的。\n'
               '猫很有礼貌地敲了敲门。“听说您会变魔法，”他说，“是真的吗？”',
               '“你看好了！”食人魔大吼一声——砰的一下，变成了一头狮子。\n猫一下子跳到柜子顶上，心里怦怦怦直跳。\n可他还是笑着。',
               '“真厉害，”猫说，“不过变大家伙容易。您能不能变个小的？比如说，一只老鼠？”\n'
               '“这有什么难的！”食人魔尖声说。砰——变成了一只老鼠。',
               '猫把老鼠一路追出门，追下台阶，追过山坡，从此再也没有人见过那个食人魔。\n然后猫掸了掸靴子上的灰，走到大门口去等着。',
               '马车咕噜咕噜开过来的时候，猫深深地鞠了一躬。\n'
               '“陛下，欢迎光临卡拉巴斯侯爵的城堡！”\n'
               '国王惊呆了，公主笑了，杰克一句话也说不出来。',
               '后来，杰克娶了公主，猫也当上了大臣，还在壁炉边有了一个自己的红垫子。\n'
               '他再也不用去抓老鼠了——不过偶尔，为了好玩，他还是会去抓一抓。'],
     'THE_END': '完',
     'COLOPHON': '改编自夏尔·佩罗一六九七年的童话《穿靴子的猫》。\n插图为矢量绘制。适合大声朗读。',
     'BACK_QUOTE': ['“给我一个口袋，再给我一双漂亮的靴子，', '你就知道了。”']},
}


def COVER_ART(c):
    sky(c, 0, 250, W, H - 250, "#F7C98B", "#FDE9C4")
    sun(c, 690, 500, 50)
    for cx, cy, s in ((140, 520, 1.2), (430, 556, 0.75), (720, 396, 0.9)):
        cloud(c, cx, cy, s, fill="#FFF6E4")
    for bx, by in ((238, 500), (292, 522), (342, 490)):
        bird(c, bx, by, 1.4, color="#B08A5E")
    hills(c, -20, 236, W + 40, 86, "#B9D69A", bumps=4, seedoff=0.3)
    hills(c, -20, 210, W + 40, 70, "grass_dk", bumps=3, seedoff=2.4)
    castle(c, 726, 262, 0.5, wall="#D8CFC0", roof="#8E5A6B", flag="#C05A6B")
    ground(c, 0, 0, W, 266, "grass", "grass_lt")
    grass_tufts(c, 0, W, 240, n=28, seed=7)
    tree(c, 82, 214, 1.35)
    bush(c, 786, 186, 1.4)
    for fx in (58, 128, 700, 792):
        flower(c, fx, 202, 1.3, petal="#FFFFFF")
    for fx in (172, 646):
        flower(c, fx, 148, 1.4, petal="#F6C453")

    draw_puss(c, 404, 108, 2.05, expr="proud", arm_r="hip", arm_l="doff",
              sword=True, tail="curl", legs="stride")
    sparkles_around(c, 404, 300, 216, 7, seed=11)


def NAMEPLATE_ART(c):
    """The hat and one boot, waiting by the door."""
    c.saveState()
    c.translate(W / 2, 236)
    shadow(c, 0, 4, 168, 24, alpha=0.10)
    c.saveState()
    c.translate(-104, 48)
    c.scale(2.7, 2.7)
    c.rotate(6)
    _cat_hat(c)
    c.restoreState()
    c.saveState()
    c.translate(92, 20)
    c.scale(3.1, 3.1)
    c.rotate(-6)
    _boot(c, 0, 0, 0)
    c.restoreState()
    c.restoreState()


def s01_three_sons(c):
    meadow(c, 330)
    windmill(c, 108, 316, 1.25)
    cottage(c, 742, 300, 1.1)
    tree(c, 596, 308, 1.0)
    grass_tufts(c, 0, W, 286, n=22, seed=3)
    horse(c, 452, BASE, 0.86, body="#B9B1A6", mane="#6B6058")
    draw_person(c, 214, BASE, 1.5, robe="#8C7A62", hair="hair_brown",
                arm_r="point", expr="happy")
    draw_person(c, 372, BASE, 1.46, robe="#7F8C6A", hair="#5E4630",
                arm_r="hold", expr="happy", flip=True)
    draw_person(c, 636, BASE, 1.52, robe="jack_old", hair="hair_brown",
                expr="sad", arm_r="down", arm_l="down")
    draw_puss(c, 736, BASE, 1.0, hat=False, cape=False, boots=False,
              legs="sit", tail="down", expr="happy", arm_r="down",
              arm_l="down", flip=True)


def s02_a_talking_cat(c):
    meadow(c, 318, clouds=((190, 520, 0.95),), sunpos=None)
    cottage(c, 132, 302, 1.3)
    tree(c, 782, 306, 1.25)
    bush(c, 660, 288, 1.3)
    grass_tufts(c, 0, W, 288, n=20, seed=9)
    for fx in (300, 352, 540):
        flower(c, fx, 268, 1.2, petal="#FFFFFF")
    rect(c, 350, 176, 116, 36, fill="wood_dk", r=9, stroke=LINE, lw=1.8)
    draw_person(c, 408, 212, 1.52, robe="jack_old", expr="surprised",
                arm_l="out", arm_r="out", legs="stride")
    draw_puss(c, 616, BASE, 1.28, hat=False, cape=False, boots=False,
              expr="sly", arm_r="point", arm_l="hip", tail="swish", flip=True)
    for bx, by, br in ((528, 370, 11), (558, 402, 7.5), (582, 428, 5)):
        circle(c, bx, by, br, fill="#FFFFFF", alpha=0.85, stroke="#E0D3BC",
               lw=1.2)


def s03_the_boots(c):
    meadow(c, 314, clouds=((700, 520, 0.95),))
    cottage(c, 742, 298, 1.15)
    grass_tufts(c, 0, W, 284, n=18, seed=12)
    for i in range(26):
        rnd = _rng(i + 2)
        sx = 110 + rnd() * 540
        stroke_path(c, [(sx, 196), (sx + 16, 204), (sx + 32, 196)],
                    color="wheat_dk", lw=2.2)
    draw_puss(c, 330, BASE, 1.95, expr="proud", arm_r="hip", arm_l="out",
              tail="up", legs="stand", hat=False)
    sparkles_around(c, 330, 340, 200, 8, seed=5)
    draw_person(c, 612, BASE, 1.5, robe="jack_old", expr="surprised",
                arm_l="up", arm_r="up", flip=True)


def s04_feather_in_his_hat(c):
    meadow(c, 322, sky_top="#C9E6F4", clouds=((170, 528, 1.05), (630, 488, 0.75)))
    tree(c, 82, 306, 1.3)
    tree(c, 778, 310, 1.1)
    grass_tufts(c, 0, W, 292, n=24, seed=15)
    for fx in (232, 292, 620, 686):
        flower(c, fx, 272, 1.2, petal="#F6C453")
    ellipse(c, 508, 202, 138, 30, fill="water", alpha=0.6)
    ellipse(c, 508, 202, 118, 22, fill="#A8D8EC", alpha=0.7)
    draw_puss(c, 386, 224, 2.0, expr="proud", arm_r="chin", arm_l="hip",
              tail="perk", legs="stand")
    sparkles_around(c, 386, 380, 208, 8, seed=21)
    for bx, by in ((650, 494), (700, 518)):
        bird(c, bx, by, 1.3)


def s05_the_rabbit(c):
    meadow(c, 336, g1="#93C973", g2="#ADD98C",
           clouds=((200, 524, 1.05), (672, 540, 0.85)))
    for i in range(44):
        rnd = _rng(i + 30)
        gx = rnd() * W
        gh = 30 + 34 * rnd()
        stroke_path(c, [(gx, 196), (gx + 10, 196 + gh * 0.6),
                        (gx + 20, 196 + gh)], color="grass_dk", lw=2.6)
    bush(c, 214, 244, 2.0)
    bush(c, 754, 250, 1.7)
    draw_puss(c, 340, BASE, 1.5, expr="sly", legs="sit", tail="swish",
              arm_r="hold", arm_l="down")
    _sack(c, 486, 252, 1.9)
    draw_rabbit(c, 664, 200, 2.5, flip=True)
    for i in range(3):
        stroke_path(c, [(566 - i * 26, 264 + i * 10),
                        (578 - i * 26, 278 + i * 10)],
                    color="#FFFFFF", lw=3.2, alpha=0.6)
    grass_tufts(c, 0, W, 190, n=22, seed=6)


def s06_before_the_king(c):
    stone_hall(c, 330)
    for bx in (130, 726):
        banner(c, bx, H - 42, 74, 186, "cape", "gold")
    rect(c, 372, 372, 108, 152, fill="#7FB6D4", r=54, stroke="stone_dk", lw=3.4)
    stroke_path(c, [(426, 372), (426, 524)], color="stone_dk", lw=2.8)
    stroke_path(c, [(372, 448), (480, 448)], color="stone_dk", lw=2.8)
    throne(c, 648, BASE, 1.35)
    draw_person(c, 648, BASE + 30, 1.5, robe="king_robe", crown=True,
                hair="hair_grey", beard=True, expr="happy", arm_r="hold",
                arm_l="down", flip=True)
    poly(c, [(104, 40), (238, BASE - 4), (566, BASE - 4), (516, 40)],
         fill="cape_dk")
    poly(c, [(126, 40), (252, BASE - 8), (552, BASE - 8), (498, 40)],
         fill="cape")
    draw_puss(c, 318, BASE, 1.42, expr="sly", arm_r="doff", arm_l="hold",
              lean=13, legs="bow", tail="curl")
    _sack(c, 392, 274, 1.25)


def s07_gifts_every_week(c):
    stone_hall(c, 326)
    banner(c, 104, H - 42, 70, 178, "#3F6FA8", "gold")
    banner(c, 762, H - 42, 70, 178, "#3F6FA8", "gold")
    throne(c, 200, BASE, 1.26)
    draw_person(c, 200, BASE + 28, 1.44, robe="king_robe", crown=True,
                hair="hair_grey", beard=True, expr="happy", arm_r="clasp",
                arm_l="down")
    gift_pile(c, 520, BASE + 10)
    draw_puss(c, 736, BASE, 1.34, expr="sly", arm_r="out", arm_l="hip",
              tail="curl", flip=True)
    bold_left(c, 262, 452, "?", 46, "#6B5A52")
    bold_left(c, 308, 490, "?", 32, "#6B5A52")


def s08_run_home(c):
    meadow(c, 312, clouds=((230, 532, 1.05), (620, 500, 0.8)))
    cottage(c, 752, 296, 1.2)
    tree(c, 76, 302, 1.2)
    wheat_field(c, 0, 196, W, 96, seed=8, n=40)
    grass_tufts(c, 0, W, 268, n=18, seed=4)
    draw_puss(c, 320, BASE, 1.72, expr="surprised", arm_r="point", arm_l="up",
              legs="run", tail="swish", lean=-8)
    motion(c, 218, 268, 3, 88, 18, color="#FFFFFF", alpha=0.7)
    draw_person(c, 674, BASE, 1.46, robe="jack_old", expr="surprised",
                arm_l="up", arm_r="down", flip=True)


def s09_into_the_river(c):
    sky(c, 0, 318, W, H - 318, "#BFE1F0", "#DDF0F8")
    sun(c, 118, 528, 42)
    cloud(c, 330, 540, 0.95)
    cloud(c, 706, 506, 0.8)
    hills(c, -20, 282, W + 40, 66, "#A9CE8E", bumps=4, seedoff=1.2)
    ground(c, 0, 0, W, 322, "grass", "grass_lt")
    river(c, 0, 176, W, 148)
    grass_tufts(c, 0, W, 300, n=20, seed=11)
    # Jack, up to his shoulders, well clear of the text panel
    circle(c, 470, 290, 21, fill="skin", stroke=LINE, lw=2.0)
    _ol(c, [(470, 314), (491, 302), (494, 288), (480, 296), (470, 299),
            (460, 296), (446, 288), (449, 302)], "hair_brown", tension=0.75)
    for dx in (-7.5, 7.5):
        circle(c, 470 + dx, 293, 2.8, fill="ink")
    ellipse(c, 470, 281, 4.0, 5.0, fill="#8E3B3F")
    for sx, ax in ((-1, 424), (1, 516)):
        taper(c, [(470 + sx * 16, 276), (ax, 292), (ax + sx * 16, 326)],
              8.0, 6.0, fill="skin", stroke=LINE, lw=1.7)
        circle(c, ax + sx * 16, 326, 7.0, fill="skin", stroke=LINE, lw=1.5)
    for i, (sx, sr) in enumerate(((-1, 62), (1, 70))):
        ellipse(c, 470 + sx * sr, 270, 34 - i * 4, 10, fill="#FFFFFF", alpha=0.65)
    # the stone, with the old clothes tucked underneath
    _ol(c, [(146, 246), (192, 272), (244, 262), (254, 234), (202, 222),
            (150, 226)], "stone_dk", tension=0.8)
    _ol(c, [(228, 240), (282, 248), (302, 232), (264, 222), (228, 228)],
        "jack_old", tension=0.8)
    draw_puss(c, 712, 244, 1.66, expr="surprised", arm_r="up", arm_l="up",
              tail="up", legs="stride", flip=True)
    for i in range(3):
        stroke_path(c, [(636 - i * 20, 424 + i * 14),
                        (606 - i * 20, 436 + i * 14)],
                    color="#FFFFFF", lw=3.6, alpha=0.6)
    coach(c, 128, 338, 0.5)


def s10_pulled_out(c):
    sky(c, 0, 320, W, H - 320, "#BFE1F0", "#E4F2F9")
    cloud(c, 190, 534, 0.9)
    cloud(c, 636, 552, 1.0)
    sun(c, 774, 496, 40)
    hills(c, -20, 286, W + 40, 60, "#A9CE8E", bumps=4, seedoff=0.9)
    ground(c, 0, 0, W, 324, "grass", "grass_lt")
    river(c, 0, 188, W * 0.28, 122, sparkles=False)
    grass_tufts(c, W * 0.30, W, 288, n=16, seed=13)
    coach(c, 736, 268, 0.8)
    draw_person(c, 150, BASE, 1.5, robe="jack_new", hair="hair_brown",
                expr="surprised", arm_l="out", arm_r="up", wet=True)
    draw_person(c, 386, BASE, 1.56, robe="king_robe", crown=True,
                hair="hair_grey", beard=True, expr="happy", arm_r="point")
    draw_person(c, 566, BASE, 1.44, robe="princess", hair="hair_gold",
                long_hair=True, hat="tiara", expr="happy", arm_r="clasp")
    draw_puss(c, 268, BASE, 1.2, expr="sly", arm_r="point", arm_l="hip",
              tail="curl")


def s11_the_golden_coach(c):
    meadow(c, 322, sky_top="#C6E6F4", clouds=((190, 534, 1.05), (712, 512, 0.85)))
    hills(c, -20, 280, W + 40, 56, "grass_dk", bumps=3, seedoff=3.0)
    road(c, 300)
    tree(c, 62, 296, 1.2)
    tree(c, 792, 300, 1.05)
    grass_tufts(c, 0, W, 262, n=14, seed=17)
    coach(c, 168, 178, 1.15, passengers=True)
    horse(c, 408, 190, 1.12)
    draw_puss(c, 690, 196, 1.5, expr="proud", arm_r="point", arm_l="out",
              legs="run", tail="swish", lean=-6)
    motion(c, 606, 252, 3, 74, 17, color="#FFFFFF", alpha=0.6)


def s12_the_haymakers(c):
    meadow(c, 330, sky_top="#F3DFAE", sky_bot="#FBEFD2", sunpos=(140, 526),
           clouds=((520, 536, 0.95),))
    hills(c, -20, 292, W + 40, 52, "#C7B771", bumps=4, seedoff=1.5)
    wheat_field(c, 0, 0, W, 292, seed=2, n=72)
    _ol(c, [(178, 214), (238, 242), (288, 224), (280, 190), (220, 180),
            (176, 190)], "stone_dk", tension=0.8)
    draw_puss(c, 232, 228, 1.48, expr="proud", arm_r="point", arm_l="hip",
              tail="up", legs="stand")
    for i, (px, ps, fl) in enumerate(((520, 1.36, False), (650, 1.44, True),
                                      (772, 1.30, False))):
        draw_person(c, px, 202, ps,
                    robe=("#C9A874", "#A8B98A", "#C08C6A")[i],
                    hat="straw", hair="#6B4A2E", expr="happy",
                    arm_r="reach" if not fl else "hold", flip=fl)
    for sx in (566, 706):
        stroke_path(c, [(sx, 214), (sx + 38, 264), (sx + 72, 276)],
                    color="wood_dk", lw=4.6)
        stroke_path(c, [(sx + 72, 276), (sx + 104, 254)], color="#B9BEC4",
                    lw=5.0)


def s13_the_ogres_castle(c):
    sky(c, 0, 300, W, H - 300, "#9FB6D4", "#CBDCEB")
    for cx, cy, s in ((176, 536, 1.15), (676, 500, 0.95)):
        cloud(c, cx, cy, s, fill="#E8EEF5")
    for bx, by in ((292, 544), (344, 564)):
        bird(c, bx, by, 1.4, color="#5E5A6B")
    hills(c, -20, 266, W + 40, 66, "#7E9A78", bumps=3, seedoff=2.0)
    ground(c, 0, 0, W, 302, "#89A874", "#9CBB84")
    castle(c, 612, 290, 1.05, wall="#B7AFA2", roof="#5B4A66",
           flag="#6B4A7A", windows="#3E4C63")
    grass_tufts(c, 0, W, 276, n=18, seed=19, color="#6B8A5E")
    tree(c, 80, 274, 1.25, leaf="#5E7A52", leaf2="#6E8B5F")
    draw_ogre(c, 456, BASE, 2.35, expr="grin", arm_l="down", arm_r="hip",
              flip=True)
    draw_puss(c, 194, BASE, 1.28, expr="sly", arm_r="doff", arm_l="hip",
              lean=8, legs="bow", tail="curl")


def s14_the_lion(c):
    interior(c, wall="#D8C6A8", floor="#9C7449", horizon=314)
    rect(c, 84, 368, 122, 156, fill="#5E7A98", r=60, stroke="wood_dk", lw=4.4)
    stroke_path(c, [(145, 368), (145, 524)], color="wood_dk", lw=3.2)
    cupboard(c, 722, 196, 1.02)
    draw_lion(c, 372, 196, 1.95)
    draw_puss(c, 722, 410, 1.0, expr="surprised", arm_r="hug", arm_l="hug",
              tail="up", legs="sit", flip=True)
    for i in range(4):
        stroke_path(c, [(536 + i * 24, 400 + i * 18),
                        (580 + i * 24, 390 + i * 18)],
                    color="#C0392B", lw=3.6, alpha=0.5)


def s15_the_mouse(c):
    """POOF -- and the great Ogre is a very small mouse."""
    interior(c, wall="#DDCBAD", floor="#A87E50", horizon=314)
    cupboard(c, 104, 214, 1.02)
    for dx, dy, rr, al in ((0, 74, 76, 0.85), (-64, 118, 54, 0.7),
                           (66, 128, 50, 0.7), (-20, 182, 40, 0.5),
                           (42, 192, 32, 0.45)):
        circle(c, 548 + dx, 232 + dy, rr, fill="#EFE6D8", alpha=al)
    for i in range(6):
        a = i * math.pi / 3
        sparkle(c, 548 + 118 * math.cos(a), 316 + 94 * math.sin(a), 11,
                color="#F6E3B0", alpha=0.85)
    draw_mouse(c, 548, BASE, 2.2)
    draw_puss(c, 268, BASE, 1.62, expr="sly", arm_r="hip", arm_l="chin",
              legs="stand", tail="perk")
    bold_left(c, 640, 452, "砰！" if layout.CJK else "poof!", 34,
              "#9C8B76")


def s16_out_the_door(c):
    """Down the steps and away over the hill."""
    interior(c, wall="#DDCBAD", floor="#A87E50", horizon=314)
    cupboard(c, 92, 210, 0.98)
    rect(c, 612, 314, 196, 262, fill="#8A6743", stroke=LINE, lw=2.6)
    rect(c, 632, 314, 156, 236, fill="#BFE1F0", stroke=LINE, lw=1.8)
    hills(c, 632, 314, 156, 54, "#A9CE8E", bumps=2, seedoff=1.0)
    poly(c, [(632, 314), (788, 314), (838, 118), (588, 118)], fill="#FBEFCF",
         alpha=0.55)
    draw_puss(c, 372, BASE, 1.68, expr="scheme", arm_r="out", arm_l="up",
              legs="run", tail="swish", lean=-12)
    draw_mouse(c, 604, BASE + 6, 1.9, flip=True)
    for i in range(3):
        stroke_path(c, [(536 + i * 22, 218 + i * 12),
                        (502 + i * 22, 210 + i * 12)],
                    color="#9C8B76", lw=2.8, alpha=0.55)
    motion(c, 282, 300, 3, 72, 18, color="#FFFFFF", alpha=0.5)


def s17_welcome(c):
    meadow(c, 326, sky_top="#F5D6A0", sky_bot="#FDEFD6", sunpos=(112, 524),
           clouds=((420, 546, 0.85), (712, 508, 0.95)))
    hills(c, -20, 288, W + 40, 56, "grass_dk", bumps=3, seedoff=1.1)
    castle(c, 566, 306, 1.02, wall="#DED5C6", roof="#B0566B", flag="#C86B7E")
    road(c, 306)
    grass_tufts(c, 0, W, 268, n=14, seed=23)
    coach(c, 96, 176, 1.05, passengers=True)
    horse(c, 286, 188, 1.02)
    draw_puss(c, 452, 194, 1.56, expr="proud", arm_r="doff", arm_l="out",
              lean=10, legs="bow", tail="curl")
    for bx, by in ((648, 498), (700, 526), (604, 476)):
        bird(c, bx, by, 1.3, color="#A88A6E")
    sparkles_around(c, 452, 300, 158, 6, seed=31)


def s18_happily_ever_after(c):
    interior(c, wall="#E4D2B4", floor="#A87E50", horizon=316, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    fireplace(c, 138, 316, 1.10)
    for bx in (626, 792):
        banner(c, bx, H - 58, 66, 152, "cape", "gold")
    for i in range(11):
        x0 = 300 + i * 42
        poly(c, [(x0, 500 - abs(i - 5) * 3), (x0 + 34, 500 - abs(i - 5.6) * 3),
                 (x0 + 17, 470 - abs(i - 5) * 3)],
             fill=("#C0392B", "#F6C453", "#5E9BC4")[i % 3], stroke=LINE, lw=1.2)
    stroke_path(c, [(296, 504), (508, 482), (720, 504)], color="wood_dk", lw=2.2)
    cushion(c, 352, 178, 1.3)
    draw_puss(c, 352, 202, 1.14, expr="closed", arm_r="hug", arm_l="hug",
              legs="sit", tail="curl")
    draw_person(c, 542, BASE, 1.56, robe="jack_new", hair="hair_brown",
                expr="happy", arm_r="reach", arm_l="down")
    draw_person(c, 690, BASE, 1.54, robe="princess", hair="hair_gold",
                long_hair=True, hat="tiara", expr="happy", arm_l="reach",
                arm_r="down", flip=True)
    for hx, hy, hs in ((616, 462, 1.5), (572, 496, 1.0), (662, 494, 0.9)):
        c.saveState()
        c.translate(hx, hy)
        c.scale(hs, hs)
        blob(c, [(0, -10), (12, 4), (7, 14), (0, 8), (-7, 14), (-12, 4)],
             fill="#E4708A", stroke=LINE, lw=1.2, tension=0.8)
        c.restoreState()


def END_ART(c):
    interior(c, wall="#E0CDAE", floor="#A87E50", horizon=310, beams=False)
    rect(c, 0, H - 46, W, 46, fill="wood_dk")
    fireplace(c, 676, 310, 1.12)
    c.saveState()
    c.translate(320, 118)
    shadow(c, 0, -6, 168, 24, alpha=0.14)
    _ol(c, [(-124, 0), (-132, 152), (-102, 214), (102, 214), (132, 152),
            (124, 0)], "cape_dk")
    _ol(c, [(-102, 30), (-106, 162), (0, 182), (106, 162), (102, 30)], "cape")
    _ol(c, [(-124, 20), (-136, 98), (-102, 110), (-89, 30)], "cape_dk")
    _ol(c, [(124, 20), (136, 98), (102, 110), (89, 30)], "cape_dk")
    rect(c, -115, 0, 36, 26, fill="wood_dk", r=6, stroke=LINE, lw=1.5)
    rect(c, 79, 0, 36, 26, fill="wood_dk", r=6, stroke=LINE, lw=1.5)
    c.restoreState()
    draw_puss(c, 320, 196, 1.38, expr="sleep", arm_r="hug", arm_l="hug",
              legs="sit", tail="curl", hat=False, shad=False)
    c.saveState()
    c.translate(320, 322)
    c.scale(1.38, 1.38)
    c.rotate(-13)
    _cat_hat(c)
    c.restoreState()
    for zx, zy, zs in ((470, 402, 24), (506, 444, 31), (548, 494, 39)):
        bold_left(c, zx, zy, "z", zs, "#8A7A66")


def BACK_ART(c):
    sky(c, 0, 0, W, H, "#F7C98B", "#FDE9C4")
    for cx, cy, s in ((180, 486, 1.05), (664, 516, 0.85)):
        cloud(c, cx, cy, s, fill="#FFF6E4")
    hills(c, -20, 168, W + 40, 78, "#B9D69A", bumps=4, seedoff=0.3)
    hills(c, -20, 142, W + 40, 62, "grass_dk", bumps=3, seedoff=2.4)
    ground(c, 0, 0, W, 190, "grass", "grass_lt")
    grass_tufts(c, 0, W, 166, n=24, seed=27)
    tree(c, 104, 152, 1.25)
    tree(c, 748, 158, 1.05)
    draw_puss(c, 420, 156, 1.86, expr="wink", arm_r="doff", arm_l="hip",
              tail="curl", legs="stand")


SCENES = [
    s01_three_sons, s02_a_talking_cat, s03_the_boots, s04_feather_in_his_hat,
    s05_the_rabbit, s06_before_the_king, s07_gifts_every_week, s08_run_home,
    s09_into_the_river, s10_pulled_out, s11_the_golden_coach, s12_the_haymakers,
    s13_the_ogres_castle, s14_the_lion, s15_the_mouse, s16_out_the_door,
    s17_welcome, s18_happily_ever_after,
]
