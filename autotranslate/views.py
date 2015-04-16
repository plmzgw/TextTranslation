#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import xlrd, xlwt

from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse

from forms import UploadFileForm
from models import UploadFile, TranslatedFile, Language
from translate_api.GoogleTranslateApi import Google_Translate
from translate_api.setting import api_key

reload(sys)
sys.setdefaultencoding('utf-8')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('myfile')
            for f in files:
                fname= f.name
                instance=UploadFile(filename = fname, file = f)
                instance.save()
                
            return HttpResponseRedirect(reverse('autotranslate.views.upload_file'))
        
    else:
        form = UploadFileForm()
    fileslist = UploadFile.objects.order_by("-upload_time")
    trans_fileslist = TranslatedFile.objects.order_by("-trans_time")
    languages = Language.objects.all()
    
    return render_to_response('fileslist.html', locals(), context_instance=RequestContext(request))

def delete_upfile(request, id=""):
    fid=id
    if fid == "":
        raise Http404
    try:
        document = UploadFile.objects.get(id=fid)
    except Exception:
        raise Http404
    if document:
        file_directory = os.path.join(settings.MEDIA_ROOT, str(document.file.name))
        if os.path.isfile(file_directory):
            os.remove(file_directory)
        document.delete()
        return HttpResponseRedirect(reverse('autotranslate.views.upload_file'))
    fileslist = UploadFile.objects.order_by("-upload_time")
    trans_fileslist = TranslatedFile.objects.order_by("-trans_time")
    languages = Language.objects.all()
    return render_to_response('filelist.html', locals())

def delete_transfile(request, id=""):
    fid=id
    if fid=="":
        raise Http404
    try:
        document = TranslatedFile.objects.get(id=fid)
    except Exception:
        raise Http404
    if document:
        if os.path.isfile(document.path):
            os.remove(document.path)
        document.delete()
        return HttpResponseRedirect(reverse('autotranslate.views.upload_file'))
    fileslist = UploadFile.objects.order_by("-upload_time")
    trans_fileslist = TranslatedFile.objects.order_by("-trans_time")
    languages = Language.objects.all()
    return render_to_response('filelist.html', locals())

def resolve_file(request, id=""):
    fileId=id
    if fileId=="":
        raise Http404
    title_list=[]
    fileslist = UploadFile.objects.order_by("-upload_time")
    trans_fileslist = TranslatedFile.objects.order_by("-trans_time")
    languages = Language.objects.all()
    try:
        document = UploadFile.objects.get(id=fileId)
    except Exception:
        raise Http404
    if document:
        fname_byid= document.filename
        fname_suffix = fname_byid[fname_byid.rfind('.'):]
        file_directory = os.path.join(settings.MEDIA_ROOT, str(document.file.name)).replace("\\", "/")
        if os.path.isfile(file_directory):
            if fname_suffix == '.csv':
                f_type = 1
                ff = open(file_directory,"rb")
                title = (ff.next()).replace("\n","")
                ff.close()
                title_list=[]
                if '\t' in title:
                    separate_type = 1
                    title_list = title.split("\t")
                else:
                    separate_type = 2
                    reader = csv.reader(open(file_directory,"rb"))
                    for line in reader:
                        title_list = line
                        break
            else:
                f_type = 2
                book = xlrd.open_workbook(file_directory)
                sheet = book.sheets()[0]
                title_list = sheet.row_values(0)
                
    return render_to_response('fileslist.html', locals(), context_instance=RequestContext(request))
        
def translate_file(request):
    if request.method != "GET":
        return HttpResponse("error")
    api = Google_Translate()
    source_lang = request.GET.get('source_lang','')
    target_lang = request.GET.get('target_lang','')
    trans_langobj = Language.objects.get(language_code=target_lang)
    trans_lang_cn = trans_langobj.language_chinese
    trans_lang_en = trans_langobj.language
    file_id = request.GET.get('fileId')
    columns = request.GET.getlist('column')
    filetype = int(request.GET.get('file_type'))
    if filetype ==1:
        separate_type = int(request.GET.get('sep_type'))
    length=len(columns)
    document = UploadFile.objects.get(id=file_id)
    file_directory = os.path.join(settings.MEDIA_ROOT, str(document.file.name)).replace("\\", "/")  #上传文件存放路径
    down_directory = os.path.join(settings.MEDIA_ROOT,"downloadfiles/").replace("\\", "/")  #翻译后的文件存放路径
    trans_filename = trans_lang_en+"_"+document.filename   #翻译后文件名
    trans_file = down_directory+trans_filename
#     if len(TranslatedFile.objects.filter(filename = trans_filename))>0:
#         return HttpResponse("该文件已经翻译，请查看已翻译文件列表！")
    if os.path.isfile(file_directory):
        if filetype == 1:
            f=file(trans_file,'wb')
            writer=csv.writer(f)
            if separate_type == 1:
                ff = open(file_directory,"rb")
                file_title = ff.next()
                titleList = (file_title.replace("\n", "")).split("\t")
                writer.writerow(titleList)
                for line in ff:
                    line = line.replace("\n", "")
                    line_list = line.split("\t")
                    for i in columns:
                        i = int(i)
                        text = line_list[i]
                        api.setParams(api_key, source_lang, target_lang, text)
                        result = api.translate()
                        if result == 'timeout':
                            return HttpResponse('请求超时，请再尝试一次！')
                        else:
                            line_list[i] = result
#                         line_list[i] = "result"+str(i)
                    writer.writerow(line_list)
                ff.close()
            elif separate_type == 2:
                reader = csv.reader(open(file_directory,"rb"))
                count=0
                for line in reader:
                    count+=1
                    if count ==1:
                        writer.writerow(line)
                    else:
                        for i in columns:
                            i = int(i)
                            text = line[i]
                            api.setParams(api_key, source_lang, target_lang, text)
                            result = api.translate()
                            if result == 'timeout':
                                return HttpResponse('请求超时，请再尝试一次！')
                            else:
                                line[i] = result
#                             line[i] = "result"+str(i)
                        writer.writerow(line)
            else:
                return HttpResponse("文件分隔符不支持，请联系开发人员！")
            f.close()
        else:
            bookr = xlrd.open_workbook(file_directory)
            sheet = bookr.sheets()[0]
            nrows = sheet.nrows
            ncols = sheet.ncols
            bookw = xlwt.Workbook(encoding='utf-8')
            sheet1 = bookw.add_sheet('Sheet1')
            row0_value = sheet.row_values(0)
            row0 = sheet1.row(0)
            
            for i in xrange(ncols):
                row0.write(i, row0_value[i])
            for i in xrange(1,nrows):
                value = sheet.row_values(i)
                row = sheet1.row(i)
                for j in columns:
                    j = int(j)
                    text = value[j]
                    api.setParams(api_key, source_lang, target_lang, text)
                    result = api.translate()
                    if result == 'timeout':
                        return HttpResponse('请求超时，请再尝试一次！')
                    else:
                        value[j] = result
#                     value[j] = "result"+str(j)
                for k in xrange(ncols):
                    row.write(k, value[k])
            bookw.save(trans_file)
        
        instance = TranslatedFile(filename = trans_filename, trans_lang = trans_lang_cn, path = trans_file)
        instance.save()
        return HttpResponseRedirect(reverse('autotranslate.views.upload_file'),'1')
    
    fileslist = UploadFile.objects.order_by("-upload_time")
    languages = Language.objects.all()
    trans_fileslist = TranslatedFile.objects.order_by("-trans_time")
    trans_state = "已完成！"
    return render_to_response('fileslist.html', locals(), context_instance=RequestContext(request))
     
      
def down_file(request, id=""):
    down_fileid = id
    down_file = TranslatedFile.objects.get(id = down_fileid)
    downfile_name = down_file.filename
    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
    
    response = HttpResponse(readFile(down_file.path), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + downfile_name
    
    return response

def test(request):
    return render_to_response('test.html', locals())
          
