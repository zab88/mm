from helpers.os_helper import OSUtils
import glob, os
import csv
from settings import *


def pdf_to_png(path_to_pdf_file, dir_aux='images/'):
    """Convert PDF file to PNG files, one PNG for each page in PDF"""
    dir_pdf, name_pdf, basename_pdf = OSUtils.checkout_path(path_to_pdf_file)
    dir_aux = dir_aux if len(dir_aux) else dir_pdf  # directory of PDF file by default
    pout, perr = OSUtils.run_subprocess(['pdftoppm', '-r', '300', '-png', path_to_pdf_file,
                                         dir_aux + basename_pdf])
    if len(perr) > 0:
        return [], perr
    else:
        img_paths = glob.glob(dir_aux + basename_pdf + '-[0-9].png')
        return img_paths, []


def img_to_xytext(path_to_img_file, dir_aux, page=1):
    """Extract tokens, relative coords and confidence levels from an image, dur_aux - full path to temp directory"""
    dir_img, name_img, basename_img = OSUtils.checkout_path(path_to_img_file)
    pout, perr = OSUtils.run_subprocess(['tesseract', path_to_img_file,
                                         dir_aux+basename_img, '--tessdata-dir', PATH_TESSDATA_PREFIX, 'tsv'])
    if len(perr) > 0 and not os.path.exists(dir_aux+basename_img+'.tsv'):
        return [], perr
    else:
        with open(dir_aux+basename_img+'.tsv', 'r', encoding="utf-8") as csv_file:
            tessreader = csv.reader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            next(tessreader)  # skip first line with field names
            res_xywh = []
            for row in tessreader:
                if len(row[11].strip()):
                    # level page_num	block_num	par_num	line_num	word_num	left	top	width	height	conf	text
                    res_xywh.append({
                        'page_num': page, 'block_num': row[2], 'line_num': row[4],
                        'x': int(row[6]), 'y': int(row[7]), 'w': int(row[8]), 'h': int(row[9]),
                        'txt': row[11]
                    })
        return res_xywh, perr
