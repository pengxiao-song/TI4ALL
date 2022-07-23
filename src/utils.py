import logging
import multiprocessing as mul
import os
import re
import sys

import pandas as pd
import yaml
from paddleocr import PaddleOCR
from styleframe import StyleFrame, Styler

# 加载模型
def load_model():
    return PaddleOCR(
        lang='ch',
        show_log=False,
        enable_mkldnn=True,
        use_tensorrt=True,
        ocr_version='PP-OCRv2' # {PP-OCR,PP-OCRv2,PP-OCRv3}
    )
    
# 加载图片
def load_images(dir_name):
    imgfiles = [os.path.join(dir_name, img) for img in os.listdir(dir_name)
                 if os.path.splitext(img)[-1] in ['.jpg', '.png']]
    return imgfiles

# 加载辅助信息
def load_info(info_file):
    info = pd.read_excel(info_file, dtype=str)
    
    dict_id_to_item = {}
    dict_mask_to_id = {}
    
    info_list = info.to_dict('records')
    for i in info_list:
        dict_id_to_item[i['身份证号码']] = i
    
    # dict_mask_to_id
    ids = [id for id in info['身份证号码'].tolist()] 
    for id in ids:
        mask_id = id[:6] + '********' + id[-4:]
        dict_mask_to_id[mask_id] = id
    
    return dict_id_to_item, dict_mask_to_id


# 预处理检测文本
def get_message(raw_data):
    words = []
    for word in raw_data:
        word = word.replace('：', '')
        word = word.replace(':', '')
        words.append(word)
    return ' '.join(words)

# 正则表达式信息提取
def extract_info(message):
    info_dict = {}

    # match id
    id_pat = re.compile('\d{6}[*]*\d{3}[\d|X|x]')
    try:
        id_loc = re.search(id_pat, message).span()
        mask_id = message[id_loc[0]: id_loc[0] + 6] + '********' + message[id_loc[1] - 4: id_loc[1]]
    except Exception as e:
        mask_id = 'idnull'
        
    # match name
    name_pat = re.compile('姓名\s(.*?)\s')
    try:
        name_loc = re.search(name_pat, message).regs[1]
        name = message[name_loc[0]: name_loc[1]].replace(' ', '')
    except Exception as e:
        name = 'namenull'
        
    # match date
    date_pat = re.compile('\d{4}-\d{2}-\d{2}')
    dates = re.findall(date_pat, message)

    info_dict['身份证号码'] = mask_id
    info_dict['姓名'] = name
    for i, date in enumerate(dates):
        info_dict['最近{}次'.format(str(i + 1))] = date

    return info_dict

# 单个核算报告检测接口
def get_info_from_image(ocr : PaddleOCR, image):
    results = ocr.ocr(image, cls=False)
    words = [result[-1][0] for result in results]

    message = get_message(words)
    info = extract_info(message)
    info['图片'] = image
    return info

# 结构化识别结果到文件
def save_info_to_file(dict_id_to_item, save_file):
    
    df = pd.DataFrame.from_dict(dict_id_to_item.values())
    titles = df.columns.to_list()
    
    sf = StyleFrame(df)
    sf.apply_column_style(cols_to_style=titles,
                          styler_obj=Styler(font='Calibri'))
    
    ew = StyleFrame.ExcelWriter(save_file)
    sf.to_excel(ew, index=False, best_fit=titles)
    ew.save()


# 存取配置文件
def load_config_from_yaml(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config

def save_config_to_yaml(config, config_file):
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, Dumper=yaml.Dumper)


# 多核相关
def load_model_to_obj(runtime):
    model = load_model()
    runtime["model"] = model

def run_one_batch_multi_process(images : list, q : mul.Queue):
    model = load_model()
    for image in images:
        try:
            results = model.ocr(image, cls=False)
            words = [result[-1][0] for result in results]
            message = get_message(words)
            info = extract_info(message)
            info["图片"] = image
            q.put(info)
        except Exception as e:
            q.put({'error' : e})
        

class Logger(object):
    def __init__(self, logger_name, out_path, CLEVEL=logging.DEBUG, FLEVEL=logging.DEBUG):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        
        # set formatter
        fmt = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        
        # create console handler
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(CLEVEL)
        
        # create file handler
        fh = logging.FileHandler(out_path, encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(FLEVEL)
        
        # load to logger
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
        
    def write(self, message):
        sys.stdout.write(message)
        self.log.write(message)
        self.flush()
        
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
