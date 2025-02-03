import logging

from pathlib import Path

import pandas as pd
import yaml
from class_pdf_report import PDF
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # noqa: WPS323
logger = logging.getLogger(__name__)


def data_preparation(config_pathfile: Path, output: Path, text_content: Path):
    """Preparation of the data for the chapters to print.

    Args:
        config_pathfile (Path): Path to the data folder
        output (Path): Path to the outpur folder
        text_content (Path): Path to the text and image to print

    """
    chp_content = text_content['chp_1']
    chp_number = chp_content['number']
    data_info = {}
    for idx, table_content in enumerate(chp_content['data_to_load']):
        table = chp_content['data_to_load'][table_content]

        table_filename = output / table['filename']
        table_label = table['label']
        table_filter = table['columns_to_filter']
        table_limit = table['table_limit']
        df_data = pd.read_csv(table_filename, decimal=',').round(1)
        table_one_col_rename = table['columns_to_rename']

        tab_one = df_data.loc[:, table_filter]
        # tab_one['Veicoli'] = tab_one['Veicoli'].astype(int)
        tab_one.rename(columns=table_one_col_rename, inplace=True)

        data_info[idx] = {
            'df': tab_one,
            'label': table_label,
            'table_limit': table_limit,
        }

    if chp_content['image_to_print']:
        image_info = {}
        for _, img in enumerate(chp_content['image_to_print']):
            img_data = chp_content['image_to_print'][img]

            df_data.set_index(img_data['set_index'], inplace=True)
            df_data.loc[
                :, img_data['columns_to_filter'],
            ].plot(grid=True)
            plt.xlabel('')
            plt.ylabel('%', rotation='horizontal')
            plt.xticks(fontsize=7)
            plt.savefig(output / img_data['save_img'])

            image_info[img] = {
                'filename': output / img_data['save_img'],
                'label': img_data['label'],
                'size': img_data['size'],
            }
            df_data.reset_index(inplace=True)

    pdf = PDF()

    pdf.set_title(f"{text_content['FILE_TITLE']}.pdf")

    pdf.print_chapter(
        chp_number,
        chp_content['title'],
        config_pathfile / chp_content['text'],
        data_info,
        image_info=image_info,
    )
    # --------------------------------------------------------------------------------------------------------------------------------

    pdf.output(output / text_content['FILE_TITLE'], 'F')


def create_report():
    """Start the main process."""
    logger.info('Radar Data Create Report Running')

    config_pathfile = Path(__file__).parent / 'config'
    output = Path(__file__).parent / 'output'
    with open(config_pathfile / 'pdf_text_content.yaml', 'r') as in_file:
        text_content = yaml.safe_load(in_file)

    data_preparation(config_pathfile, output, text_content)
    logger.info('Radar Data Create Report End')


if __name__ == '__main__':
    create_report()
