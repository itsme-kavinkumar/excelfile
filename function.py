from src.endpoints.exportexcel import CreateExcel,generate_filename
import http.server
import socketserver
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from tempfile import NamedTemporaryFile
import shutil
import webbrowser
app = FastAPI()
# file=CreateExcel()

from spire.xls import *
from spire.xls.common import *
from openpyxl import load_workbook
import traceback
import re
from win32com import client 
import os
import re
import win32com.client as client
from concurrent.futures import ThreadPoolExecutor
import time


import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = os.path.abspath('.')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    webbrowser.open(f"http://localhost:{PORT}")
    httpd.serve_forever()


def ExcelToPdf():
    try:
        start_time=time.time()
        excel = client.Dispatch("Excel.Application")
        excel.DisplayAlerts = False
        workbook_path = os.path.join(os.getcwd(), 'excel_files', 'test_excel_to_pdf.xlsx')
        sheets = excel.Workbooks.Open(workbook_path)
        work_sheets = sheets.Worksheets[0]

        work_sheets.PageSetup.Orientation = 2
        work_sheets.Cells.Font.Size = 8
        margin_left, margin_right, margin_top, margin_bottom = 0.3, 0, 0.3, 0

        work_sheets.PageSetup.LeftMargin = excel.Application.InchesToPoints(margin_left)
        work_sheets.PageSetup.RightMargin = excel.Application.InchesToPoints(margin_right)
        work_sheets.PageSetup.TopMargin = excel.Application.InchesToPoints(margin_top)
        work_sheets.PageSetup.BottomMargin = excel.Application.InchesToPoints(margin_bottom)
                 
        page_width = 11.69  
        column_count = work_sheets.UsedRange.Columns.Count
        column_width_in_points = excel.Application.InchesToPoints((page_width - 2 * (margin_left + margin_right)) / column_count)
        for col in range(1, column_count + 1):
            work_sheets.Columns(col).ColumnWidth = column_width_in_points / 7  # Approximate conversion factor

        [setattr(shape, 'Width', 40) or setattr(shape, 'Height', 17) or setattr(shape, 'Top', 20 ) for shape in work_sheets.Shapes]
            # shape.Width=cell_range.Width/2
            # shape.Height=cell_range.Height/2
        used_range_rows=work_sheets.UsedRange.Rows.Count
        used_range_columns=work_sheets.UsedRange.Columns.Count

        merged_range={  work_sheets.Cells(row, col).MergeArea.Address.replace('$', '')
                        for col in range(1, used_range_columns + 1)
                        for row in range(1, used_range_rows + 1)
                        if work_sheets.Cells(row, col).MergeCells }

        
        for row in range(1, used_range_rows + 1):
            merged = False
            for mergedrange in merged_range:
                if row >= work_sheets.Range(mergedrange).Row and row <= work_sheets.Range(mergedrange).Row + work_sheets.Range(mergedrange).Rows.Count - 1:
                    merged = True
                    break
            if not merged:
                work_sheets.Rows(row).AutoFit()

        work_sheets.Cells.WrapText = True
        pdf_path = os.path.join(os.getcwd(), "pdf_files", generate_filename('excel-to-pdf', 'pdf'))
        work_sheets.ExportAsFixedFormat(0, pdf_path)
        sheets.Close(SaveChanges=False)
        excel.Quit()
        end_time=time.time()
        print(f"----used time {end_time-start_time}")
    except Exception as e:
        print('---------', str(e), traceback.extract_tb(e.__traceback__))

ExcelToPdf()
# try:

#     with ThreadPoolExecutor() as executor:
#         thread=executor.submit(ExcelToPdf)

#         thread.result()
# except Exception as e:
#     print('---------', str(e), traceback.extract_tb(e.__traceback__))

# def ExcelToPdf():
#     try:
#         excel = client.Dispatch("Excel.Application")
#         excel.DisplayAlerts = False
#         workbook_path = os.path.join(os.getcwd(), 'excel_files', 'test_excel_to_pdf.xlsx')
#         sheets = excel.Workbooks.Open(workbook_path)
#         work_sheets = sheets.Worksheets[0]

#         work_sheets.PageSetup.Orientation = 2
#         work_sheets.Cells.Font.Size = 8

#         margin_left = 0.3
#         margin_right = 0
#         margin_top = 0
#         margin_bottom = 0
#         work_sheets.PageSetup.LeftMargin = excel.Application.InchesToPoints(margin_left)
#         work_sheets.PageSetup.RightMargin = excel.Application.InchesToPoints(margin_right)
#         work_sheets.PageSetup.TopMargin = excel.Application.InchesToPoints(margin_top)
#         work_sheets.PageSetup.BottomMargin = excel.Application.InchesToPoints(margin_bottom)
    
#         merged_range = []
#         for row in range(1, work_sheets.UsedRange.Rows.Count + 1):
#             for col in range(1, work_sheets.UsedRange.Columns.Count + 1):
#                 cell = work_sheets.Cells(row, col)
#                 if cell.MergeCells:
#                     merged_area = cell.MergeArea
#                     if merged_area.Address not in merged_range:
#                         merged_range.append(merged_area.Address)
#                         rows = merged_area.Rows.Count
#                         columns = merged_area.Columns.Count

#         page_width = 11.69  
#         column_count = work_sheets.UsedRange.Columns.Count
#         usable_width = page_width - 2 * (margin_left + margin_right)  
#         column_width_in_inches = usable_width / column_count
#         column_width_in_points = excel.Application.InchesToPoints(column_width_in_inches)

#         for col in range(1, column_count + 1):
#             work_sheets.Columns(col).ColumnWidth = column_width_in_points / 7  # Approximate conversion factor

#         for area in merged_range:
#             area = re.sub(r'[$]', '', area)
#             cell_range = work_sheets.Range(area)
#             for shape in work_sheets.Shapes:
#                 top_left_cell = shape.TopLeftCell
#                 bottom_right_cell = shape.BottomRightCell
#                 # if top_left_cell.Row >= cell_range.Row and bottom_right_cell.Row <= cell_range.Row + cell_range.Rows.Count - 1 and \
#                 #         top_left_cell.Column >= cell_range.Column and bottom_right_cell.Column <= cell_range.Column + cell_range.Columns.Count - 1:
#                 shape.Width = 40
#                 shape.Height = 17
#                 shape.Top=20
#                 # shape.Width=cell_range.Width/2
#                 # shape.Height=cell_range.Height/2

#         for row in range(1, work_sheets.UsedRange.Rows.Count + 1):
#             merged = False
#             for area in merged_range:
#                 merged_cell = re.sub(r'[$]', '', area)
#                 if row >= work_sheets.Range(merged_cell).Row and row <= work_sheets.Range(merged_cell).Row + work_sheets.Range(merged_cell).Rows.Count - 1:
#                     merged = True
#                     continue
#             if not merged:
#                 work_sheets.Rows(row).AutoFit()

#         work_sheets.Cells.WrapText = True
#         pdf_path = os.path.join(os.getcwd(), "pdf_files", generate_filename('excel-to-pdf', 'pdf'))
#         work_sheets.ExportAsFixedFormat(0, pdf_path)
#         sheets.Close(SaveChanges=False)
#         excel.Quit()

#     except Exception as e:
#         print('---------', str(e), traceback.extract_tb(e.__traceback__))
# ExcelToPdf()