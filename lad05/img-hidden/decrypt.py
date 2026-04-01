import sys
from PIL import Image


END_MARKER = '1111111111111110'


def decode_image(image_path):
    img = Image.open(image_path)
    width, height = img.size
    binary_data = ''

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))

            for i in range(3):
                binary_data += str(pixel[i] & 1)

                if binary_data.endswith(END_MARKER):
                    binary_data = binary_data[:-len(END_MARKER)]
                    message = ''

                    for j in range(0, len(binary_data), 8):
                        byte = binary_data[j:j + 8]
                        if len(byte) == 8:
                            message += chr(int(byte, 2))

                    return message

    return "Không tìm thấy thông điệp được giấu trong ảnh."


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python decrypt.py <duong_dan_anh>")
        print("Ví dụ: python decrypt.py encoded_image.jpg")
        return

    image_path = sys.argv[1]

    try:
        hidden_message = decode_image(image_path)
        print("Thông điệp giải mã được:", hidden_message)
    except Exception as e:
        print("Lỗi:", e)


if __name__ == "__main__":
    main()
