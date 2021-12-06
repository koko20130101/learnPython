from django.template import loader  # 导入loader方法
from django.shortcuts import render  # 导入render 方法
# from django.http import HttpResponse

# Create your views here.

# 方式一


# def test_html(request):
#     t = loader.get_template('test.html')
#     html = t.render({'name': 'haha'})
#     return HttpResponse(html)

# 方式二


# def test_html(request):
#     return render(request, 'test.html', {'name': 'koko'})

def test_html(request):
    # a = {
    #     'name': 'koko',
    #     'course': ["Python", "C", "C++", "Java"],
    #     'a': {'name': 'C语言中文网', 'address': 'http://c.biancheng.net/'},
    #     'test_hello': test_hello('haha'),
    #     'class_obj': Website()
    # }
    name = 'koko'
    course = ["Python", "C", "C++", "Java"]
    a = {'name': 'C语言中文网', 'address': 'http://c.biancheng.net/'}
    test_hello = test_hello2()
    class_obj = Website()
    return render(request, 'test.html', locals())


def test_hello2():
    return '欢迎来到C语言中文网'


class Website:
    def Web_name(self):
        return 'Hello，C语言中文网!'
    # Web_name.alters_data = True  # 不让Website()方法被模板调用
