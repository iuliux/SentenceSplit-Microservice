import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import split_sentences

@csrf_exempt
def sentence_split(request):
    if request.method != 'POST':
        response_body = {"error": "POST method expected"}
    else:
        try:
            request_body = json.loads(request.body)
        except ValueError:
            response_body = {"error": "JSON body expected"}
        else:
            if 'text' not in request_body:
                response_body = {"error": "'text' key expected"}
            else:
                response_body = split_sentences(request_body['text'])
    return JsonResponse(response_body, safe=False)
