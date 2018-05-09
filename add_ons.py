import json
from datetime import datetime, time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


class DateTimeEncoder(json.JSONEncoder):
    # default JSONEncoder cannot serialize datetime.datetime objects
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = obj.strftime('%s')
        else:
            encoded_object = super(self, obj)
        return encoded_object


class JsonResponse(HttpResponse):
    def __init__(self, content, status=None, content_type='application/json'):
        data = dict()
        data['data'] = content
        data['status_code'] = status
        json_text = json.dumps(data, default=json_serial)
        super(JsonResponse, self).__init__(
            content=json_text,
            status=status,
            content_type=content_type)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    elif isinstance(obj, time):
        serial = obj.isoformat()
        return serial
    else:
        return "Non-Serializable Data"
    #raise TypeError ("Type not serializable")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validate_mobile(mobile):
    if len(mobile) >= 10:
        return True
    else:
        return False


def paginate_data(searched_data, request_data):
    if int(request_data.data['paginator']) > 0:
        paginator = Paginator(searched_data.data, request_data.data['paginator'])
        try:
            curr = paginator.page(request_data.data['page'])
        except PageNotAnInteger:
            curr = paginator.page(1)
        except EmptyPage:
            curr = paginator.page(paginator.num_pages)

        data = {'total_pages': paginator.num_pages, 'current': curr.number,
                'total_objects': len(searched_data.data)}
        if curr.has_next():
            data['next'] = curr.next_page_number()
        else:
            data['next'] = -1

        if curr.number > 1:
            data['previous'] = curr.previous_page_number()
        else:
            data['previous'] = -1
        data['objects'] = curr.object_list
    else:
        data = {'objects': searched_data.data, 'previous': -1, 'next': -1, 'total_pages': 1, 'current': 1,
                'total_objects': len(searched_data.data)}
    return data


