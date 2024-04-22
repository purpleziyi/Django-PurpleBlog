from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .forms import PubBlogForm
from django.db.models import Q


# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request,'index.html', context={'blogs':blogs})

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html', context={'blog': blog})


# @login_required(login_url=reverse_lazy("pzauth:login"))
# @login_required(login_url="/auth/login")
@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={"categories": categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            # author is the current user, so it can be gotten by request.user
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            # 若要获取用户输入在富文本框内的数据，就必须通过js才能获取到，所以只能通过Ajax请求才能获取，故而返回JsonResponse
            return JsonResponse({"code": 200, "message": "Blog published successfully!", "data": {"blog_id": blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, "message": "Parameter error!"})


@require_POST
@login_required()   # as long as you login can you publish
def pub_comment(request):
    blog_id = request.POST.get('blog_id')     # 获取评论id
    content = request.POST.get('content')     # 获取评论内容
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    # 重新加载博客详情页 redirect the details of the blog-side
    return redirect(reverse("blog:blog_detail", kwargs={'blog_id': blog_id}))


@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    # 从博客的标题和内容中查找含有q关键字的博客
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, 'index.html', context={"blogs": blogs})