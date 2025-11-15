import openpyxl

class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self, sheet_name):
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook[sheet_name]
        data = []

        headers = [cell.value for cell in sheet[1]]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if all(v is None for v in row):
                continue
            row_data = {headers[i]: row[i] for i in range(len(headers))}
            data.append(row_data)
        return data
