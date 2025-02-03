"""Start the program."""
import fire
import general_pdf_report



def run_generator():
    """Start the extraction process for rvr data."""
    general_pdf_report.create_report()



if __name__ == '__main__':
    fire.Fire({
        'run': run_generator,
    })
