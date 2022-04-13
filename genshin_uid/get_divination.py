import json
import random
import time
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from base64 import b64encode
from io import BytesIO
import os
# 别挂配置数据

FILE_PATH = os.path.dirname(__file__)
FILE2_PATH = os.path.join(FILE_PATH, 'mihoyo_libs/mihoyo_bbs')
INDEX_PATH = os.path.join(FILE2_PATH, 'index')
gua_data_path=os.path.join(INDEX_PATH, "data.json")
bt = ImageFont.truetype(os.path.join(INDEX_PATH,"YangRenDongZhuShiTi-Regular-2.ttf"), 80)
gt = ImageFont.truetype(os.path.join(INDEX_PATH,"YangRenDongZhuShiTi-Regular-2.ttf"), 36)
gy = ImageFont.truetype(os.path.join(INDEX_PATH,"YangRenDongZhuShiTi-Regular-2.ttf"), 55)
cx = ImageFont.truetype(os.path.join(INDEX_PATH,"YangRenDongZhuShiTi-Regular-2.ttf"), 24)
img = Image.open(os.path.join(INDEX_PATH,"bugua.png"))


# 别卦数据
gua_data_map = {

}
fake_delay = 10


# 读取别卦数据
async def init_gua_data(json_path):
    with open(gua_data_path, 'r', encoding='utf8')as fp:
        global gua_data_map
        gua_data_map = json.load(fp)


# 爻图标映射
yao_icon_map = {
    0: "- -",
    1: "---"
}

# 经卦名
base_gua_name_map = {
    0: "坤", 1: "震", 2: "坎", 3: "兑", 4: "艮", 5: "离", 6: "巽", 7: "乾"
}


# 数字转化为二进制数组
async def base_gua_to_yao(gua, yao_length=3):
    result = []
    while gua >= 1:
        level = 0 if gua % 2 == 0 else 1
        gua //= 2
        result.append(level)
    while len(result) < yao_length:
        result.append(0)
    return result


# 二进制数组转化为数字
async def base_yao_to_gua(array):
    array = array[:]
    while len(array) > 0 and array[-1] == 0:
        array.pop()
    result = 0
    for i in range(len(array)):
        if array[i] == 0:
            continue
        result += pow(2, i)

    return result


# 打印一个挂
async def print_gua(gua):
    yao_list = await base_gua_to_yao(gua, 6)
    up_yao_list = yao_list[0:3]
    up = base_yao_to_gua(up_yao_list)

    print(yao_icon_map[up_yao_list[2]])
    print(yao_icon_map[up_yao_list[1]] + " " + base_gua_name_map[up])
    print(yao_icon_map[up_yao_list[0]])

    print("")

    down_yao_list = yao_list[3:6]
    down = base_yao_to_gua(down_yao_list)
    print(yao_icon_map[down_yao_list[2]])
    print(yao_icon_map[down_yao_list[1]] + " " + base_gua_name_map[down])
    print(yao_icon_map[down_yao_list[0]])

async def get_yao_gua(gua):
    yao_list =await base_gua_to_yao(gua, 6)
    up_yao_list = yao_list[0:3]
    up = base_yao_to_gua(up_yao_list)
    down_yao_list = yao_list[3:6]
    down = base_yao_to_gua(down_yao_list)
    return [base_gua_name_map[up],base_gua_name_map[down]]

async def paragraph(txt_,sum_width):
    paragraph = ""
    # 宽度总和

    re_line = 0
    line_len = 0
    for x in txt_:
        if line_len <= sum_width:
            paragraph += x
            line_len += 1
            re_line = 0
        else:
            paragraph += "\n" + x
            line_len = 0
    return paragraph
# 使用梅花易数
async def calculate_with_plum_flower(uid,nickname):
    await init_gua_data(gua_data_path)
    # bt = ImageFont.truetype("font/YangRenDongZhuShiTi-Regular-2.ttf", 80)
    # gt = ImageFont.truetype("font/YangRenDongZhuShiTi-Regular-2.ttf", 36)
    # gy = ImageFont.truetype("font/YangRenDongZhuShiTi-Regular-2.ttf", 55)
    # cx = ImageFont.truetype("font/YangRenDongZhuShiTi-Regular-2.ttf", 24)
    # img = Image.open("bugua.png")
    draw = ImageDraw.Draw(img)
    # 起上卦
    # print("使用梅花易数♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣")
    func="梅花易数"
    draw.text((900, 100), func, fill="#8B4513", font=bt)
    draw.text((800, 190), nickname, fill="#8B4513", font=bt)
    # print_a_wait_animation("卜上卦：", fake_delay)
    unit = 3600 * 24
    print(int(time.time()) / unit * unit - 8 * 3600 +uid)
    tt=int(time.time()) / unit * unit - 8 * 3600 +uid

    # up_base_gua = int(round(time.time() * 1000)) % 8
    up_base_gua = int(round(tt)) % 8
    up_yao_array = await base_gua_to_yao(up_base_gua)
    # draw.text((260, 80), base_gua_name_map[up_base_gua], fill="#363636", font=bt)
    draw.text((260, 80), base_gua_name_map[up_base_gua], fill="#8B4513", font=bt)
    # # 起下卦
    # print_a_wait_animation("正在获取下卦：", fake_delay)
    down_base_gua = random.randint(0, 999999999999) % 8
    down_yao_array = await base_gua_to_yao(down_base_gua)

    draw.text((260, 190), base_gua_name_map[down_base_gua], fill="#8B4513", font=bt)
    # # 组成卦象
    # print_a_wait_animation("正在组成本卦：", fake_delay)
    # print("------------------------------------------------本卦------------------------------------------------")
    yao_list = up_yao_array + down_yao_array
    gua = await base_yao_to_gua(yao_list)

    # print_gua(gua)
    up_yao,down_yao=await get_yao_gua(gua)
    draw.text((330, 335), up_yao, fill="#8B4513", font=gy)
    draw.text((500, 335), down_yao, fill="#8B4513", font=gy)
    # # 读取本卦象信息
    gua_code = str(base_gua_name_map[up_base_gua]) + str(base_gua_name_map[down_base_gua])

    gua_data = gua_data_map[gua_code]
    # print("本卦为:", gua_data['name'])
    # 卦爻
    draw.text((330, 335), up_yao, fill="#8B4513", font=gy)
    draw.text((500, 335), down_yao, fill="#8B4513", font=gy)
    draw.text((240, 410),gua_data['name'], fill="#8B4513", font=gt)

    # 卦辞象
    draw.text((150, 510), paragraph(gua_data['words'],17), fill="#8B4513", font=cx)
    draw.text((150, 650),paragraph(gua_data['white_words'],17), fill="#8B4513", font=cx)
    draw.text((150, 820), paragraph(gua_data['picture'],17), fill="#8B4513", font=cx)
    draw.text((150, 960),paragraph(gua_data['white_picture'],17), fill="#8B4513", font=cx)
    # print("------------------------------------------------互卦------------------------------------------------")
    # 读取互卦象信息
    up_hu_yao_list = [yao_list[4], yao_list[5], yao_list[0]]
    up_hu_gua = await base_yao_to_gua(up_hu_yao_list)
    down_hu_yao_list = [yao_list[5], yao_list[0], yao_list[1]]
    down_hu_gua = await base_yao_to_gua(down_hu_yao_list)
    hu_yao_list = up_hu_yao_list + down_hu_yao_list
    hu_gua =await base_yao_to_gua(hu_yao_list)
    hu_gua_code = str(base_gua_name_map[up_hu_gua]) + str(base_gua_name_map[down_hu_gua])
    hu_gua_data = gua_data_map[hu_gua_code]
    # print_gua(hu_gua)
    up_yao,down_yao=await get_yao_gua(hu_gua)
    # print(up_yao,down_yao)

    draw.text((950, 335), up_yao, fill="#8B4513", font=gy)
    draw.text((1120, 335), down_yao, fill="#8B4513", font=gy)
    draw.text((870, 410), hu_gua_data['name'], fill="#8B4513", font=gt)

    # 卦辞象
    draw.text((800, 510), paragraph(hu_gua_data['words'], 17), fill="#8B4513", font=cx)
    draw.text((800, 650), paragraph(hu_gua_data['white_words'], 17), fill="#8B4513", font=cx)
    draw.text((800, 820), paragraph(hu_gua_data['picture'], 17), fill="#8B4513", font=cx)
    draw.text((800, 960), paragraph(hu_gua_data['white_picture'], 17), fill="#8B4513", font=cx)

    # print("------------------------------------------------变卦------------------------------------------------")
    change_index = int(round(time.time() * 1000)) % 6
    change_yao_list = yao_list[:]
    change_yao_list[change_index] = 0 if change_yao_list[change_index] == 1 else 1
    up_change_yao_list = change_yao_list[0:3]
    up_change_gua = await base_yao_to_gua(up_change_yao_list)
    down_change_yao_list = change_yao_list[3:5]
    down_change_gua = await base_yao_to_gua(down_change_yao_list)

    change_gua = await base_yao_to_gua(change_yao_list)
    # print_gua(change_gua)

    up_yao,down_yao=get_yao_gua(change_gua)
    # print(up_yao,down_yao)
    change_gua_code = str(base_gua_name_map[up_change_gua]) + str(base_gua_name_map[down_change_gua])
    change_gua_data = gua_data_map[change_gua_code]
    # print("变卦为:", change_gua_data['name'])

    draw.text((1580, 335), up_yao, fill="#8B4513", font=gy)
    draw.text((1750, 335), down_yao, fill="#8B4513", font=gy)
    draw.text((1510, 410), change_gua_data['name'], fill="#8B4513", font=gt)

    # 卦辞象
    draw.text((1450, 510), paragraph(change_gua_data['words'], 17), fill="#8B4513", font=cx)
    draw.text((1450, 650), paragraph(change_gua_data['white_words'], 17), fill="#8B4513", font=cx)
    draw.text((1450, 820), paragraph(change_gua_data['picture'], 17), fill="#8B4513", font=cx)
    draw.text((1450, 960), paragraph(change_gua_data['white_picture'], 17), fill="#8B4513", font=cx)
    # img.show()
    bg_img = img.convert('RGB')
    result_buffer = BytesIO()
    bg_img.save(result_buffer, format='JPEG', subsampling=0, quality=90)
    # bg_img.save(result_buffer, format='PNG')
    imgmes = 'base64://' + b64encode(result_buffer.getvalue()).decode()
    # resultmes = f'[CQ:image,file={imgmes}]'
    resultmes = imgmes
    return resultmes


async def print_a_wait_animation(tips, times):
    animation = "|/-\\"
    idx = 0
    for i in range(times):
        print(tips + animation[idx % len(animation)], animation[idx % len(animation)], animation[idx % len(animation)],
              animation[idx % len(animation)], animation[idx % len(animation)], end="\r"),
        idx += 1
        time.sleep(0.1)


init_gua_data(gua_data_path)
# calculate_with_plum_flower()