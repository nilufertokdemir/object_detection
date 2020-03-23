import argparse
import os

import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F

import cv2

from utils import CTCLabelConverter, AttnLabelConverter
from dataset import RawDataset, AlignCollate
from model import Model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Ocr:

    def resize_image(self):

        numbers = []

        for file in os.listdir("plates"):

            img = cv2.imread("plates/"+file, 0)
            for num in os.listdir("demo_image"):
                numbers.append(num.split("_")[1])

            numbers_sorted = sorted(numbers)
            size = len(numbers)


            if size == 0:
                next_number = 1
            else:
                next_number = int(numbers_sorted[size - 1].split(".")[0]) + 1

            width = 300
            height = 90
            dim = (width, height)

            resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)# resize image

            cv2.imwrite('results/plates_' + str(next_number) + '.jpeg',resized)

            original_image = cv2.imread('results/plates_' + str(next_number) + '.jpeg')

            cropped1= original_image[0:89, 42:106]
            cropped2= original_image[0:89, 106:191]
            cropped3= original_image[0:89, 191:284]

            images = [];

            images.append(cropped1);
            images.append(cropped2);
            images.append(cropped3);

            j=0;

            for i in images:
                j+=1
                cv2.imwrite('demo_image/cropped_'+str(j)+'.png',i)




    def demo(self):
        opt = self.get_args()
        self.resize_image()

        if 'CTC' in opt.Prediction:
            converter = CTCLabelConverter(opt.character)
        else:
            converter = AttnLabelConverter(opt.character)
        opt.num_class = len(converter.character)

        if opt.rgb:
            opt.input_channel = 3
        model = Model(opt)

        model = torch.nn.DataParallel(model).to(device)

        model.load_state_dict(torch.load(opt.saved_model, map_location=device))

        AlignCollate_demo = AlignCollate(imgH=opt.imgH, imgW=opt.imgW, keep_ratio_with_pad=opt.PAD)
        demo_data = RawDataset(root=opt.image_folder, opt=opt)  # use RawDataset
        demo_loader = torch.utils.data.DataLoader(
            demo_data, batch_size=opt.batch_size,
            shuffle=False,
            num_workers=int(opt.workers),
            collate_fn=AlignCollate_demo, pin_memory=True)

        # predict
        model.eval()
        with torch.no_grad():
            for image_tensors, image_path_list in demo_loader:
                batch_size = image_tensors.size(0)
                image = image_tensors.to(device)
                # For max length prediction
                length_for_pred = torch.IntTensor([opt.batch_max_length] * batch_size).to(device)
                text_for_pred = torch.LongTensor(batch_size, opt.batch_max_length + 1).fill_(0).to(device)

                if 'CTC' in opt.Prediction:
                    preds = model(image, text_for_pred)

                    # Select max probabilty (greedy decoding) then decode index to character
                    preds_size = torch.IntTensor([preds.size(1)] * batch_size)
                    _, preds_index = preds.max(2)
                    preds_index = preds_index.view(-1)
                    preds_str = converter.decode(preds_index.data, preds_size.data)

                else:
                    preds = model(image, text_for_pred, is_train=False)

                    # select max probabilty (greedy decoding) then decode index to character
                    _, preds_index = preds.max(2)
                    preds_str = converter.decode(preds_index, length_for_pred)


                log = open(f'./log_demo_result.txt', 'a')
                dashed_line = '-' * 80
                head = f'{"image_path":25s}\t{"predicted_labels":25s}\tconfidence score'

                print(f'{dashed_line}\n{head}\n{dashed_line}')
                log.write(f'{dashed_line}\n{head}\n{dashed_line}\n')

                preds_prob = F.softmax(preds, dim=2)
                preds_max_prob, _ = preds_prob.max(dim=2)
                for img_name, pred, pred_max_prob in zip(image_path_list, preds_str, preds_max_prob):
                    if 'Attn' in opt.Prediction:
                        pred_EOS = pred.find('[s]')
                        pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
                        pred_max_prob = pred_max_prob[:pred_EOS]

                    # calculate confidence score (= multiply of pred_max_prob)
                    confidence_score = pred_max_prob.cumprod(dim=0)[-1]

                    print(f'{img_name:25s}\t{pred:25s}\t{confidence_score:0.4f}')
                    log.write(f'{img_name:25s}\t{pred:25s}\t{confidence_score:0.4f}\n')

                log.close()

    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('--image_folder', default = "demo_image/", help='path to image_folder which contains text images')
        parser.add_argument('--workers', type=int, help='number of data loading workers', default=4)
        parser.add_argument('--batch_size', type=int, default=192, help='input batch size')
        parser.add_argument('--saved_model', default = "TPS-ResNet-BiLSTM-Attn.pth", help="path to saved_model to evaluation")
        """ Data processing """
        parser.add_argument('--batch_max_length', type=int, default=25, help='maximum-label-length')
        parser.add_argument('--imgH', type=int, default=32, help='the height of the input image')
        parser.add_argument('--imgW', type=int, default=100, help='the width of the input image')
        parser.add_argument('--rgb', action='store_true', help='use rgb input')
        parser.add_argument('--character', type=str, default='0123456789abcdefghijklmnopqrstuvwxyz', help='character label')
        parser.add_argument('--sensitive', action='store_true', help='for sensitive character mode')
        parser.add_argument('--PAD', action='store_true', help='whether to keep ratio then pad for image resize')
        """ Model Architecture """
        parser.add_argument('--Transformation', type=str, default = "TPS", help='Transformation stage. None|TPS')
        parser.add_argument('--FeatureExtraction', type=str, default = "ResNet", help='FeatureExtraction stage. VGG|RCNN|ResNet')
        parser.add_argument('--SequenceModeling', type=str, default="BiLSTM", help='SequenceModeling stage. None|BiLSTM')
        parser.add_argument('--Prediction', type=str, default= "Attn", help='Prediction stage. CTC|Attn')
        parser.add_argument('--num_fiducial', type=int, default=20, help='number of fiducial points of TPS-STN')
        parser.add_argument('--input_channel', type=int, default=1, help='the number of input channel of Feature extractor')
        parser.add_argument('--output_channel', type=int, default=512,
                            help='the number of output channel of Feature extractor')
        parser.add_argument('--hidden_size', type=int, default=256, help='the size of the LSTM hidden state')

        opt = parser.parse_args()

        cudnn.benchmark = True
        cudnn.deterministic = True
        opt.num_gpu = torch.cuda.device_count()

        return opt
