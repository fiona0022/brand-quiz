"""从两个docx提取所有品牌数据，生成quiz_data.js供前端使用"""
import re, sys, unicodedata, json
sys.stdout.reconfigure(encoding='utf-8')

def get_docx_text(path):
    with open(path, encoding='utf-8') as f:
        xml = f.read()
    text = re.sub(r'<[^>]+>', ' ', xml)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

key_text = get_docx_text(r'C:\Users\J nash\Desktop\workbuddy\品牌\unpack_key\word\document.xml')
other_text = get_docx_text(r'C:\Users\J nash\Desktop\workbuddy\品牌\unpack_other\word\document.xml')
full_text = key_text + ' ' + other_text

# ─── 品牌数据 ────────────────────────────────────────────────────
# (英文名, 中文名, 集团, 类型代码)
brands = [
    # ========== LVMH 路威酩轩 ==========
    # 时装与皮具 f
    ("Louis Vuitton", "路易威登", "LVMH 路威酩轩", "f"),
    ("Christian Dior", "迪奥", "LVMH 路威酩轩", "f"),
    ("Loro Piana", "诺悠翩雅", "LVMH 路威酩轩", "f"),
    ("Fendi", "芬迪", "LVMH 路威酩轩", "f"),
    ("Givenchy", "纪梵希", "LVMH 路威酩轩", "f"),
    ("Celine", "思琳", "LVMH 路威酩轩", "f"),
    ("Loewe", "罗意威", "LVMH 路威酩轩", "f"),
    ("Berluti", "伯尔鲁帝", "LVMH 路威酩轩", "f"),
    ("Barton Perreira", "", "LVMH 路威酩轩", "f"),
    ("Rimowa", "日默瓦", "LVMH 路威酩轩", "f"),
    ("Emilio Pucci", "璞琪", "LVMH 路威酩轩", "f"),
    ("Kenzo", "高田贤三", "LVMH 路威酩轩", "f"),
    ("Marc Jacobs", "马克雅可布", "LVMH 路威酩轩", "f"),
    ("Moynat", "摩奈", "LVMH 路威酩轩", "f"),
    ("Patou", "巴度", "LVMH 路威酩轩", "f"),
    ("Vuarnet", "", "LVMH 路威酩轩", "f"),
    # 化妆品与香水 c
    ("Acqua di Parma", "帕尔马之水", "LVMH 路威酩轩", "c"),
    ("Benefit Cosmetics", "贝玲妃", "LVMH 路威酩轩", "c"),
    ("Bvlgari Parfums", "宝格丽香水", "LVMH 路威酩轩", "c"),
    ("Celine Parfums", "思琳香水", "LVMH 路威酩轩", "c"),
    ("Christian Dior Parfums", "迪奥香水", "LVMH 路威酩轩", "c"),
    ("Cha Ling", "茶灵", "LVMH 路威酩轩", "c"),
    ("Fenty Beauty by Rihanna", "蕾哈娜彩妆", "LVMH 路威酩轩", "c"),
    ("Fresh", "馥蕾诗", "LVMH 路威酩轩", "c"),
    ("Givenchy Parfums", "纪梵希香水", "LVMH 路威酩轩", "c"),
    ("Guerlain", "法国娇兰", "LVMH 路威酩轩", "c"),
    ("KVD Beauty", "", "LVMH 路威酩轩", "c"),
    ("Kenzo Parfums", "高田贤三香水", "LVMH 路威酩轩", "c"),
    ("Loewe Perfumes", "罗意威香水", "LVMH 路威酩轩", "c"),
    ("Maison Francis Kurkdjian", "梵诗柯香", "LVMH 路威酩轩", "c"),
    ("Make up for ever", "玫珂菲", "LVMH 路威酩轩", "c"),
    ("Ole Henriksen", "奥丽哈力逊", "LVMH 路威酩轩", "c"),
    ("Officine Universelle Buly", "普利1803", "LVMH 路威酩轩", "c"),
    # 腕表 w
    ("Daniel Roth", "丹尼尔罗斯", "LVMH 路威酩轩", "w"),
    ("Gerald Genta", "尊达", "LVMH 路威酩轩", "w"),
    ("Hublot", "宇舶", "LVMH 路威酩轩", "w"),
    ("TAG Heuer", "泰格豪雅", "LVMH 路威酩轩", "w"),
    ("Zenith", "真力时", "LVMH 路威酩轩", "w"),
    # 珠宝 w
    ("Bvlgari", "宝格丽", "LVMH 路威酩轩", "w"),
    ("Chaumet", "尚美巴黎", "LVMH 路威酩轩", "w"),
    ("Fred", "斐登", "LVMH 路威酩轩", "w"),
    ("Repossi", "雷波西", "LVMH 路威酩轩", "w"),
    ("Tiffany & Co.", "蒂芙尼", "LVMH 路威酩轩", "w"),
    # 精品零售 o
    ("DFS", "免税店", "LVMH 路威酩轩", "o"),
    ("Le Bon Marche", "乐蓬马歇百货", "LVMH 路威酩轩", "o"),
    ("La Samaritaine", "莎玛丽丹百货", "LVMH 路威酩轩", "o"),
    ("24S.com", "电商平台", "LVMH 路威酩轩", "o"),
    # 其他 o
    ("Belmond", "贝梦德酒店", "LVMH 路威酩轩", "o"),
    ("Cova", "Cova甜品", "LVMH 路威酩轩", "o"),
    ("Cheval Blanc", "白马庄园", "LVMH 路威酩轩", "o"),
    ("Sephora", "丝芙兰", "LVMH 路威酩轩", "c"),
    # 酒类 l
    ("Ardbeg", "雅伯", "LVMH 路威酩轩", "l"),
    ("Glenmorangie", "格兰杰", "LVMH 路威酩轩", "l"),
    ("Hennessy", "轩尼诗", "LVMH 路威酩轩", "l"),
    ("Woodinville", "伍丁维尔", "LVMH 路威酩轩", "l"),
    ("Ao Yun", "敖云", "LVMH 路威酩轩", "l"),
    ("Bodega Numanthia", "弩曼希亚酒庄", "LVMH 路威酩轩", "l"),
    ("Colgin Cellars", "蔻金酒庄", "LVMH 路威酩轩", "l"),
    ("Cheval des Andes", "安第斯白马酒庄", "LVMH 路威酩轩", "l"),
    ("Cloudy Bay", "云雾之湾", "LVMH 路威酩轩", "l"),
    ("Domaine des Lambrays", "朗贝雷酒庄", "LVMH 路威酩轩", "l"),
    ("Joseph Phelps", "约瑟夫菲尔普斯", "LVMH 路威酩轩", "l"),
    ("Newton Vineyard", "纽顿酒庄", "LVMH 路威酩轩", "l"),
    ("Dom Perignon", "唐培里侬", "LVMH 路威酩轩", "l"),
    ("Domaine Chandon", "夏桐", "LVMH 路威酩轩", "l"),
    ("Krug", "库克香槟", "LVMH 路威酩轩", "l"),
    ("Moet & Chandon", "酩悦", "LVMH 路威酩轩", "l"),
    ("Mercier", "梅西埃", "LVMH 路威酩轩", "l"),
    ("Ruinart", "汇雅香槟", "LVMH 路威酩轩", "l"),
    ("Veuve Clicquot", "凯歌香槟", "LVMH 路威酩轩", "l"),
    ("Belvedere", "雪树伏特加", "LVMH 路威酩轩", "l"),
    ("Eminente", "埃米南特朗姆酒", "LVMH 路威酩轩", "l"),

    # ========== Kering 开云 ==========
    # 时装与皮具 f
    ("Gucci", "古驰", "Kering 开云", "f"),
    ("Saint Laurent", "圣罗兰", "Kering 开云", "f"),
    ("Bottega Veneta", "葆蝶家", "Kering 开云", "f"),
    ("Balenciaga", "巴黎世家", "Kering 开云", "f"),
    ("Alexander McQueen", "麦昆", "Kering 开云", "f"),
    ("Brioni", "布里奥尼", "Kering 开云", "f"),
    ("ALAIA", "阿莱亚", "Richemont 历峰", "f"),
    ("Chloe", "蔻依", "Richemont 历峰", "f"),
    ("G/FORE", "吉福", "Richemont 历峰", "f"),
    # 腕表与珠宝 w
    ("Boucheron", "宝诗龙", "Kering 开云", "w"),
    ("Pomellato", "宝曼兰朵", "Kering 开云", "w"),
    ("Qeelin", "麒麟", "Kering 开云", "w"),
    ("DoDo", "都都", "Kering 开云", "w"),
    ("Ginori 1735", "", "Kering 开云", "w"),
    # 眼镜 g
    ("Alexander McQueen眼镜", "麦昆眼镜", "Kering 开云", "g"),
    ("ALAIA眼镜", "阿莱亚眼镜", "Kering 开云", "g"),
    ("Bottega Veneta眼镜", "葆蝶家眼镜", "Kering 开云", "g"),
    ("Balenciaga眼镜", "巴黎世家眼镜", "Kering 开云", "g"),
    ("Cartier眼镜", "卡地亚眼镜", "Kering 开云", "g"),
    ("Chloe眼镜", "蔻依眼镜", "Kering 开云", "g"),
    ("Dunhill眼镜", "登喜路眼镜", "Kering 开云", "g"),
    ("Gucci眼镜", "古驰眼镜", "Kering 开云", "g"),
    ("Lindberg眼镜", "林德伯格眼镜", "Kering 开云", "g"),
    ("Montblanc眼镜", "万宝龙眼镜", "Kering 开云", "g"),
    ("Maui Jim眼镜", "茂宜晴眼镜", "Kering 开云", "g"),
    ("Puma眼镜", "彪马眼镜", "Kering 开云", "g"),
    ("Saint Laurent眼镜", "圣罗兰眼镜", "Kering 开云", "g"),
    ("ZEAL Optics", "ZEAL Optics", "Kering 开云", "g"),

    # ========== Richemont 历峰 ==========
    # 时装与皮具 f
    ("Purdey", "珀迪", "Richemont 历峰", "f"),
    ("Delvaux", "德尔沃", "Richemont 历峰", "f"),
    ("Montblanc", "万宝龙", "Richemont 历峰", "f"),
    ("Dunhill", "登喜路", "Richemont 历峰", "f"),
    ("Serapian", "塞拉皮安", "Richemont 历峰", "f"),
    ("Gianvito Rossi", "吉安维托罗西", "Richemont 历峰", "f"),
    ("Peter Millar", "彼得米拉", "Richemont 历峰", "f"),
    # 腕表 w
    ("A. Lange & Sohne", "朗格", "Richemont 历峰", "w"),
    ("Baume & Mercier", "名士", "Richemont 历峰", "w"),
    ("IWC Schaffhausen", "万国表", "Richemont 历峰", "w"),
    ("Jaeger-LeCoultre", "积家", "Richemont 历峰", "w"),
    ("Piaget", "伯爵", "Richemont 历峰", "w"),
    ("Panerai", "沛纳海", "Richemont 历峰", "w"),
    ("Roger Dubuis", "罗杰杜彼", "Richemont 历峰", "w"),
    ("Vacheron Constantin", "江诗丹顿", "Richemont 历峰", "w"),
    # 珠宝 w
    ("Buccellati", "布契拉提", "Richemont 历峰", "w"),
    ("Cartier", "卡地亚", "Richemont 历峰", "w"),
    ("Van Cleef & Arpels", "梵克雅宝", "Richemont 历峰", "w"),
    ("Vhernier", "维尔尼尔", "Richemont 历峰", "w"),

    # ========== Estee Lauder 雅诗兰黛 ==========
    # 高端护肤
    ("Darphin", "巴黎朵梵", "Estee Lauder 雅诗兰黛", "c"),
    ("Estee Lauder", "雅诗兰黛", "Estee Lauder 雅诗兰黛", "c"),
    ("La Mer", "海蓝之谜", "Estee Lauder 雅诗兰黛", "c"),
    # 大众护肤
    ("Aramis", "雅男士", "Estee Lauder 雅诗兰黛", "c"),
    ("Clinique", "倩碧", "Estee Lauder 雅诗兰黛", "c"),
    ("Dr. Jart+", "蒂佳婷", "Estee Lauder 雅诗兰黛", "c"),
    ("Glamglow", "格莱魅", "Estee Lauder 雅诗兰黛", "c"),
    ("Lab Series", "朗仕", "Estee Lauder 雅诗兰黛", "c"),
    ("Origins", "悦木之源", "Estee Lauder 雅诗兰黛", "c"),
    ("The Ordinary", "研度公式", "Estee Lauder 雅诗兰黛", "c"),
    # 彩妆
    ("Bobbi Brown", "芭比波朗", "Estee Lauder 雅诗兰黛", "c"),
    ("M.A.C", "魅可", "Estee Lauder 雅诗兰黛", "c"),
    ("Tom Ford Beauty", "汤姆福德美妆", "Estee Lauder 雅诗兰黛", "c"),
    ("Too Faced", "", "Estee Lauder 雅诗兰黛", "c"),
    # 香水
    ("AERIN", "雅芮", "Estee Lauder 雅诗兰黛", "c"),
    ("Editions de Parfums Frederic Malle", "馥马尔香水出版社", "Estee Lauder 雅诗兰黛", "c"),
    ("Jo Malone", "祖马龙", "Estee Lauder 雅诗兰黛", "c"),
    ("Kilian", "凯利安", "Estee Lauder 雅诗兰黛", "c"),
    ("Le Labo", "勒莱柏", "Estee Lauder 雅诗兰黛", "c"),
    # 护发美发
    ("Aveda", "艾梵达", "Estee Lauder 雅诗兰黛", "c"),
    ("Bumble and bumble", "", "Estee Lauder 雅诗兰黛", "c"),

    # ========== LOreal 欧莱雅 ==========
    # 高档化妆品 c
    ("Lancome", "兰蔻", "LOreal 欧莱雅", "c"),
    ("Yves Saint Laurent Beaute", "圣罗兰美妆", "LOreal 欧莱雅", "c"),
    ("Armani Beauty", "阿玛尼美妆", "LOreal 欧莱雅", "c"),
    ("Valentino Beauty", "华伦天奴美妆", "LOreal 欧莱雅", "c"),
    ("HR", "赫莲娜", "LOreal 欧莱雅", "c"),
    ("Miu Miu Beauty", "缪缪美妆", "LOreal 欧莱雅", "c"),
    ("Prada Beauty", "普拉达美妆", "LOreal 欧莱雅", "c"),
    ("Kiehls", "科颜氏", "LOreal 欧莱雅", "c"),
    ("Shu Uemura", "植村秀", "LOreal 欧莱雅", "c"),
    ("Atelier Cologne", "法国欧珑", "LOreal 欧莱雅", "c"),
    ("Aesop", "伊索", "LOreal 欧莱雅", "c"),
    ("Azzaro", "阿莎罗", "LOreal 欧莱雅", "c"),
    ("Biotherm", "碧欧泉", "LOreal 欧莱雅", "c"),
    ("Carita", "凯芮黛", "LOreal 欧莱雅", "c"),
    ("Cacharel", "卡夏尔", "LOreal 欧莱雅", "c"),
    ("Diesel Beauty", "迪赛美妆", "LOreal 欧莱雅", "c"),
    ("IT Cosmetics", "依科美", "LOreal 欧莱雅", "c"),
    ("Maison Margiela Fragrances", "梅森马吉拉香氛", "LOreal 欧莱雅", "c"),
    ("Mugler", "穆格勒", "LOreal 欧莱雅", "c"),
    ("Ralph Lauren Fragrances", "拉夫劳伦香氛", "LOreal 欧莱雅", "c"),
    ("Takami", "高见", "LOreal 欧莱雅", "c"),
    ("Urban Decay", "衰败城市", "LOreal 欧莱雅", "c"),
    ("Viktor & Rolf 美妆", "维果罗夫", "LOreal 欧莱雅", "c"),
    ("Yue Sai", "羽西", "LOreal 欧莱雅", "c"),
    ("Youth To The People", "", "LOreal 欧莱雅", "c"),
    # 大众化妆品
    ("LOreal Paris", "巴黎欧莱雅", "LOreal 欧莱雅", "c"),
    ("Dr.G", "蒂迩肌", "LOreal 欧莱雅", "c"),
    ("Essie", "艾茜", "LOreal 欧莱雅", "c"),
    ("Garnier", "卡尼尔", "LOreal 欧莱雅", "c"),
    ("Maybelline New York", "美宝莲纽约", "LOreal 欧莱雅", "c"),
    ("Mixa", "", "LOreal 欧莱雅", "c"),
    ("NYX Professional Makeup", "逆色", "LOreal 欧莱雅", "c"),
    ("Niely", "", "LOreal 欧莱雅", "c"),
    ("Thayers", "金缕梅", "LOreal 欧莱雅", "c"),
    ("Vogue", "", "LOreal 欧莱雅", "c"),
    ("3CE", "三熹玉", "LOreal 欧莱雅", "c"),
    # 专业美发
    ("Kerastase", "卡诗", "LOreal 欧莱雅", "c"),
    ("LOreal Professionnel", "欧莱雅PRO", "LOreal 欧莱雅", "c"),
    ("Biolage", "碧拉吉", "LOreal 欧莱雅", "c"),
    ("Matrix", "美奇丝", "LOreal 欧莱雅", "c"),
    ("Mizani", "", "LOreal 欧莱雅", "c"),
    ("Pureology", "", "LOreal 欧莱雅", "c"),
    ("Pulp Riot", "", "LOreal 欧莱雅", "c"),
    ("Redken", "丽得康", "LOreal 欧莱雅", "c"),
    ("Shu Uemura Art of Hair", "植村秀美发", "LOreal 欧莱雅", "c"),
    # 皮肤科学美容
    ("CeraVe", "适乐肤", "LOreal 欧莱雅", "c"),
    ("La Roche-Posay", "理肤泉", "LOreal 欧莱雅", "c"),
    ("SkinCeuticals", "修丽可", "LOreal 欧莱雅", "c"),
    ("Skinbetter Science", "斯佳博", "LOreal 欧莱雅", "c"),
    ("Vichy", "薇姿", "LOreal 欧莱雅", "c"),
    # 香水 c
    ("Alexander McQueen香水", "麦昆香水", "LOreal 欧莱雅", "c"),
    ("Bottega Veneta香水", "葆蝶家香水", "LOreal 欧莱雅", "c"),
    ("Balenciaga香水", "巴黎世家香水", "LOreal 欧莱雅", "c"),
    ("Creed", "恺芮得", "LOreal 欧莱雅", "c"),
    ("Pomellato香水", "宝曼兰朵香水", "LOreal 欧莱雅", "c"),
    ("Qeelin香水", "麒麟香水", "LOreal 欧莱雅", "c"),

    # ========== Swatch 斯沃琪 ==========
    # 高奢腕表
    ("Blancpain", "宝珀", "Swatch 斯沃琪", "w"),
    ("Breguet", "宝玑", "Swatch 斯沃琪", "w"),
    ("Glashutte Original", "格拉苏蒂原创", "Swatch 斯沃琪", "w"),
    ("Harry Winston", "海瑞温斯顿", "Swatch 斯沃琪", "w"),
    ("Jaquet Droz", "雅克德罗", "Swatch 斯沃琪", "w"),
    ("Omega", "欧米茄", "Swatch 斯沃琪", "w"),
    # 轻奢腕表
    ("Longines", "浪琴", "Swatch 斯沃琪", "w"),
    ("Rado", "雷达表", "Swatch 斯沃琪", "w"),
    # 中端腕表
    ("Balmain", "巴尔曼", "Swatch 斯沃琪", "w"),
    ("Certina", "雪铁纳", "Swatch 斯沃琪", "w"),
    ("Hamilton", "汉密尔顿", "Swatch 斯沃琪", "w"),
    ("Mido", "美度", "Swatch 斯沃琪", "w"),
    ("Tissot", "天梭", "Swatch 斯沃琪", "w"),
    # 大众腕表
    ("Calvin Klein", "卡尔文克莱恩", "Swatch 斯沃琪", "w"),
    ("Flik Flak", "飞菲", "Swatch 斯沃琪", "w"),
    ("Swatch", "斯沃琪", "Swatch 斯沃琪", "w"),

    # ========== OTB ==========
    ("Amiri", "埃米尔", "OTB 集团", "f"),
    ("Brave Kid", "儿童成衣配饰", "OTB 集团", "f"),
    ("Diesel", "迪赛", "OTB 集团", "f"),
    ("Jill Sander", "吉尔桑达", "OTB 集团", "f"),
    ("Maison Margiela", "梅森马吉拉", "OTB 集团", "f"),
    ("Marni", "玛尼", "OTB 集团", "f"),
    ("Viktor & Rolf 时装", "维果罗夫", "OTB 集团", "f"),

    # ========== 其他品牌（独立/独立集团）==========
    ("Acne Studios", "", "独立品牌", "f"),
    ("Ami", "阿米", "独立品牌", "f"),
    ("Ann Demeulemeester", "安迪穆拉米斯特", "独立品牌", "f"),
    ("Alo Yoga", "", "独立品牌", "f"),
    ("Brooks Brothers", "布克兄弟", "独立品牌", "f"),
    ("Club Monaco", "摩纳哥会馆", "独立品牌", "f"),
    ("Graff", "格拉夫", "独立品牌", "w"),
    ("Isabel Marant", "伊莎贝尔玛兰", "独立品牌", "f"),
    ("Lululemon", "露露乐蒙", "独立品牌", "f"),
    ("Moose Knuckles", "慕瑟纳可", "独立品牌", "f"),
    ("Margaret Howell", "玛格丽特霍威尔", "独立品牌", "f"),
    ("Mikimoto", "御木本", "独立品牌", "w"),
    ("Rick Owens", "瑞克欧文斯", "独立品牌", "f"),
    ("Tasaki", "塔思琦", "独立品牌", "w"),
    ("Vivienne Westwood", "薇薇安韦斯特伍德", "独立品牌", "f"),

    # ========== 安踏 ==========
    ("ANTA Sports", "安踏", "ANTA Sports 安踏", "f"),
    ("ANTA", "安踏", "ANTA Sports 安踏", "f"),
    ("Arc'teryx", "始祖鸟", "ANTA Sports 安踏", "f"),
    ("DESCENTE", "迪桑特", "ANTA Sports 安踏", "f"),
    ("FILA", "斐乐", "ANTA Sports 安踏", "f"),
    ("Jack Wolfskin", "狼爪", "ANTA Sports 安踏", "f"),
    ("KOLON Sport", "可隆", "ANTA Sports 安踏", "f"),
    ("Salomon", "萨洛蒙", "ANTA Sports 安踏", "f"),

    # ========== 其他 docx ==========
    # Aeffe Group
    ("Moschino", "莫斯奇诺", "Aeffe Group", "f"),
    # Burberry
    ("Burberry", "博柏利", "Burberry 集团", "f"),
    # Brunello Cucinelli
    ("Brunello Cucinelli", "布内罗古奇拉利", "Brunello Cucinelli 集团", "f"),
    # Chanel
    ("Chanel", "香奈儿", "Chanel 香奈儿集团", "f"),
    # Chelsey House
    ("Mackage", "迈凯奇", "Chelsey House 俏时屋", "f"),
    ("Sporty & Rich", "运动与富裕", "Chelsey House 俏时屋", "f"),
    ("r13", "", "Chelsey House 俏时屋", "f"),
    ("Zimmermann", "齐默尔曼", "Chelsey House 俏时屋", "f"),
    # Capri Holdings
    ("Michael Kors", "迈克高仕", "Capri Holdings 卡普里", "f"),
    ("Jimmy Choo", "周仰杰", "Capri Holdings 卡普里", "f"),
    ("Versace", "范思哲", "Prada Group 普拉达", "f"),
    # Dolce & Gabbana
    ("Dolce & Gabbana", "杜嘉班纳", "Dolce & Gabbana 杜嘉班纳", "f"),
    # Ermenegildo Zegna
    ("Ermenegildo Zegna", "杰尼亚", "Zegna 杰尼亚集团", "f"),
    ("Thom Browne", "桑姆布朗尼", "Zegna 杰尼亚集团", "f"),
    ("Zegna", "杰尼亚", "Zegna 杰尼亚集团", "f"),
    # Giorgio Armani
    ("Armani Exchange", "阿玛尼休闲", "Giorgio Armani 乔治阿玛尼", "f"),
    ("Emporio Armani", "安普里奥阿玛尼", "Giorgio Armani 乔治阿玛尼", "f"),
    ("Giorgio Armani", "乔治阿玛尼", "Giorgio Armani 乔治阿玛尼", "f"),
    # Hermes
    ("Hermes", "爱马仕", "Hermes 爱马仕集团", "f"),
    # Hugo Boss
    ("Boss", "博斯", "Hugo Boss 雨果博斯", "f"),
    ("Hugo", "雨果", "Hugo Boss 雨果博斯", "f"),
    # Lanvin Group
    ("Lanvin", "浪凡", "Lanvin Group 浪凡集团", "f"),
    ("Sergio Rossi", "塞乔罗西", "Lanvin Group 浪凡集团", "f"),
    # Max Mara
    ("Max Mara", "麦丝玛拉", "Max Mara 麦丝玛拉集团", "f"),
    ("Max Mara Studio", "", "Max Mara 麦丝玛拉集团", "f"),
    ("Max & Co.", "", "Max Mara 麦丝玛拉集团", "f"),
    ("S Max Mara", "", "Max Mara 麦丝玛拉集团", "f"),
    ("SportMax", "", "Max Mara 麦丝玛拉集团", "f"),
    ("Weekend Max Mara", "", "Max Mara 麦丝玛拉集团", "f"),
    # Moncler
    ("Moncler", "盟可睐", "Moncler 盟可睐集团", "f"),
    ("Stone Island", "石头岛", "Moncler 盟可睐集团", "f"),
    # Prada Group
    ("Church's", "", "Prada Group 普拉达", "f"),
    ("Car Shoe", "", "Prada Group 普拉达", "f"),
    ("Miu Miu", "缪缪", "Prada Group 普拉达", "f"),
    ("Prada", "普拉达", "Prada Group 普拉达", "f"),
    ("Dries Van Noten", "德赖斯范诺顿", "Prada Group 普拉达", "f"),
    # Puig
    ("Byredo", "柏芮朵", "Puig 普伊格", "c"),
    ("Christian Louboutin Beauty", "路铂廷", "Puig 普伊格", "c"),
    ("Charlotte Tilbury", "夏洛特蒂铂丽", "Puig 普伊格", "c"),
    ("L'Artisan Parfumeur", "阿蒂仙之香", "Puig 普伊格", "c"),
    ("Penhaligon's", "潘海利根", "Puig 普伊格", "c"),
    ("Uriage", "依泉", "Puig 普伊格", "c"),
    # Rolex
    ("Rolex", "劳力士", "Rolex 劳力士集团", "w"),
    ("Tudor", "帝舵", "Rolex 劳力士集团", "w"),
    # Tapestry
    ("Coach", "蔻驰", "Tapestry 泰佩思琦", "f"),
    ("Kate Spade", "凯特丝蓓", "Tapestry 泰佩思琦", "f"),
    ("Stuart Weitzman", "思缇韦曼", "Tapestry 泰佩思琦", "f"),
    ("Tapestry", "泰佩思琦", "Tapestry 泰佩思琦", "f"),
    # Salvatore Ferragamo
    ("Salvatore Ferragamo", "菲拉格慕", "Salvatore Ferragamo 菲拉格慕集团", "f"),
    ("Giovanni Valentino", "卓凡尼华伦天奴", "Valentino 华伦天奴集团", "f"),
    # TOD'S
    ("Fay", "斐", "TOD'S 集团", "f"),
    ("Hogan", "霍根", "TOD'S 集团", "f"),
    ("Roger Vivier", "罗杰维威耶", "TOD'S 集团", "f"),
    ("TOD'S", "托德斯", "TOD'S 集团", "f"),
    # Valentino
    ("Valentino", "华伦天奴", "Valentino 华伦天奴集团", "f"),
]

# 去重（同名不同集团视为独立条目，加入集团名做区分）
seen = set()
unique = []
for b in brands:
    key = b[0].lower().replace(' ','') + '|' + b[2].lower()
    if key not in seen:
        seen.add(key)
        unique.append(b)

print(f"品牌总数(去重): {len(unique)}")

# 生成JS数据
js_lines = ["const BRANDS = ["]
for en, cn, grp, typ in unique:
    cn_str = f'"{cn}"' if cn else '""'
    js_lines.append(f'  [{repr(en)}, {cn_str}, "{grp}", "{typ}"],')
js_lines.append("];")

with open(r'C:\Users\J nash\Desktop\workbuddy\品牌\quiz_data.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_lines))

print("已生成 quiz_data.js")
