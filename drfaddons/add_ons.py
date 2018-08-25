import json
from django.http import HttpResponse


class DateTimeEncoder(json.JSONEncoder):
    """Date Time Encoder for JSON. I do not use this anymore
    Can't identify original source.
    Sources: [https://gist.github.com/dannvix/29f53570dfde13f29c35,
    https://www.snip2code.com/Snippet/106599/Custom-Django-JsonResponse-which-support]
    """
    def default(self, obj):
        from datetime import datetime

        if isinstance(obj, datetime):
            encoded_object = obj.strftime('%s')
        else:
            encoded_object = super(self, obj)
        return encoded_object


class JsonResponse(HttpResponse):
    """
    A HttpResponse that responses in JSON. Used in APIs.
    Can't identify original source.
    Sources: [https://gist.github.com/dannvix/29f53570dfde13f29c35,
    https://www.snip2code.com/Snippet/106599/Custom-Django-JsonResponse-which-support]
    """
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
    """
    JSON serializer for objects not serializable by default json code
    Sources: [https://stackoverflow.com/a/22238613,
    https://stackoverflow.com/a/41200652,
    https://github.com/chartmogul/chartmogul-python/blob/master/chartmogul/resource.py]
    """
    from datetime import datetime, time

    if isinstance(obj, (datetime, time)):
        serial = obj.isoformat()
        return serial
    else:
        return "Non-Serializable Data"
    # raise TypeError ("Type not serializable")


def get_client_ip(request):
    """
    Fetches the IP address of a client from Request and return in proper format.
    Source: https://stackoverflow.com/a/4581997
    Parameters
    ----------
    request: django.http.HttpRequest

    Returns
    -------
    ip: str
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_email(email):
    """
    Validates an email address
    Source: Himanshu Shankar (https://github.com/iamhssingh)
    Parameters
    ----------
    email: str

    Returns
    -------
    bool
    """
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validate_mobile(mobile):
    """
    Validates a mobile number
    Source: Himanshu Shankar (https://github.com/iamhssingh)
    Parameters
    ----------
    mobile: str

    Returns
    -------
    bool
    """
    if len(mobile) >= 10:
        return True
    else:
        return False


def paginate_data(searched_data, request_data):
    """
    Paginates the searched_data as per the request_data
    Source: Himanshu Shankar (https://github.com/iamhssingh)
    Parameters
    ----------
    searched_data: Serializer.data
                    It is the data received from queryset. It uses show_serializer
    request_data: Serializer.data
                    It is the request data. It uses serializer_class.

    Returns
    -------
    data: dict
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


def send_message(message: str, subject: str, recip: list, recip_email: list):
    """
    Sends message to specified value.
    Source: Himanshu Shankar (https://github.com/iamhssingh)
    Parameters
    ----------
    message: str
        Message that is to be sent to user.
    subject: str
        Subject that is to be sent to user, in case prop is an email.
    recip: list
        Recipient to whom message is being sent.
    recip_email: list
        Recipient to whom EMail is being sent. This will be deprecated once SMS feature is brought in.

    Returns
    -------
    sent: dict
    """
    from django.conf import settings
    from django.core.mail import send_mail

    import smtplib

    import re

    from hspsms import HSPConnector

    sent = {'success': False, 'message': None}

    if not getattr(settings, 'EMAIL_HOST', None):
        raise ValueError('EMAIL_HOST must be defined in django setting for sending mail.')
    if not getattr(settings, 'EMAIL_FROM', None):
        raise ValueError('EMAIL_FROM must be defined in django setting for sending mail. Who is sending email?')

    # For sms.hspsms.com
    hspsms = getattr(settings, 'HSPSMS', None)

    if isinstance(recip, str):
        # For backsupport
        recip = [recip]
    if isinstance(recip_email, str):
        # For backsupport
        recip_email = [recip_email]

    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", recip[0]):
        try:
            send_mail(subject=subject,
                      message=message,
                      from_email=settings.EMAIL_FROM, recipient_list=[recip])
            sent['message'] = 'Message sent successfully!'
            sent['success'] = True
        except smtplib.SMTPException as ex:
            sent['message'] = 'Message sending failed!' + str(ex.args)
            sent['success'] = False

    else:
        if hspsms:
            hspsms = HSPConnector(username=hspsms['USER'], apikey=hspsms['APIKEY'], sender=hspsms.get('SENDER', None),
                                  smstype=getattr(hspsms, 'SMSTYPE', 'TRANS'))
            try:
                hspsms.send_sms(recip, message)
                sent['message'] = 'Message sent successfully!'
                sent['success'] = True
            except Exception as ex:
                sent['message'] = 'Message sending Failed!' + str(ex.args)
                sent['success'] = False

        if not sent['success']:
            try:
                send_mail(subject=subject,
                          message=message,
                          from_email=settings.EMAIL_FROM, recipient_list=[recip_email])
                sent['message'] = 'Message sent successfully!'
                sent['success'] = True
            except smtplib.SMTPException as ex:
                sent['message'] = 'Message sending Failed!' + str(ex.args)
                sent['success'] = False

    return sent
