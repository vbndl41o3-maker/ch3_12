from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from myapp.models import *
from django.forms.models import model_to_dict
# Create your views here.
def search_list(request):
    if 'cname' in request.GET:
        cname = request.GET['cname']
        print(f'cname: {cname}')
        resultList = students.objects.filter(cname__icontains=cname).order_by('-cid')
    else:
        resultList = students.objects.all().order_by('-cid')
        for student in resultList:
            print(model_to_dict(student))

    #resultList = []  #測試若無資料時，清空列表
    errormessgae=""
    if not resultList:
        errormessgae = "查無資料"

    #return HttpResponse("This is the search student view.")
    return render(request, "search_list.html", locals())

def search_name(request):  
    return render(request, "search_name.html")
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET['site_search']
        site_search = site_search.strip() #去除前後空白
        # print(f"site_search: {site_search}")
        #切割關鍵字，依空白分隔
        keywords = site_search.split() # 依空白分隔關鍵字
        print(f'site_search: {site_search}')
        #by github copilot
        #多關鍵字搜尋，搜尋cname,cbirthday,cemail,cphone,caddr
        from django.db.models import Q
        query = Q()
        resultList = students.objects.all().order_by('cid')
        for keyword in keywords:  # query |= 相似 i = i+ 1
            query &= Q(cname__icontains=keyword) | Q(cbirthday__icontains=keyword) | Q(cemail__icontains=keyword) | Q(cphone__icontains=keyword) | Q(caddr__icontains=keyword)
        resultList = students.objects.filter(query).order_by('cid')

        #測試若無資料時，清空列表
        # resultList = []   
    else:
        resultList = students.objects.all().order_by('cid')
    for student in resultList:
        print(model_to_dict(student))
    # resultList =[] # 測試若無資料時，清空列表
    status = True   
    errormessgae=""
    if not resultList:
        errormessgae = "查無資料"
        status = False
        data_count = 0
    else:
        data_count = resultList.count() # 計算目前資料筆數

    #分頁設定，每頁顯示3筆
    from django.core.paginator import Paginator
    paginator = Paginator(resultList, 3)  # 每頁顯示3筆
    page_number = request.GET.get('page')   #取得目前頁碼
    page_obj = paginator.get_page(page_number)  #取得目前頁面的資料
    #說明:
    
    # page_obj 是一個包含該頁資料的物件
    # page_obj.number 目前頁碼
    # page_obj.paginator.num_pages 總頁數
    # page_obj.paginator.page_range 所有可用的頁碼（從 1 開始）
    # page_obj.previous_page_number 上一頁的頁碼
    # page_obj.next_page_number 下一頁的頁碼

    # page_obj.has_next 是否有下一頁
    # page_obj.has_previous 是否有上一頁
    # page_obj.object_list 該頁的資料

    # return HttpResponse("This is the index view.")
    return render(request, "index.html", locals())

def post(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f'cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}')
        # 儲存資料到資料庫
        student = students(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )
        student.save()
        return redirect('index')
    else:
        return render(request, "post.html")

def edit(request, id):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f'id: {id}')
        print(f'cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}')
        #更新指定ID的學生資料
        students.objects.filter(cid=id).update(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )
        #return HttpResponse("This is a POST request for edit student.")
        return redirect('index')
    else:
        print(f"id: {id}")
        #舉得指定ID的學生資料
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        #return HttpResponse("This is the edit view for student with id: {id}")
        return render(request, "edit.html", locals())

def delete(request, id):
    if request.method == 'POST':
        print(f'id: {id}')
        students.objects.filter(cid=id).delete()#刪除指定ID的學生資料

        #return HttpResponse("This is a POST request for delete student.")
        return redirect('index') #刪除完成後導向首頁
    else:
        print(f'id: {id}')
        #取得指定ID的學生資料
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        return render(request, "delete.html", locals())