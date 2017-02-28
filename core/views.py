import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import AccessToken
from .utils import split_sentences


@csrf_exempt
def sentence_split(request):
    if request.method != 'POST':
        response_body = {"error": "POST method expected"}
        status = 400
    elif request.content_type != 'application/json':
        response_body = {"error": "application/json content type expected"}
        status = 400
    else:
        token = request.META.get('HTTP_X_ACCESS_TOKEN')
        if not token:
            response_body = {"error": "x-access-token header expected"}
            status = 400
        elif not AccessToken.objects.filter(value=token):
            response_body = {"error": "access denied (invalid token)"}
            status = 403
        else:
            try:
                request_body = json.loads(request.body)
            except ValueError:
                response_body = {"error": "JSON body expected"}
                status = 400
            else:
                if 'text' not in request_body:
                    response_body = {"error": "'text' key in body expected"}
                    status = 400
                else:
                    response_body = split_sentences(request_body['text'])
                    status = 200
    return JsonResponse(response_body, status=status, safe=False)
