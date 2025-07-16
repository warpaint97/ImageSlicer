from PIL import Image
import os
import platform

# ANSI color tags
GREEN = "\033[32m"
RED   = "\033[31m"
END   = "\033[0m"


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def file_prompt(prompt: str = "Enter image file path: ") -> str:
    while True:
        path = input(prompt).strip('"')
        if os.path.isfile(path):
            return path
        print(f"{RED}File not found: {path}{END}")


def dir_prompt(prompt: str, default_dir: str) -> str:
    while True:
        user_input = input(prompt).strip('"')
        path = default_dir if not user_input else user_input
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            print(f"{RED}Could not create directory: {e}{END}")
            continue
        if os.path.isdir(path):
            return path
        print(f"{RED}Invalid directory: {path}{END}")


def int_prompt(prompt: str = "Enter an integer: ") -> int:
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) > 0:
            return int(val)
        print(f"{RED}Invalid input, please enter a positive integer.{END}")


def slice_image(image_path: str, rows: int, cols: int, output_dir: str) -> None:
    img = Image.open(image_path)
    width, height = img.size
    tile_w = width // cols
    tile_h = height // rows

    print(f"Image size: {width}×{height}px -> each tile: {tile_w}×{tile_h}px")

    base_name = os.path.splitext(os.path.basename(image_path))[0]

    for row in range(rows):
        for col in range(cols):
            left = col * tile_w
            upper = row * tile_h
            right = left + tile_w
            lower = upper + tile_h
            box = (left, upper, right, lower)

            tile = img.crop(box)
            tile_name = f"{base_name}_r{row+1}_c{col+1}.png"
            tile_path = os.path.join(output_dir, tile_name)
            tile.save(tile_path)
            print(f"Saved: {tile_name}")

    print(f"{GREEN}Slicing completed: {rows*cols} tiles saved in '{output_dir}'.{END}")


if __name__ == "__main__":
    clear_screen()
    print("Image Grid Splitter")

    # Prompt user for inputs
    img_path = file_prompt("Path to the large image: ")
    rows = int_prompt("Number of rows: ")
    cols = int_prompt("Number of columns: ")

    # Default output directory next to input image
    base_dir = os.path.dirname(img_path)
    default_dir = os.path.join(base_dir, 'output_tiles')
    out_prompt = f"Output directory (press Enter for default '{default_dir}'): "
    out_dir = dir_prompt(out_prompt, default_dir)

    # Perform slicing
    slice_image(img_path, rows, cols, out_dir)

    input(f"{GREEN}Done!{END} Press Enter to exit.")