from pathlib import Path
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image

class PdfEditor:
    def __init__(self,path_list='') -> None:
        if len(path_list) == 0:
            print('Sorry files do not exist please try again')
            return None
        else:
            print('loading files')
            for f in path_list:
                # print(type(f))
                if f.exists() and f.glob('*.pdf'):
                    print('.')
                    self.FileType='pdf'
                elif f.exists() and (f.glob('*.jpg') or f.glob('*.png') or f.glob('*.jpeg')):
                    print('*')
                    self.FileType='pic'
                else:
                    print('Invalid file type supplied')
                    return 0
        self.path_list=path_list
        print(str(self.path_list))
        print('Files loaded successfully')

                
    def write_pdf(self,finalpdf_obj, file_name='sample.pdf'):
        with Path(file_name).open(mode="wb") as output_file:
            finalpdf_obj.write(output_file)
    def pdf_merge(self,savepath=''):
        
        pdf_merger = PdfFileMerger()
        for f in self.path_list:
            pdf_merger.append(str(f))
        savepath=savepath+'\\'+str(f.name)
        self.write_pdf(finalpdf_obj=pdf_merger,file_name=savepath)
        print('Pdfs merged succesfully')
        return True
        # with Path("full_pdf.pdf").open(mode="wb") as output_file:
        #     print('all the pdf files merged')
        #     pdf_merger.write(output_file)

    def extract_page(self,page_nos=[1],range=1):
        pdf_writer = PdfFileWriter()
        count=0
        for f in self.path_list:
            input_pdf = PdfFileReader(str(f))
            if range:
                extracted_page=input_pdf.pages[page_nos[0],page_nos[1]]
                pdf_writer.addPage(extracted_page)
            else:
                for pg in page_nos:
                    print(f'extracted {count+1} no. of pages')
                    extracted_page = input_pdf.getPage(pg)
                    pdf_writer.addPage(extracted_page)
        self.write_pdf(finalpdf_obj=pdf_writer,file_name=str(f.name)+'final'+str(count)+'.pdf')
        count=count+1

    def imgtopdf(self):
        image_list=[]
        for f in self.path_list:
            inputFile = Image.open(str(f))
            ImageB=inputFile.convert('RGB')
            image_list.append(ImageB)
        first_pg=image_list[0]
        image_list.pop(0)
        first_pg.save('image.pdf',save_all=True,append_images=image_list)
        return True
            
        


if __name__ == "__main__":
    """
    p = Path(__file__).parents[0]
    # Use this file loading pdf files
    path_list=list(p.glob('pdf_files/*.pdf'))
    # Use this while loading image files
    path_list=list(p.glob('pdf_files/*.jpg'))
    p= PdfEditor(path_list=path_list)
    p.imgtopdf()
    """


    # Block for extracting pages
    getfile = Path(__file__).parents[0]
    path_list=list(getfile.glob('pdf_files/*.pdf'))
    p= PdfEditor(path_list=path_list)
    range=input('If the pages needed to be extracted from a range please input 1 and enter to confirm else just press enter\n')
    print('\nEnter the pages that needed to be extracted once over type\"stop\"\nFor range input just type first and last page number then then \"stop\"\n')
    try:
        my_list = []
        while True:
            my_list.append(int(input()))     
    # if the input is not-integer, just print the list
    except:
        print(my_list)
        p.extract_page(page_nos=my_list,range=range)

    # Block for extracting page finishes

   
    # p.pdf_merge()

    