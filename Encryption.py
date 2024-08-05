import cv2 as cv
import numpy as np
import os

def initialize_matrices():
    # 建立值矩阵
    date_matrix = np.zeros((256, 256), dtype=int)
    for i in range(256):
        date_matrix[255, i] = i % 16
    for i in range(254, -1, -1):
        for j in range(256):
            date_matrix[i, j] = (date_matrix[i + 1, j] + (4 if i % 2 == 0 else 5)) % 16

    # 建立类矩阵
    type_matrix = np.zeros((256, 256), dtype=int)
    type_matrix[255, 1] = 0
    type_matrix[255, 0] = 3
    for i in range(4, 256, 3):
        type_matrix[255, i] = (type_matrix[255, i - 3] + 1) % 4
    type_matrix[255, 2:255:3] = 3
    type_matrix[255, 3:255:3] = 3

    for i in range(254, 249, -1):
        for j in range(3, 255, 3):
            type_matrix[i, j:j + 3] = (type_matrix[i, j - 3] + 1) % 4

    for i in range(249, -1, -1):
        for j in range(0, 255, 3):
            type_matrix[i, j:j + 3] = (type_matrix[i + 5, j] + 2) % 4

    for i in range(250, 5, -5):
        for j in range(1, 255, 2):
            type_matrix[i, j] = int(type_matrix[i, j]) ^ int(type_matrix[i - 1, j])

    # 初始化编号矩阵
    no_matrix = np.zeros((256, 256), dtype=int)
    for i in range(0, 253, 11):
        for j in range(0, 252, 6):
            value = (i // 11 + j // 6) % 4
            no_matrix[i:i + 11, j:j + 6] = value
    for i in range(11, 253, 11):
        for j in range(0, 252, 6):
            no_matrix[i:i + 11, j:j + 6] = (no_matrix[i - 11, j:j + 6] + 2) % 4
    for i in range(11, 253, 11):
        for j in range(252, 256, 4):
            no_matrix[i:i + 11, j:j + 4] = (no_matrix[i - 11, j:j + 4] + 2) % 4

    return date_matrix, type_matrix, no_matrix

def spiral_search_with_condition(matrix1, matrix2, matrix3, x, y, a, b, c):
    rows = len(matrix1)
    cols = len(matrix1[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    curr_dir = 0
    curr_pos = (x, y)
    for _ in range(rows * cols):
        if matrix1[curr_pos[0]][curr_pos[1]] == a and matrix2[curr_pos[0]][curr_pos[1]] == b and matrix3[curr_pos[0]][curr_pos[1]] == c:
            return curr_pos
        visited[curr_pos[0]][curr_pos[1]] = True
        next_pos = (curr_pos[0] + dirs[curr_dir][0], curr_pos[1] + dirs[curr_dir][1])
        if (next_pos[0] < 0 or next_pos[0] >= rows or next_pos[1] < 0 or next_pos[1] >= cols):
            curr_dir = (curr_dir + 1) % 4
            next_pos = (curr_pos[0] + dirs[curr_dir][0], curr_pos[1] + dirs[curr_dir][1])
        if not visited[next_pos[0]][next_pos[1]]:
            curr_pos = next_pos
            curr_dir = (curr_dir + 1) % 4
        if visited[next_pos[0]][next_pos[1]]:
            curr_dir = curr_dir - 1
            if curr_dir == -1:
                curr_dir = 3
    return None

def hide_data(image_path, data):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    binary_data = '{0:018b}'.format(data)
    binary_index = 0

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            if binary_index < len(binary_data):
                pixel = bin(img[row, col])[2:].zfill(8)
                pixel = pixel[:-1] + binary_data[binary_index]
                img[row, col] = int(pixel, 2)
                binary_index += 1
            else:
                break
        if binary_index >= len(binary_data):
            break

    cv.imwrite("hidden.png", img)
    # print("Data hidden in image successfully.")

# 主函数
def main():
    image_path = 'img_1.png'
    if not os.path.exists(image_path):
        print(f"图像文件 {image_path} 不存在，请检查路径。")
        return

    img = cv.imread(image_path, 0)
    if img is None:
        print(f"无法读取图像文件 {image_path}，请检查文件是否损坏。")
        return

    # 获取图像的宽度和高度
    height, width = img.shape

    # 将每个像素的灰度值转换为8位二进制字符串，并将这些字符串存储在一个新的numpy数组中
    binary_pixels = np.vectorize(lambda x: format(x, '08b'))(img)

    # 将二维数组转换为一维数组，并将所有字符串连接起来
    binary_pixels_string = ''.join(binary_pixels.flatten())

    date_matrix, type_matrix, no_matrix = initialize_matrices()

    # 将二进制字符串转换为三部分：四进制、十六进制、四进制
    n = 8
    substrings = [binary_pixels_string[i:i + n] for i in range(0, len(binary_pixels_string), n)]
    int_array = []

    for s in substrings:
        first_two = int(s[:2], 2)
        middle_four = int(s[2:6], 2)
        last_two = int(s[6:], 2)
        int_array.extend([first_two, middle_four, last_two])

    # 将数据隐藏到图像中
    num = len(substrings) * 2
    hide_data("img.png", num)

    # 从图像中提取数据
    image = cv.imread("hidden.png", 0)
    w, h = image.shape
    date_array = [image[x, y] for x in range(w) for y in range(h) if (x * w + y) > 35][:len(substrings) * 2]

    pos_arr = []
    for i in range(0, len(substrings) * 2, 2):
        pos = spiral_search_with_condition(type_matrix, date_matrix, no_matrix, date_array[i], date_array[i + 1],
                                           int_array[3 * (i // 2)], int_array[3 * (i // 2) + 1], int_array[3 * (i // 2) + 2])
        pos_arr.extend(pos)

    # 将位置数组写入图像
    i = 0
    for x in range(w):
        if i == len(pos_arr):
            break
        for y in range(h):
            if (x * w + y) > 35:
                image[x, y] = pos_arr[i]
                i += 1
                if i == len(pos_arr):
                    break

    # 保存图像
    cv.imwrite("Dence_image.png", image)
    cv.waitKey()

if __name__ == "__main__":
    main()
