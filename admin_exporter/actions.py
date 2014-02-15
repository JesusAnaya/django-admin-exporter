from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
from .utils import json_to_csv, filter_duplicate_params
import json


def serialize_queryset(queryset, values, format):
    data = serializers.serialize(format, queryset, fields=values)
    return data


def export(modeladmin, request, queryset, format):
    selected_action = request.POST.getlist('_selected_action')
    select_across = request.POST.get('select_across')
    action = filter_duplicate_params(request.POST.getlist('action'))
    export_data = request.POST.get('export_data')

    if export_data:
    	model_name = modeladmin.model.__name__
    	fieldnames = export_data.split(',')

        if format == "csv":
            data = serialize_queryset(queryset, fieldnames, "json")
            data = json.loads(data)

            dataFlattened = []
            for item in data:
            	print item["fields"]
                flattednedItem = item["fields"]
                dataFlattened.append(flattednedItem)
            data = json.dumps(dataFlattened)
            data = json_to_csv(data, fieldnames)
        else:
            data = serialize_queryset(queryset, fieldnames, format)

        now = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        response = HttpResponse(data, mimetype="application/x-download")
        content = "attachment;filename={filename}-{now}.{extention}".format(
                                                extention=format.lower(),
                                                filename=model_name.lower(),
                                                now=now)
        response["Content-Disposition"] = content
        return response

    else:
    	fields = modeladmin.model._meta.fields

        return render(request, "export_parameters.html", {
            'action': action,
            'fields': fields,
            'selected_actions': selected_action,
            'select_across': select_across,
        })

def export_as_csv_action(modeladmin, request, queryset):
    return export(modeladmin, request, queryset, format="csv")
export_as_csv_action.short_description = "Export selected items to CSV"

def export_as_json_action(modeladmin, request, queryset):
    return export(modeladmin, request, queryset, format="json")
export_as_json_action.short_description = "Export selected items to JSON"

def export_as_xml_action(modeladmin, request, queryset):
    return export(modeladmin, request, queryset, format="xml")
export_as_xml_action.short_description = "Export selected items to XML"

def export_as_yaml_action(modeladmin, request, queryset):
    return export(modeladmin, request, queryset, format="yaml")
export_as_yaml_action.short_description = "Export selected items to YAML"
