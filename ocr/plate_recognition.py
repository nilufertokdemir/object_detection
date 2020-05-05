#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import argparse
import collections
import csv
import datetime
import json
import math
import os
import time
from collections import OrderedDict
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import app

class Ocr:
    def parse_arguments(self, args_hook=lambda _: _):
        parser = argparse.ArgumentParser(
            description=
            'Read license plates from images and output the result as JSON.',
            epilog='Examples:\n'
            'To send images to our cloud service: '
            'python plate_recognition.py --api-key MY_API_KEY /path/to/vehicle-*.jpg\n',

            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-a', '--api-key', default='4db0c1a9113fe917f3dc316b4e2ac4904ebfd727')

        files = []
        for file in os.listdir("plates"):
            files.append("plates/"+file)
        parser.add_argument('-files', default=files)
        args_hook(parser)
        args = parser.parse_args()

        return args


    def recognition_api(self,fp,api_key):

        for _ in range(3):
            fp.seek(0)
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                files=dict(upload=fp),

                headers={'Authorization': 'Token ' + api_key})
            if response.status_code == 429:  # Max calls per second reached
                time.sleep(1)
            else:
                break

        if response.status_code < 200 or response.status_code > 300:
            print("1"+response.text)
            exit(1)
        return response.json(object_pairs_hook=OrderedDict)


    def blur(self, im, blur_amount, api_res):
        for res in api_res.get('results', []):
            b = res['box']
            width, height = b['xmax'] - b['xmin'], b['ymax'] - b['ymin']
            crop_box = (b['xmin'], b['ymin'], b['xmax'], b['ymax'])
            ic = im.crop(crop_box)

            # Increase amount of blur with size of bounding box
            blur_image = ic.filter(
                ImageFilter.GaussianBlur(radius=math.sqrt(width * height) * .3 *
                                         blur_amount / 10))
            im.paste(blur_image, crop_box)
        return im




    def flatten_dict(self, d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                if isinstance(v, list):
                    items.append((new_key, json.dumps(v)))
                else:
                    items.append((new_key, v))
        return dict(items)


    def flatten(self, result):
        plates = result['results']
        del result['results']
        del result['usage']
        if not plates:
            return result
        for plate in plates:
            data = result.copy()
            data.update(self.flatten_dict(plate))
        return data


    def save_results(self, results, args):
        path = Path(args.output_file)
        if not path.parent.exists():
            print('%s does not exist' % path)
            return
        if not results:
            return
        if args.format == 'json':
            with open(path, 'w') as fp:
                json.dump(results, fp)
        elif args.format == 'csv':
            fieldnames = []
            for result in results[:10]:
                candidate = self.flatten(result.copy()).keys()
                if len(fieldnames) < len(candidate):
                    fieldnames = candidate
            with open(path, 'w') as fp:
                writer = csv.DictWriter(fp, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    writer.writerow(self.flatten(result))



    def main(self):
        args = self.parse_arguments()
        paths = args.files
        results = []
        for path in paths:
            with open(path, 'rb') as fp:
                api_res = self.recognition_api(fp, args.api_key)
            results.append(api_res)

        for result in results:
            #print(result)
            result = result["results"]

            if len(result) != 0:

                #print(json.dumps(result[0].__getitem__("plate"), indent=2))
                json_data = {
                    "plate": result[0].__getitem__("plate"),
                    "time": str((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).isoformat()),
                    "camId": "111"

                }
                #print(json_data)
                app.postValues('http://localhost:3000/arac/', json_data)

