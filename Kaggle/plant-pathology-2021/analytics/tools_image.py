import numpy as np
import cv2  # opencv-python
from os.path import isfile

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from skimage.exposure import equalize_adapthist
from skimage.util import img_as_ubyte

from matplotlib.image import imread


def show_img(img, text=''):
    """Показывает изображение.
    :param img: путь к изображению
    """
    if isinstance(img, str) and not isfile(img):
        print(f'Не найден файл изображения: {img}')
        return None
        
    try:
        img = mpimg.imread(img)
    except Exception as e:
        print('Не удалось преобразовать картинку')
        print(e)
        pass
    plt.figure(figsize=(10, 15), )
    plt.imshow(img, cmap='gray')
    plt.title(text)
    plt.axis('off')
    plt.show()

def spectrum(img):
    """Показывает изображения в разных цветовых фильтрах. Отображается
    :param img: путь к изображению
    """
    red_channel = img.copy()
    # set blue and green channels to 0
    red_channel[:, :, 1] = 0
    red_channel[:, :, 2] = 0

    green_channel = img.copy()
    # set blue and red channels to 0
    green_channel[:, :, 0] = 0
    green_channel[:, :, 2] = 0

    blue_channel = img.copy()
    # set green and red channels to 0
    blue_channel[:, :, 0] = 0
    blue_channel[:, :, 1] = 0

    show_img(cv2.cvtColor(red_channel, cv2.COLOR_BGR2GRAY), 'red_channel')
    show_img(cv2.cvtColor(green_channel, cv2.COLOR_BGR2GRAY), 'green_channel')
    show_img(cv2.cvtColor(blue_channel, cv2.COLOR_BGR2GRAY), 'blue_channel')

def compare(img1, img2, title=''):
    """Показывает
    :param img: путь к изображению
    """
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(20, 15), sharex=True, sharey=True)
    ax1.imshow(img1, cmap='gray')
    ax1.set_title(title)
    ax1.axis('off')
    ax2.imshow(img2, cmap='gray')
    ax2.set_title(title)
    ax2.axis('off')
    plt.show()

def opencv2tensorflow(src):
    import tensorflow
    src = tensorflow.convert_to_tensor(src, dtype=tf.float32)
    return src

def skimage2opencv(src):
    src *= 255
    src.astype(int)
    cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    return src

def opencv2skimage(src):
    cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    src.astype(float32)
    src /= 255
    return src

def datatype_restore(img, to_dtype='uint8'):
    """Преобразует тип изображения из skimage в CV2"""
    if img.dtype != to_dtype:
        img = img_as_ubyte(img)
    return img

def crop_box(img, crop_size:int = 0):
    """Обрезает края изображения
    :param img: черно-белое opencv изображение (например, после cv2.COLOR_BGR2GRAY)
    :param int crop_size: сколько процентов ширины/высоты отступить от края изображения
    :return img: обрезанное opencv изображение
    """
    coeff = crop_size/100

    # обрезка краёв изображения (прямоугольником)
    width = img.shape[0]
    height = img.shape[1]

    img = img[int(width*coeff):int(width*(1-coeff)),
              int(height*coeff):int(height*(1-coeff))]

    return img

def split_channels(img, channel:str = '', gamma='BGR'):
    """Удаляет все цветовые каналы кроме заданных.
    :param img: цветное opencv изображение
    :param str channel: какой именно канал нужно выделить: 'blue' / 'red' / 'green'
    :param str gamma: гамма: 'BGR' / 'RGB'
    :return: opencv изображение, прошедшее через cv2.COLOR_BGR2GRAY
    """
    img = img.copy()

    if gamma == 'RGB':
        img = img[...,::-1]  # из BGR в RGB (аналогично можно обратно)

    if channel == 'red':
        img[:, :, 1] = 0
        img[:, :, 2] = 0
        return img
    elif channel == 'green':
        img[:, :, 0] = 0
        img[:, :, 2] = 0
        return img
    elif channel == 'blue':
        img[:, :, 0] = 0
        img[:, :, 1] = 0
        return img
    else: # все каналы
        red_channel = img.copy()
        # set blue and green channels to 0
        red_channel[:, :, 1] = 0
        red_channel[:, :, 2] = 0

        green_channel = img.copy()
        # set blue and red channels to 0
        green_channel[:, :, 0] = 0
        green_channel[:, :, 2] = 0

        blue_channel = img.copy()
        # set green and red channels to 0
        blue_channel[:, :, 0] = 0
        blue_channel[:, :, 1] = 0

        if gamma == 'BGR':
            return blue_channel, green_channel, red_channel
        if gamma == 'RGB':
            return red_channel, green_channel, blue_channel

def remove_edge_oval(img, crop_edge:int = 0):
    """Затемняет (удаляет значения) пикселей по краям изображения, используя маску
    овальной формы.
    :param img: черно-белое (!!!) opencv изображение (например, после cv2.COLOR_BGR2GRAY)
    :param int crop_edge: сколько процентов отступить от края изображения
    :return img, mask_oval: opencv изображения: обрезанное оригинальное и маска для обрезки
    """
    if isinstance(img, str):
        img = imread(path)

    # затемнение краёв изображения (овалом)
    width = img.shape[0]
    height = img.shape[1]
    mask_oval = np.zeros(img.shape, np.uint8)

    img_center = (int(height/2), int(width/2))  # центр картинки (кол-во пикселей)
    mask_radius = img_center

    if crop_edge: # края фигуры не будут соприкасаться с краями фото
        mask_radius = (int(img_center[0]), int(img_center[1]))

    mask_ar = cv2.ellipse(mask_oval, img_center, mask_radius, 0, 0, 360, (255, 255, 255), -1)

    assert img.shape == mask_oval.shape, f'Размеры маски и изображения не ' \
                                         f'совпадают! {img.shape} {mask_oval.shape}'

    img = cv2.bitwise_and(img, mask_oval)

    return img, mask_oval

def resize(image,
           width:int = None,
           height:int = None,
           shape:str = 'exact',
           interpolation=cv2.INTER_AREA):
    """Изменить размер изображения, (не)сохраняя пропорции.
    :param img: opencv изображение или путь к нему
    :param int width: ширина изображения после обработки
    :param int height: высота изображения после обработки
    :param str shape: значение "exact" - изменить строго в указанный размер, "proportional" - пропорционально
    :return img: opencv изображения с изменёнными размерами
    """
    """Изменить размер изображения. По умолчанию сохраняя пропорции"""
    if isinstance(image, str):
        image = imread(image)

    dim = None
    width = int(width)
    height = int(height)

    if (height, width) == image.shape[:2]: # изображение уже подготовлено
        return image

    if 'exact' in shape:  # изменить для точного совпадения с размерами
       dim = (width, height)

    if 'proport' in shape:  # пропорциональное изменение
      (h, w) = image.shape[:2]

      if width is None and height is None:
         return image

      if width is None:
         r = height / float(h)
         dim = (int(w * r), height)
      else:
         r = width / float(w)
         dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=interpolation)

def image_extract_object(img,
                     channel:str = '',
                     verbose:bool = False,
                     bin_size:int = 50,
                     bottom:int = 40,
                     top:int = 80):
    """Обрезает края изображения (по овалу), находит в оставшемся центре самый
    контрастный объект, определяет его границы и вырезает. Возвращает вырезанный
    объект.
    :param img: Путь к изображению или загруженное cv2/matplotlib изображение.
    :param bin_size: Минимальный размер точки для выделения контура объекта.
    :param channel: Цветовой канал изображения, который надо использовать
    :param bottom: Нижний порого фильтра cv2.Canny
    :param top: Верхний порого фильтра cv2.Canny
    :param verbose: Вывод дополнительной информации о процессе.
    :return: Изображение, размер объекта на изображении (в процентах).
    """
    if isinstance(img, str):
        img = imread(img)

    # предельные размеры контуров, которые находим на изображении
    num_pixels_in_picture = len(np.concatenate(img))
    min_contur_size = num_pixels_in_picture * 0.15
    max_contur_size = num_pixels_in_picture * 0.75

    # запоминаем состояние, чтобы потом из него вырезать по маске
    init_img = img.copy()

    # получим только один канал
    if channel:
        img = split_channels(img, channel)

        if channel == 'red':
            bin_size = 30
        if channel == 'green':
            bin_size = 14
        if channel == 'blue':
            bin_size = 45

    # преобразованием в серый цвет
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # повысим контрастность с помощью equalize_adapthist
    img = equalize_adapthist(img)
    img = img_as_ubyte(img)

    # canny
    canned = cv2.Canny(img, bottom, top)

    # dilate to close holes in lines
    kernel = np.ones((bin_size, bin_size), np.uint8)
    mask = cv2.dilate(canned, kernel, iterations = 1)

    # вырезаем овал изменно из маски. Если вырезать из изображения, то края
    # овала будут определены как контур объекта
    mask, mask_oval = remove_edge_oval(mask)

    # find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find big contours
    biggest_cntr = None
    biggest_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > biggest_area:
            biggest_area = area
            biggest_cntr = contour

    # draw contours
    crop_mask = np.zeros_like(mask)
    cv2.drawContours(crop_mask, [biggest_cntr], -1, (255), -1)

    # fill in holes
    # inverted
    inverted = cv2.bitwise_not(crop_mask)

    # contours again
    contours, _ = cv2.findContours(inverted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find small contours
    small_cntrs = [];
    for contour in contours:
        area = cv2.contourArea(contour)
        # берём только среднего размера контуры. Придумать, к чему привязать эту цифру!
        # if min_contur_size < area and area < max_contur_size: # берём только среднего размера контуры
        # if area < 20000: # берём только среднего размера контуры
        if area / min_contur_size < 0.00001 and area / min_contur_size < 0.01:
            small_cntrs.append(contour)

    # draw on mask
    cv2.drawContours(crop_mask, small_cntrs, -1, (255), -1);

    # opening + median blur to smooth jaggies
    crop_mask = cv2.erode(crop_mask, kernel, iterations = 1)
    crop_mask = cv2.dilate(crop_mask, kernel, iterations = 1)
    crop_mask = cv2.medianBlur(crop_mask, 5);

    # crop image
    crop = np.zeros_like(init_img)
    # crop[crop_mask == 255] = img[crop_mask == 255]  # даёт маску из серого цвета
    crop = cv2.bitwise_and(init_img, init_img, mask=crop_mask)

    # Получаем размер изображения в %, который получился после обрезки.
    # При этом учитывается, что основная форма, относительно которой надо
    # считать %, это овальная маска.
    mask_pix = np.sum(np.concatenate(crop_mask == 255))
    mask_pix_oval_total = np.sum(np.concatenate(mask_oval == 255))
    mask_size = 100 * mask_pix / mask_pix_oval_total  # сколько процентов занимает маска
    # print(f'Объект занимает {mask_size} % изображения')

    # plot_comparison(init_img, crop, path)

    return crop, mask_size

def increase_contrast(img, verbose:bool = False):
    """Увеличивает контрастность изображения.
    :param img: Путь к изображению или загруженное cv2/matplotlib изображение.
    :param verbose: Вывод дополнительной информации о процессе.
    :return: Изображение, размер объекта на изображении (в процентах).
    """
    if isinstance(img, str):
        img = imread(path)

    # повысим контрастность с помощью equalize_adapthist
    img = equalize_adapthist(img)
    img = img_as_ubyte(img)

    return img
