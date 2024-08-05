# Three-layer Pencil Matrix Encryption and Decryption

This repository contains two Python scripts for image encryption and decryption using a three-layer pencil matrix method.

## Files

- `Encryption.py`: Script for encrypting an image.
- `Decryption.py`: Script for decrypting an encrypted image.
- `img.png`: Example of cover image.
- `img_1.png`: Example of dense image .

## Requirements

- Python 3.9
- OpenCV
- NumPy
- Matplotlib

You can install the required Python libraries using:

```bash
pip install opencv-python numpy matplotlib
```

## Encryption

The `Encryption.py` script encrypts an image by hiding data within its pixels.

### Usage

1. Ensure you have an image named `img_1.png` in the same directory as the script.
2. Run the script:

```bash
python Encryption.py
```

3. The encrypted image will be saved as `Dence_image.png`.

### Function Descriptions

- `initialize_matrices()`: Initializes the matrices used for encryption.
- `spiral_search_with_condition()`: Searches through matrices to find positions that match specific conditions.
- `hide_data(image_path, data)`: Hides binary data within the pixels of an image.
- `main()`: The main function that orchestrates the encryption process.

## Decryption

The `Decryption.py` script decrypts an image that was encrypted using the `Encryption.py` script.

### Usage

1. Ensure you have the encrypted image named `Dence_image.png` in the same directory as the script.
2. Run the script:

```bash
python Decryption.py
```

3. The decrypted image will be displayed and saved as `gray_img.png`.

### Function Descriptions

- `initialize_matrices()`: Initializes the matrices used for decryption.
- `extract_data(image_path)`: Extracts hidden data from an image.
- `decrypt_image()`: The main function that orchestrates the decryption process.

## Example Images

Two example images (`img.png` and `img_1.png`) are provided to demonstrate the encryption and decryption process.

## Troubleshooting

If you encounter issues with OpenCV related to GUI functions (such as `cv.imshow`), you may need to reinstall OpenCV or use a headless version if you do not require GUI functionality.

```bash
pip uninstall opencv-python opencv-python-headless
pip install opencv-python
```

For environments without a display server, consider using `matplotlib` to display images instead of `cv.imshow`.

## License

This project is licensed under the Apache License 2.0 License.
