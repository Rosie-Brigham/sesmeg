import os
import json
import requests
from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("json_file", "waterlogged-images.json", "Your name.")
flags.DEFINE_string("output_dir", "./groundwater/", "")


def download_img_and_label(img_url, lab_url, idx_):
    filename = img_url.split('?')[0].split('/')[-1]
    _, file_extension = os.path.splitext(filename)
    img_filename = os.path.join(FLAGS.output_dir, f'img_{idx_:03}{file_extension}')
    print(img_filename)
    lab_filename = os.path.join(FLAGS.output_dir, f'lab_{idx_:03}.png')
    if os.path.exists(img_filename):
        return
    r = requests.get(img_url)
    if r.ok:
        with open(img_filename, 'wb') as f:
            f.write(r.content)
    r = requests.get(lab_url)
    if r.ok:
        with open(lab_filename, 'wb') as f:
            f.write(r.content)                

def main(argv):
    if not os.path.exists(FLAGS.output_dir):
        os.makedirs(FLAGS.output_dir)
    with open(FLAGS.json_file) as json_file:
        data = json.load(json_file)
    for i, d in enumerate(data):
        try:
            label_uri = d['Label']['objects'][0]['instanceURI']
            image_uri = d['Labeled Data']
            download_img_and_label(image_uri, label_uri, i)
            print(f'Success {i}')
        except Exception as e:
            e_msg = str(e)[:60]
            print(f'Failure {i} {e_msg}')
        

if __name__ == '__main__':
  app.run(main)
