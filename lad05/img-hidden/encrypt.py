import sys
from PIL import Image


def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    pixel_index = 0

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Đánh dấu kết thúc thông điệp

    if len(binary_message) > width * height * 3:
        raise ValueError("Thông điệp quá dài, không thể giấu vào ảnh này.")

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))

            for i in range(3):
                if pixel_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[pixel_index])
                    pixel_index += 1

            img.putpixel((x, y), tuple(pixel))

            if pixel_index >= len(binary_message):
                img.save("encoded_image.jpg", format="PNG")
                print("Đã giấu tin thành công vào file encoded_image.jpg")
                return


def main():
    if len(sys.argv) < 3:
        print("Cách dùng: python encrypt.py <duong_dan_anh> <thong_diep>")
        print("Ví dụ: python encrypt.py image.jpg \"Hello HUTECH\"")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]

    try:
        encode_image(image_path, message)
    except Exception as e:
        print("Lỗi:", e)


if __name__ == "__main__":
    main()
