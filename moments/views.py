from collections import Counter

from django.conf import settings
# from django.conf.global_settings import STATIC_URL

from blueapps.patch.settings_open_saas import SITE_URL,STATIC_URL
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from moments.models import Status, WeChatUser, Reply
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from blueking.component.shortcuts import get_client_by_request
# Create your views here.
from moments.models import Status


def home(request):
    return render(request, 'homepage.html')


@login_required
def show_user(request):
    user = WeChatUser.objects.get(user=request.user)
    # po = {
    #     'name':'xiaoming',
    #     'region':"xi'an'",
    #     'motto':"i love xi'an",
    #     'pic':'Po2.jpg',
    #     'email':"ppp@xx.com"
    # }
    return render(request, 'user.html', {'user': user})


@login_required
def show_status(request):
    keyword = request.GET.get("keyword", "")
    page = request.GET.get("page", "1")

    if not keyword:
        statuses = Status.objects.all()
    else:
        statuses = Status.objects.filter(Q(text__contains=keyword) | Q(user__user__username__contains=keyword))

    p = Paginator(statuses, 5)
    statuses = p.get_page(page)

    for status in statuses:
        status.likes = Reply.objects.filter(status=status, type="0")
        status.comments = Reply.objects.filter(status=status, type="1")
    return render(request, "status.html", {"statuses": statuses,
                                           "user": request.user.username,
                                           "keyword": keyword,
                                           "page_range": p.page_range,
                                           "page": int(page),
                                           })


@login_required
def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get("text")
    uploaded_file = request.FILES.get("pics")

    if uploaded_file:
        name = uploaded_file.name
        with open("./moments/static/image/{}".format(name), 'wb') as handler:
            for block in uploaded_file.chunks():
                handler.write(block)
    else:
        name = ''

    if text:
        status = Status(user=user, text=text, pics=name)
        status.save()
        return redirect("{}status".format(SITE_URL))

    return render(request, "my_post.html")



@login_required
def show_post(request):
    user = WeChatUser.objects.get(user=request.user)

    text = request.POST.get('text')
    upload_file = request.FILES.get('pic')
    if upload_file:
        file_name = upload_file.name
        with open("static/image/{}".format(file_name), 'wb') as f:
            for block in upload_file.chunks():
                f.write(block)
    else:
        file_name = ""
    if text:
        status = Status(text=text, user=user, pics=file_name)
        status.save()
        return redirect("{}status".format(SITE_URL))
    return render(request, "my_post.html")


def register(request):
    try:

        username, password, email = [request.POST.get(i) for i in ("username", "password", "email")]

        # user = User(username=username, email=email)
        # user.set_password(password)
        # user.save()
        WeChatUser.objects.create(user=request.user,email=email)
    except Exception as e:
        result = False
        message = str(e)
    else:

        result = True
        message = "Register success"
    return JsonResponse({"result": result, "message": message})


def update_user(request):
    try:
        kwargs = {key: request.POST.get(key) for key in ("region", "motto", "pic","email") if request.POST.get(key)}
        WeChatUser.objects.filter(user=request.user).update(**kwargs)

        # email = request.POST.get("email")
        # if email:
        #     we_user = WeChatUser.objects.get(user=request.user)
        #     we_user.user.email = email
        #     we_user.user.save()

    except Exception as e:
        result = False
        message = str(e)
    else:
        result = True
        message = "Update success"
    return JsonResponse({"result": result, "message": message})


@login_required
def like(request):
    user = request.user.username
    status_id = request.POST.get("status_id")
    like = Reply.objects.filter(author=user, status=status_id, type="0")
    if like:
        like.delete()
    else:
        Reply.objects.create(author=user, status=Status.objects.get(id=status_id), type="0")
        client = get_client_by_request(request)
        client.cmsi.send.mail(receiver =Status.objects.get(id=status_id).user.email
                              ,title = "点赞通知",content='<div><b><u style="">{}</u></b>&nbsp;赞了你的朋友圈状态&nbsp;<i style=""><b style=""><font color="#333300" size="4">{}</font></b></i></div>'.format(user,Status.objects.get(id=status_id).text))
    return JsonResponse({"result": True})


@login_required
def comment(request):
    user = request.user.username
    status_id = request.POST.get("status_id")
    at_person = request.POST.get("at_person", "")
    text = request.POST.get("text")

    Reply.objects.create(author=user, status=Status.objects.get(id=status_id), type="1", at_person=at_person, text=text)
    return JsonResponse({"result": True})


@login_required
def delete_comment(request):
    comment_id = request.POST.get("comment_id")
    Reply.objects.filter(id=comment_id).delete()
    return JsonResponse({"result": True})

@login_required
def report(request):
    return render(request,'report.html')

def stats(request):
    statuses = Status.objects.all()
    values = list(statuses.values_list("user__user__username"))
    counter = Counter(values)
    top_five = counter.most_common(5)
    response = {
        "code": 0,
        "result": True,
        "message": "success",
        "data": {
            "xAxis": [{
                "type": "category",
                "data": [user[0][0] for user in top_five]
            }],
            "series": [{
                "name": "发状态数",
                "type": "bar",
                "data": [user[1] for user in top_five]
            }]
        }

    }
    return JsonResponse(response)


@login_required
def friends(request):
    return render(request, "friends.html")