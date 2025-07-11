from .generic import *


def getCommunes(request, province_id):
    algeria = loadJSON('algeria.json')
    print(province_id)
    if province_id:
        communes = [entry for entry in algeria if entry['wilaya_code'] == f"{int(province_id):02}"]
    else:
        communes = []
    return JsonResponse(communes, safe=False)