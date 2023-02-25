from fpdf import FPDF
import logging

logging.basicConfig(filename = 'app.log', filemode='a', level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s')

class create_pdf:
    def pdf(self, data):
        try:
            pdf_file = FPDF()
            pdf_file.add_page()

            pdf_file.set_font("Arial", size=15)
            for bundle in data.values():
                pdf_file.multi_cell(w = 0, h = 10, txt = bundle['bundle_name'], align = 'C')
                pdf_file.multi_cell(w = 0, h = 10, txt = '=> Description')
                for description in bundle['description']:
                    pdf_file.multi_cell(w = 0, h = 10, txt = description)
                pdf_file.multi_cell(w = 0, h = 10, txt = '=> Features')
                for feature in bundle['feature']:
                    pdf_file.multi_cell(w = 0, h = 10, txt = feature)
            pdf_file.output('data.pdf')
            logging.info('Document data.pdf Created')
        except Exception as e:
            logging.error(f'Failed PDF {e}')

