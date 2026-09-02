import logging

from google.auth.exceptions import TransportError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from settings import settings


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_file(
    str(settings.google_credentials_file), scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = settings.google_spreadsheet_id
sheet_id = settings.google_sheet_id
ACTUAL_PRICE = 'Актуальный прайс'
KUSH_PRICE = 'Куш прайс'
ALL_OPERATIONS = 'Все операции'
MINUS_OPERATIONS = 'Минусовые операции'
REPORT_DATA = 'Сводная страница'

service = build('sheets', 'v4', credentials=credentials).spreadsheets()


def _execute(request, operation):
    try:
        return request.execute()
    except (HttpError, TransportError, OSError) as exc:
        logging.exception("Google Sheets operation failed: %s", operation)
        raise RuntimeError(f"Google Sheets operation failed: {operation}") from exc


# Функия которая возвращяет цены металлов
def call_metals_prices(kush=False):
    if kush:
        request = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=KUSH_PRICE)
    else:
        request = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=ACTUAL_PRICE)
    result = _execute(request, "read metal prices")
    return result.get('values', [])[1:-1]


# функция для удаления последней строки в google sheets
def delete_last_row():
    request_body = {
        'requests': [
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': 1,
                        'endIndex': 2
                    }
                }
            }
        ]
    }
    request = service.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=request_body)
    _execute(request, "delete last row")


# Функия для записи плюсовой операции в google sheets
def record_plus_operation(values):
    request_body = {
        'requests': [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': 1,
                        'endIndex': 2
                    }
                }
            }
        ]
    }
    insert_request = service.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=request_body)
    _execute(insert_request, "insert operation row")
    range_ = f"'{ALL_OPERATIONS}'!A2:G2"
    array = {'values': [values]}
    update_request = service.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                             range=range_,
                                             valueInputOption='USER_ENTERED',
                                             body=array)
    _execute(update_request, "write operation")


# Функия для записи минусовой операции в google sheets
def record_minus_operation(values):
    request = service.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                      range=f"'{MINUS_OPERATIONS}'",
                                      valueInputOption='USER_ENTERED',
                                      body={'values': [values]})
    _execute(request, "write negative operation")


# Функия для получения нужной нам информации из google sheets
def get_report(request):
    if 'all_time' in request:
        api_request = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                           range=f"'{REPORT_DATA}'!A2:B20")
        return _execute(api_request, "read all-time report").get('values')
    if 'today' in request:
        api_request = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                           range=f"'{REPORT_DATA}'!D2:E19")
        return _execute(api_request, "read daily report").get('values')
    raise ValueError("Unknown report request")
