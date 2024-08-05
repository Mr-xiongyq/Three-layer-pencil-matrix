import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 封装矩阵初始化函数
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
            type_matrix[i, j] ^= type_matrix[i - 1, j]

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

# 提取数据函数
def extract_data(image_path):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    binary_data = ""
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            pixel = bin(img[row, col])[2:].zfill(8)
            binary_data += pixel[-1]
            if len(binary_data) == 18:
                break
        if len(binary_data) == 18:
            break
    extracted_data = int(binary_data, 2)
    return extracted_data

# 解密主函数
def decrypt_image():
    date_matrix, type_matrix, no_matrix = initialize_matrices()

    Dence_image = cv.imread("Dence_image.png", 0)
    count_pixel = extract_data("Dence_image.png")

    pos_arr1 = [0] * count_pixel
    int_arr1 = [0] * (3 * (count_pixel // 2))
    w1, h1 = Dence_image.shape

    i, number_c = 0, 0
    for x in range(w1):
        if i == count_pixel:
            break
        for y in range(h1):
            if number_c > 35:
                pos_arr1[i] = Dence_image[x, y]
                i += 1
                if i == count_pixel:
                    break
            number_c += 1

    for i in range(0, count_pixel, 2):
        int_arr1[3 * (i // 2)] = type_matrix[pos_arr1[i]][pos_arr1[i + 1]]
        int_arr1[3 * (i // 2) + 1] = date_matrix[pos_arr1[i]][pos_arr1[i + 1]]
        int_arr1[3 * (i // 2) + 2] = no_matrix[pos_arr1[i]][pos_arr1[i + 1]]

    arr = [""] * (count_pixel // 2)
    for i in range(0, count_pixel, 2):
        x = int_arr1[3 * (i // 2)]
        y = int_arr1[3 * (i // 2) + 1]
        z = int_arr1[3 * (i // 2) + 2]
        binary_x = format(x, 'b').zfill(2)
        binary_y = format(y, 'b').zfill(4)
        binary_z = format(z, 'b').zfill(2)
        arr[i // 2] = binary_x + binary_y + binary_z

    result = ''.join(arr)
    binary_pixels_chunks = [result[i:i + 8] for i in range(0, len(result), 8)]
    int_pixels = np.array([int(chunk, 2) for chunk in binary_pixels_chunks])
    side_length = int(np.sqrt(len(int_pixels)))
    gray_image = np.reshape(int_pixels, (side_length, side_length))

    cv.imwrite("gray_img.png", gray_image)
    plt.imshow(gray_image, cmap='gray')
    plt.show()

# 执行解密
if __name__ == "__main__":
    decrypt_image()
