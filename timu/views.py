from django.shortcuts import render,HttpResponse
from django.http import JsonResponse, response
from timu import models
import uuid
import timu
import pandas as ps


# Create your views here.
"""
------添加题目------
api : http://127.0.0.1:8081/timu/addtimu/
method: post
数据: form-data
    timufile: Subject.csv

返回内容:
{
    'is_add':'no',
    'wrongRow':[],
    'add_num':0,
}
"""
def add_timu(request):
    if request.method == 'POST':
        response_data={
            'is_add':'no',
            'wrongRow':[],
            'add_num':0,
        }

        #获取文件
        Subject = request.FILES.get('Subject')
        # 保存文件
        with open('Subject.xlsx','wb') as f:
            for chunk in Subject.chunks():
                f.write(chunk)

        #读取csv文件
        rowList = []
        # with open('Subject.csv', 'r',encoding='gbk') as f:
        #         rowList = csv.reader(f)
        #         rowList = list(rowList)
        df = ps.read_excel('Subject.xlsx',header=None)

        rowList=df.values

        # print(rowList)
        # for row in rowList:
        #     print(row)

        row0 = rowList[0]
        print(row0)
        columlist = ['案例标题','Subject','rightAnswer1','wrongAnswer1','wrongAnswer2','wrongAnswer3']

        if all(row0 == columlist):
            #进行文件检测
            for index in range(1,len(rowList)):
                eachrow = rowList[index]
                if '(   )' not in eachrow[1]: #看有么有空列和(   )是不是再题干中
                    response_data['wrongRow'].append(str(index)) # 添加错误行
            
            if response_data['wrongRow']: #若不空说明文件有错
                return JsonResponse(response_data)
            else:
                # 没错的录入文件
                for index in range(1,len(rowList)):
                    eachrow = rowList[index]
                    if not models.Table.objects.filter(
                        anliuuid = uuid.uuid3(uuid.NAMESPACE_DNS, eachrow[0].strip()), 
                        Subject = eachrow[1].strip()).exists(): #题目不存在才加入
                        models.Table.objects.create(
                            anliuuid = str( uuid.uuid3(uuid.NAMESPACE_DNS, eachrow[0].strip()) ),
                            Subject = str(eachrow[1]).strip(),
                            rightAnswer = str(eachrow[2]).strip(),
                            wrongAnswer1 = str(eachrow[3]).strip(),
                            wrongAnswer2 = str(eachrow[4]).strip(),
                            wrongAnswer3 = str(eachrow[5]).strip(),
                            )
                        response_data['add_num'] += 1
                response_data['is_add'] = 'yes'
                return JsonResponse(response_data)
        else:
            response_data['wrongRow'].append('0') # 0行错误
            return JsonResponse(response_data)
    else:
        return HttpResponse('Bad request',status = 500)
"""
------获取题目------
api : http://127.0.0.1:8081/timu/gettimu/<str:timuuuid>
method: get
数据: 参数 url中得timuuuid

返回内容:

"""
def get_timu(request,timuuuid):
    if request.method == 'GET':
        response_data = {
            'is_get':'no',
            'timudict':{},
            'uuid_is_wrong':'no',
        }
        if timuuuid and models.Table.objects.filter(anliuuid = timuuuid).exists():
            timulist = models.Table.objects.filter(anliuuid = timuuuid).values(
                'Subject',
                'rightAnswer',
                'wrongAnswer1',
                'wrongAnswer2',
                'wrongAnswer3'
            )
            timulist = list(timulist)

            for index,timu in enumerate(timulist):
                response_data['timudict'][str(index)] = timu
            
            response_data['is_get'] = 'yes'
            return JsonResponse(response_data)
        else:
            response_data['uuid_is_wrong'] = 'yes'
            return JsonResponse(response_data)
    else:
        return HttpResponse("Bad request",status = 500)