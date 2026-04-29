from textnode import TextNode, TextType
import os
import shutil

def main():
    copy_static_to_main("static", "public")

def copy_static_to_main(content_path, destination_path):
    shutil.rmtree(destination_path)
    os.mkdir(destination_path)
    file_log = {"new_directory": [], "new_file": []}
    for item in os.listdir(content_path):
        item_path = "/".join([content_path, item])
        item_destination = "/".join([destination_path, item])
        if os.path.isfile(item_path):
            shutil.copy(item_path, item_destination)
            file_log["new_file"].append(item_path)
        else:
            os.mkdir(item_destination)
            file_log["new_directory"].append(item_destination)
            copy_static_to_main(item_path, item_destination)
    print(file_log)



main()
