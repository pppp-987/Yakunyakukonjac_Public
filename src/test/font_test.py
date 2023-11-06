from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (1000, 1000))
draw = ImageDraw.Draw(img)
bbox_fill = None
bbox_outline = (255, 0, 0)


draw.rectangle((0, 100, 1000, 150), fill=bbox_fill, outline=bbox_outline)
draw.rectangle((0, 200, 1000, 250), fill=bbox_fill, outline=bbox_outline)
# font = ImageFont.truetype("segoeui.ttf", 50)
# text = "J"
# tl = (100, 100)
# print(tl)
# draw.text(tl, text, font=font)
# bbox = draw.textbbox(tl, text, font=font)
# print(bbox)
# draw.rectangle(bbox, fill=bbox_fill, outline=bbox_outline)

# tl = (bbox[0] + 50, bbox[1] - 25)
# draw.text(tl, text, font=font)


for lst in [
    [
        ("A", "segoeui.ttf", 100, 100),
        ("a", "segoeui.ttf", 200, 100),
        ("y", "segoeui.ttf", 300, 100),
        ("j", "segoeui.ttf", 400, 100),
        ("Æ", "segoeui.ttf", 500, 100),
        ("Ã", "segoeui.ttf", 600, 100),
        ("ç", "segoeui.ttf", 700, 100),
        ("ÿ", "segoeui.ttf", 800, 100),
        ("1", "segoeui.ttf", 900, 100),
    ],
    [
        ("Б", "segoeui.ttf", 100, 200),
        ("б", "segoeui.ttf", 200, 200),
        ("Ы", "segoeui.ttf", 300, 200),
        ("щ", "segoeui.ttf", 400, 200),
        ("ي", "segoeui.ttf", 400, 200),
        ("كيا", "segoeui.ttf", 500, 200),
        ("אקר", "segoeui.ttf", 600, 200),
        ("אתה", "segoeui.ttf", 700, 200),
    ],
    [
        ("あ", "msmincho.ttc", 100, 300),
        ("ア", "msmincho.ttc", 200, 300),
        ("A", "msmincho.ttc", 300, 300),
        ("a", "msmincho.ttc", 400, 300),
        ("y", "msmincho.ttc", 500, 300),
        ("j", "msmincho.ttc", 600, 300),
        ("1", "msmincho.ttc", 700, 300),
        ("あ", "msmincho.ttc", 100, 300),
    ],
    [
        ("讠", "msyh.ttc", 100, 400),
        ("戠", "msyh.ttc", 200, 400),
        ("罢", "msyh.ttc", 300, 400),
        ("贝", "msyh.ttc", 400, 400),
        ("1", "msyh.ttc", 500, 400),
    ],
    [
        ("ㅏ", "malgun.ttf", 100, 500),
        ("ㄱ", "malgun.ttf", 200, 500),
        ("가", "malgun.ttf", 300, 500),
        ("뮤", "malgun.ttf", 400, 500),
        ("뗘", "malgun.ttf", 500, 500),
        ("1", "malgun.ttf", 600, 500),
    ],
]:
    font_size = 50
    y = lst[0][3]
    draw.rectangle((0, y, 1000, y + font_size), fill=bbox_fill, outline=bbox_outline)
    for text, fontname, x, y in lst:
        font_size = 50
        if fontname != "msmincho.ttc":
            font_size = int(font_size * 2 / 3)
        font = ImageFont.truetype(fontname, font_size)
        tl = (x, y)
        draw.text(tl, text, font=font)
        bbox = draw.textbbox(tl, text, font=font)
        draw.rectangle(bbox, fill=bbox_fill, outline=bbox_outline)
        # tl = (x + 50, bbox[1])
        # draw.text(tl, text, font=font)
        # print(bbox)

    # font = ImageFont.truetype(fontname, 100)
    # tl = (x, 300)
    # draw.text(tl, text, font=font)
    # bbox = draw.textbbox(tl, text, font=font)
    # draw.rectangle(bbox, fill=bbox_fill, outline=bbox_outline)

    # tl = (x + 50, bbox[1])
    # draw.text(tl, text, font=font)
    # # print(bbox)
    # # draw.line((tl, (tl[0], tl[1] - 5)))

    # font = ImageFont.truetype(fontname, 10)
    # tl = (x, 500)
    # draw.multiline_text(tl, text, font=font)
    # bbox = draw.multiline_textbbox(tl, text, font=font)
    # draw.rectangle(bbox, fill=bbox_fill, outline=bbox_outline)
img.show()
