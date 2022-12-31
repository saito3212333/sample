import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageEnhance
import io
import os
import pyocr

#テーマカラーを設定
sg.theme('Purple')

#TesseractのPath情報登録
TESSERACT_PATH = 'C:\\Users\\・・・・\\Tesseract-OCR' #インストールしたTesseract-OCRのpath
TESSDATA_PATH = 'C:\\Users\\・・・・\\Tesseract-OCR\\tessdata' #tessdataのpath
os.environ["PATH"] += os.pathsep + TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH

def ocr_tesseract(file_path):
    """Tesseractの日本語OCR関数 ※前回記事を関数にしただけ"""

    #OCRエンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    #OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)

    #解析画像読み込み(雨ニモマケズ)
    img = Image.open(file_path) #他の拡張子でもOK

    #適当に画像処理(もっとうまくやれば制度上がるかもです)
    img_g = img.convert('L') #Gray変換
    enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
    img_con = enhancer.enhance(2.0) #コントラストを上げる

    #画像からOCRで日本語を読んで、文字列として取り出す
    txt_pyocr = tool.image_to_string(img_con , lang='jpn', builder=builder)

    #半角スペースを消す ※読みやすくするため
    txt_pyocr = txt_pyocr.replace(' ', '')

    return txt_pyocr

def get_img_data(f, maxsize=(450, 450), first=False):
    """画像を読み込む関数"""
    global status_text #画像サイズをGUI表示させるためにグローバル変数で関数外でも参照できるようにする
    img = Image.open(f)
    status_text = "%d x %d" % img.size  # オリジナルの画像サイズ
    img.thumbnail(maxsize) #アスペクト比を維持しながら、指定したサイズ以下の画像に縮小
    status_text += " (%d x %d)" % img.size  # 縮小された画像サイズ
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

#GUIへ初期画像を登録する(適当にパワポとかで作ってもOK)
fname_first = './new_app/初期画像.png'
image_elem = sg.Image(data=get_img_data(fname_first, first=True))

#画像サイズを表示させる部分を変数化しておく(画像毎にアップデートさせるため)
status_elem = sg.Text(key='-STATUS-', size=(64, 1))

#フレーム1
frame1 = sg.Frame('',
    [
        # テキストレイアウト
        [
            sg.Text('①画像選択ボタンを押してOCRを行いたい画像を選んでね', font=('メイリオ',12))
        ],
        #画像選択ボタン
        [
            sg.Text("ファイル"),
            sg.InputText('ファイルを選択', key='-INPUTTEXT-', enable_events=True,),
            sg.FileBrowse(button_text='画像選択', font=('メイリオ',8), size=(8,3), key="-FILENAME-")
        ],
        # テキストレイアウト
        [
            sg.Text("②画像を選択したらOCR開始ボタンを押してね", font=('メイリオ',12)),
        ],
        #画像サイズ表示
        [
            sg.Text("元画像サイズ(GUI表示画像サイズ) : "),
            status_elem
        ],
        #画像表示 ※初期画面では自分で用意した適当な画像を表示
        [
            image_elem,
        ],
        #OCR開始ボタン
        [
            sg.Submit(button_text='OCR開始',
                      font=('メイリオ',8),size=(8,3),key='button_ocr')
        ]
    ], size=(500, 700)
)

#フレーム2
frame2 = sg.Frame('',
    [
        # テキストレイアウト
        [
            sg.Text("OCR結果"),
        ],
        # MLineでテキストエリアを作成。sizeは「**列×**行」を表している
        [
            sg.MLine(font=('メイリオ',8), size=(50,60), key='-OUTPUT-'),
        ]
    ] , size=(400, 700)
)

#左と右のフレームを合体させた全体レイアウト
layout = [
    [
        frame1,
        frame2
    ]
]

#GUIタイトルと全体レイアウトをのせたWindowを定義する
window = sg.Window('日本語OCR実行アプリ', layout, resizable=True)

#GUI表示実行部分
while True:
    # ウィンドウ表示 ※eventがイベント発生、valuesはその際の中身
    event, values = window.read()

    #クローズボタンの処理
    if event is None:
        print('exit')
        break

    #何かファイルが選択され、inputテキストエリアに書かれたpathが存在する場合のイベント処理
    if values['-FILENAME-'] != '': #-FILENAME-で選択した画像pathのpathをvaluesで取得
        if os.path.isfile(values['-INPUTTEXT-']): #選択したファイル(テキストエリアに転記)が存在した場合の処理
            global img_path #選択した画像Pathを記憶させておく
            try:
                img_path = values['-INPUTTEXT-'] #OCR用に画像Path取得
                image_elem.update(data=get_img_data(values['-INPUTTEXT-'], first=True)) #画像表示エリアをアップデート
                status_elem.update(status_text) #画像サイズ表示部分をアップデート
            except: #例外処理 ※うまく画像が読めなかったりした場合
                error_massage = values['-INPUTTEXT-'] + ' を画像として読み込めません'
                sg.popup('画像読み込みエラー', error_massage) #エラーのポップアップを表示
                image_elem.update(data=get_img_data(fname_first, first=True)) #画像を初期画像に戻す

    #OCR開始ボタンを押したときのアクション
    if event == 'button_ocr':
        try:
            text_ocr = ocr_tesseract(img_path) #取得した画像PathをOCR関数へ渡す
            window.FindElement('-OUTPUT-').Update(text_ocr) #フレーム2の出力テキストエリアをアップデート
        except: #例外処理
            error_massage = img_path + ' をOCRできませんでした'
            sg.popup('OCRエラー', error_massage) #エラーのポップアップを表示

window.close()