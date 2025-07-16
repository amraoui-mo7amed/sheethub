from .generic import *
from django.http import JsonResponse

def getCommunes(request, province_id, lang_code):
    algeria = loadJSON('algeria.json')
    filtered = [entry for entry in algeria if entry['wilaya_code'] == f"{int(province_id):02}"]

    # Select field names depending on the lang
    if lang_code.lower() == 'ar':
        communes = [
            {
                "id": entry["id"],
                "commune_name": entry["commune_name"],
                "wilaya_name": entry["wilaya_name"]
            }
            for entry in filtered
        ]
    else:  # 'fr', 'en', or default
        communes = [
            {
                "id": entry["id"],
                "commune_name": entry["commune_name_ascii"],
                "wilaya_name": entry["wilaya_name_ascii"]
            }
            for entry in filtered
        ]

    return JsonResponse(communes, safe=False)
