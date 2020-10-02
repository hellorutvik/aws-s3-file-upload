import uuid
import os
import boto3
from tqdm import tqdm


def random_filename(filepath):
    return str(uuid.uuid4()) + '-' + os.path.basename(filepath)


def write_text_file(content, filename, path):
    with open(os.path.join(path, filename), 'w') as file:
        file.write(content)


master = input('Path of Master : ')
sub_folders = os.listdir(master)

for parent_dir in sub_folders:
    s3 = boto3.client('s3')
    files = [os.path.join(master, parent_dir, file) for file in os.listdir(os.path.join(master, parent_dir)) if file != 'links.txt']
    urls = str()
    print(parent_dir)
    pbar = tqdm(total=len(files))
    for file in reversed(files):
        pbar.update(1)
        name = os.path.join(parent_dir, random_filename(file))
        s3_resource = boto3.resource('s3')
        second_object = s3_resource.Object('rangpeetara', name)
        second_object.upload_file(file, ExtraArgs={
            'ACL': 'public-read'})
        url = 'https://rangpeetara.s3.us-east-2.amazonaws.com/' + name
        urls = urls + url + '\n'
    write_text_file(urls, 'links.txt', os.path.join(master, parent_dir))
    pbar.close()
    print()
