"""Class for the PDF Generator."""
import logging
from fpdf import FPDF

PAGE_SIZE = (210, 297)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # noqa: WPS323
logger = logging.getLogger(__name__)


class PDF(FPDF):
    """Create PDF Object.

    Args:
        FPDF (_type_): _description_
    """

    def set_logo_dx(self, logo_info):
        "Logo on theright."
        self.logo_dx = logo_info[0]
        self.logo_dx_x = logo_info[1]
        self.logo_dx_y = logo_info[2]
        self.logo_dx_w = logo_info[3]
        self.logo_dx_h = logo_info[4]

    def set_logo_sx(self, logo_info):
        "Logo on the left."
        self.logo_sx = logo_info[0]
        self.logo_sx_x = logo_info[1]
        self.logo_sx_y = logo_info[2]
        self.logo_sx_w = logo_info[3]
        self.logo_sx_h = logo_info[4]

    def header(self):
        """Create Header of the file."""
        # Logo on the right
        self.image(
            name=str(self.logo_dx),
            x=self.w - self.logo_dx_x,
            y=self.logo_dx_y,
            w=self.logo_dx_w,
            h=self.logo_dx_h,
        )

        # Logo on the left
        self.image(
            name=str(self.logo_sx),
            x=self.logo_sx_x,
            y=self.logo_sx_y,
            w=self.logo_sx_w,
            h=self.logo_sx_h,
        )
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 0, 0)
        title = self.title
        # Calculate width of title and position
        width = self.get_string_width(title) + 6
        self.set_x((self.w - width) / 2)

        # Colors of frame, background and text
        # self.set_draw_color(0, 80, 180)
        # self.set_fill_color(230, 230, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(0.1)
        # Title
        self.cell(w=width, h=9, txt=title, border=0, ln=1, align='C', fill=0)
        # Line break
        self.ln(15)

    def footer(self):
        """Create Footer of the file."""
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        page_number = str(self.page_no())
        self.cell(w=0, h=10, txt=f'Page {page_number}', border=0, ln=0, align='C')

    def chapter_title(self, num: int, label: str):
        """Set chapter titles.

        Args:
            num (int): Chapter number
            label (str): Chapter title text
        """
        # Arial 12
        self.set_font('Arial', '', 12)
        self.set_text_color(255, 255, 255)
        # Background color
        self.set_fill_color(5, 38, 62)
        # Title
        self.cell(w=0, h=6, txt=f'Chapter {num} : {label}', border=0, ln=1, align='L', fill=1)
        # Line break
        self.ln(4)

    def chapter_body(self, name: str, data_info: dict, image_info=()):
        """Creation of the body of the chapter

        Args:
            name (str): File name with text.
            data_info (dict): dataframe, label and table limit.
            image_info (Dict, optional): Name labgel and information of the images to print. Defaults to ().
        """
        # Read text file
        with open(name, 'r') as in_file:
            txt = in_file.read()

        self.set_font('Times', '', 12)
        self.set_text_color(0, 0, 0)
        # Output justified text
        self.multi_cell(w=0, h=5, txt=txt.encode('utf-8').decode('latin-1'), align='J')
        # Line break
        # self.ln()

        for key in data_info:
            df = data_info[key]['df']
            df_label = data_info[key]['label']
            table_limit = data_info[key]['table_limit']

            self.set_font('Times', '', 12)
            self.set_font('', 'BUI')
            self.ln()
            self.multi_cell(w=0, h=5, txt=df_label, align='C')
            self.ln()
            self.set_font('Times', '', 10)
            self.set_font('', 'BU')
            for col in df.columns:
                self.cell(w=table_limit[0], h=table_limit[1], txt=str(col), border=1, align='C')
            self.ln()
            self.set_font('', '')
            for _, row in df.iterrows():
                for _, row_data in enumerate(row.values):
                    self.cell(w=table_limit[0], h=table_limit[1], txt=str(row_data), border=1, align='C')
                self.ln()
        self.ln()

        if image_info:
            for _, image_x in enumerate(image_info):
                filename = image_info[image_x]['filename']
                image_label = image_info[image_x]['label']
                size_image = image_info[image_x]['size']
                pos_x_image = (((self.w - size_image[0]) / 2) - 2)
                label_image_space = 8
                if self.y + size_image[1] + label_image_space > self.page_break_trigger:
                    self.add_page()
                self.set_font('Times', '', 12)
                self.set_font('', 'BUI')
                self.cell(w=0, h=5, txt=image_label, align='C')
                self.ln(label_image_space)
                self.image(name=str(filename), w=size_image[0], h=size_image[1], x=pos_x_image)

                # print('PAGINA IMAGE 3', str(self.page_no()))

    def print_chapter(self, num, chp_title, name, data_info, image_info=()):
        """Print chapter.

        Args:
            num (int): Chapter number.
            chp_title (str): Chapter Title.
            name (str): File name with text.
            data_info (dict): dataframe, label and table limit.
            image_info (Disct, optional): Name labgel and information of the images to print. Defaults to ().
        """
        self.add_page()
        self.chapter_title(num, chp_title)
        self.chapter_body(name, data_info, image_info=image_info)
