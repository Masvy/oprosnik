import io
import openpyxl


async def generate_excel_file(user_ids, first_names, user_names):
    # Создаем новую книгу Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Users"

    # Заголовки столбцов
    sheet['A1'] = "User ID"
    sheet['B1'] = 'First Name'
    sheet['C1'] = "Username"

    # Заполняем данными
    for user_id, first_name, user_name in zip(user_ids, first_names, user_names):
        sheet.append([str(user_id), first_name, user_name])

    # Создаем бинарный поток для записи в файл
    excel_buffer = io.BytesIO()
    workbook.save(excel_buffer)
    excel_buffer.seek(0)

    return excel_buffer
