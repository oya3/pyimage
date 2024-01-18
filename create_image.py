from PIL import Image, ImageDraw, ImageFont, ImageOps
import argparse
import traceback

# フォントサイズは32.0としておく
FONT_SIZE = 32.0
# フォントは環境に応じて設定する
#  - windows: ＭＳ ゴシック: 'C:/Windows/Fonts/msgothic.ttc'
#  - ubuntu22.04: UbuntuMono: '/usr/share/fonts/truetype/ubuntu/UbuntuMono-RI.ttf'
FONT_NAME = '/usr/share/fonts/truetype/ubuntu/UbuntuMono-RI.ttf'

def font2PixcelSize(pt):
    '''
    フォントptからピクセルに変換
    '''
    return ((pt * 96.0) / 72.0)


def mm2PixcelSize(mm):
    '''
    mm からピクセルに変換
    '''
    return ((mm * 96.0) / 27)


def create_image(message):
    width = 200
    height = int(font2PixcelSize(FONT_SIZE))  # フォントサイズからピクセルの高さを計算
    image = Image.new('RGB', (width, height), (255, 255, 255))    # width x height のピクセル画像エリアを作成し、背景色は白色にする
    draw = ImageDraw.Draw(image)
    # 色は色見本文字列でも指定可能 ex: 'Red': (255, 0, 0) 
    #  https://www.colorhexa.com/color-names
    draw.line((0, 0, width, 0), fill=(255, 0, 0), width=1)  # 上部に赤線を引いておく
    draw.line((0, height-1, width, height-1), fill=(0, 255, 0), width=1)  # 下部に緑線を引いておく
    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuMono-RI.ttf', FONT_SIZE)
    anchor = 'la' # la=左, ma=中央, ra=右
    draw.text((0, 0), message, (0, 0, 0), spacing=0, align='left', anchor=anchor, font=font)  # message 文字列を描画する
    return image


def concat_image(base_image, add_image):
    # サイズはbase_imageを基準にする
    new_image = Image.new('RGB', (base_image.width, base_image.height + add_image.height))
    new_image.paste(base_image, (0, 0))  # base_image を書き込み
    new_image.paste(add_image, (0, base_image.height))  # add_image を base_image に下部に書き込み　
    return new_image


def main(args):
    image1 = create_image('image1')  # 画像１を作成
    image2 = create_image('image2')  # 画像２を作成
    new_image = concat_image(image1, image2)  # 画像１と画像２を結合して新画像を作成
    new_image.save(args.imagefile+'.PNG')  # 新画像からPNG 形式画像ファイルを出力。PNG指定はデフォルト。new_image.save(imagefile+'.PNG', 'PNG') と同じ
    # 指定可能なフォーマットは PNG, JPEG, PPM, GIF, TIFF, BMP ... JPEG,GIF をサンプル出力しておく
    new_image.save(args.imagefile+'.JPEG', 'JPEG')
    new_image.save(args.imagefile+'.GIF', 'GIF')


if __name__ == '__main__':  # プログラム実行ポイント
    try:
        # 入力引数設定
        parser = argparse.ArgumentParser(description='png画像生成')
        parser.add_argument('imagefile', help='image ファイル')  # 入力引数１：生成した画像を保存するファイル名
        args = parser.parse_args()  # 入力引数取得
        main(args)
    except Exception:  # main() で発生する異常はすべてキャッチする
        t = traceback.format_exc()
        print("ERROR: {}".format(t))


