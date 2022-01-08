# from os import path
from pathlib import Path
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
# from kivy.utils import platform
from pathlib import Path

class PdfEditor:
	def __init__(self, path_list="") -> None:
		if len(path_list) == 0:
			print("Sorry files do not exist please try again")
			return None
		else:
			print("loading files")
			# print(path_list)
			for f in path_list:
				# print(type(f))
				if f.exists() and f.glob("*.pdf"):
					print(".")
					self.FileType = "pdf"
				elif f.exists() and (
					f.glob("*.jpg") or f.glob("*.png") or f.glob("*.jpeg")
				):
					print("*")
					self.FileType = "pic"
				else:
					print("Invalid file type supplied")
					return 0
		self.path_list = path_list
		print(str(self.path_list))
		print("Files loaded successfully")

	def write_pdf(self, finalpdf_obj, file_name=Path(Path.home(),"sample.pdf")):
		with file_name.open(mode="wb") as output_file:
			finalpdf_obj.write(output_file)
	def write_txt(self,file_content="", file_name=Path(Path.home(),"sample.txt")):
		with file_name.open(mode="a+") as output_file:
			output_file.write(file_content)

	def pdf_merge(self, savepath=""):

		pdf_merger = PdfFileMerger()
		for f in self.path_list:
			pdf_merger.append(str(f))
		final_path = Path(savepath, "merged.pdf")
		self.write_pdf(finalpdf_obj=pdf_merger, file_name=final_path)
		print("Pdfs merged succesfully")
		print(final_path)
		return True


	def extract_page(self, page_nos=[1], pg_range=1, savepath="",save=True):
		pdf_writer = PdfFileWriter()
		count = 0
		for f in self.path_list:
			input_pdf = PdfFileReader(str(f))
			if pg_range:
				print("page 0 and page 1 are", page_nos[0], page_nos[1])
				extracted_page = input_pdf.pages[page_nos[0] : page_nos[1]]
				for xtract in extracted_page:
					pdf_writer.addPage(xtract)
			else:
				for pg in page_nos:
					print(f"extracted {count+1} no. of pages")
					extracted_page = input_pdf.getPage(pg)
					pdf_writer.addPage(extracted_page)
		if save:
			final_path = Path(savepath, f"{str(count)}_{str(f.name)}")
			self.write_pdf(finalpdf_obj=pdf_writer, file_name=final_path)
			print(final_path)
			count = count + 1
		else:
			return pdf_writer

	def imgtopdf(self, savepath=""):
		image_list = []
		for f in self.path_list:
			inputFile = Image.open(str(f))
			ImageB = inputFile.convert("RGB")
			image_list.append(ImageB)
		first_pg = image_list[0]
		image_list.pop(0)
		final_path = Path(savepath, "converted_image.pdf")
		first_pg.save(str(final_path), save_all=True, append_images=image_list)
		print(final_path)
		return True

	def extract_text(self, page_nos=[1], pg_range=1, savepath=""):

		writer = self.extract_page(
			page_nos=page_nos, pg_range=pg_range, savepath="", save=False
		)
		total_pages=writer.getNumPages()
		final_path = Path(savepath, "extracted.txt")
		for pg in range(total_pages):
			pageObj=writer.getPage(pg)
			self.write_txt(file_content=pageObj.extractText(), file_name=final_path)
			# file_content=file_content+pageObj.extractText()
			# print(type(pageObj.extractText()))
			
		# self.write_txt(file_content=file_content, file_name=final_path)
		print('Feature not fully implemented')
	def make_searchable_pdf(self,pdf_pg=""):
		print("make_searchable_pdf function called")

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
	# path_list = list(getfile.glob("pdf_files/*.pdf"))
	path_list = list(getfile.glob("*.pdf"))
	print(path_list)
	p = PdfEditor(path_list=path_list)

	"""
	# extract page
		range = input(
			"If the pages needed to be extracted from a range please input 1 and enter to confirm else just press enter\n"
		)
		print(
			'\nEnter the pages that needed to be extracted once over type"stop"\nFor range input just type first and last page number then then "stop"\n'
		)
		try:
			my_list = []
			while True:
				my_list.append(int(input()))
		# if the input is not-integer, just print the list
		except:
			print(my_list)
			p.extract_page(page_nos=my_list, range=range)
			# Block for extracting page finishes
	"""

	
	"""Merge PDF
	p.pdf_merge()
	"""

	pg_range = input(
			"If the pages needed to be extracted from a range please input 1 and enter to confirm else just press enter\n"
		)
	print(
		'\nEnter the pages that needed to be extracted once over type"stop"\nFor range input just type first and last page number then then "stop"\n'
	)
	try:
		my_list = []
		while True:
			my_list.append(int(input()))
	# if the input is not-integer, just print the list
	except Exception as e:
		print(e)
		print(my_list)
		p.extract_text(page_nos=my_list, pg_range=pg_range)