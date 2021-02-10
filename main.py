import cv2
from easyocr import Reader

def recognize_text(pic_path, langs):
    def clean_text(text):                               # Удаляем non-acsii символы
        return "".join([c if ord(c) < 128 else "" for c in text]).strip()


    def del_dup(list_with_text):                 # Дроп дублей, тк eosr временами дублирует слова
        return " ".join(list(dict.fromkeys(list_with_text))).strip()


    image = cv2.imread('C:\\Users\\esus\\PycharmProjects\\eocr\\pics\\{}'.format(pic_path))


    reader = Reader(langs, gpu=False)

    results = reader.readtext(image)

    full_text = []
    for (bbox, text, prob) in results:
        full_text.append(text)

        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        text = clean_text(text)
        full_text.append(text)
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        cv2.putText(image, text, (tl[0], tl[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (1, 0, 1), 2)

    full_text = del_dup(full_text)
    pic_path = 'pics/recog_pics/'+pic_path.split('/')[1].split('.')[0] + '_1' + '.jpg' #страшные сплиты нужны для сохраниния картинки с бб
    cv2.imwrite(pic_path, image)
    return full_text, pic_path
