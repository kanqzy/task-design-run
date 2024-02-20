# 图像工具

import os

import cv2
import numpy as np
from PIL import Image
import pyautogui

import util


def findSubImageLocation(
    main_image: str | np.ndarray,
    sub_image: str | np.ndarray,
    match_threshold: float = 0.8,
) -> list[int]:
    """
    查找子图像的位置

    可选参数:
        match_threshold (flaot): 匹配阈值
            在主图像中查找子图像, 进行匹配计算, 计算的匹配阈值只有大于等于当前参数值,
            才能判断为找到了该子图像

    返回:
        成功查找到子图像, 返回子图像位置 `[x1, y1, x2, y2]`; 反之返回 `None`
    """
    if isinstance(main_image, str):
        if not os.path.exists(main_image):
            return None
        main_image = cv2.imread(main_image)

    if isinstance(sub_image, str):
        if not os.path.exists(sub_image):
            return None
        sub_image = cv2.imread(sub_image)

    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    sub_gray = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
    
    result = None
    try:
        result = cv2.matchTemplate(main_gray, sub_gray, cv2.TM_CCOEFF_NORMED)
    except Exception as e:
        return None

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= match_threshold:
        top_left = max_loc
        bottom_right = (
            top_left[0] + sub_image.shape[1],
            top_left[1] + sub_image.shape[0],
        )
        x1, y1 = top_left
        x2, y2 = bottom_right

        return [x1, y1, x2, y2]

    return None


def check_isSubImage(
    image: str | np.ndarray, image_2: str | np.ndarray, match_threshold: float = 0.8
) -> dict:
    """
    检测图像 `image` 是否是 图像 `image_2`的 子图像

    返回:
        {
            isSubImage: bool,
            subLocation: [x1,y1,x2,y2]
        }
    """
    if isinstance(image, str):
        if not os.path.exists(image):
            return None
        image = cv2.imread(image)

    if isinstance(image_2, str):
        if not os.path.exists(image_2):
            return None
        image_2 = cv2.imread(image_2)

    subLocation = findSubImageLocation(image_2, image, match_threshold)
    if subLocation:
        return {"isSubImage": True, "subLocation": subLocation}

    return {"isSubImage": False}


def findScreenSubImageLocation(
    sub_image: str | np.ndarray,
    match_threshold: float = 0.8,
) -> list[int]:
    """
    查找屏幕子图像的位置

    可选参数:
        match_threshold (flaot): 匹配阈值
            在主图像中查找子图像, 进行匹配计算, 计算的匹配阈值只有大于等于当前参数值,
            才能判断为找到了该子图像

    返回:
        成功查找到子图像, 返回子图像位置 `[x1, y1, x2, y2]`; 反之返回 `None`
    """
    fullScreen_image = pyautogui.screenshot()
    main_image = np.array(fullScreen_image)

    return findSubImageLocation(main_image, sub_image, match_threshold)


def check_screen_window_match(winRect: list[int], compare_img_path: str) -> bool:
    """
    检测屏幕特定窗口区域的窗口是否与给定的图像匹配

    探测过程:
        截屏参数 `winRect`所代表的的窗口区域, 然后若检测该截屏包含子图像 `compare_img_path`, 则直接返回 `True`
        枚举不到匹配的窗口返回 `None`
    """
    x1, y1, x2, y2 = winRect
    screenshot_region = (x1, y1, x2 - x1, y2 - y1)
    screenshot_image = pyautogui.screenshot(region=screenshot_region)
    image_array = np.array(screenshot_image)
    check_result = check_isSubImage(compare_img_path, image_array)
    if check_result["isSubImage"]:
        return True

    return False
