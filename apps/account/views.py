from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from post.models import Post


class MyProfileView(LoginRequiredMixin, View):
    template_name = 'account/my_profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(owner=user, is_archive=False, is_banned=False).select_related('owner').prefetch_related('media_files', 'tags', 'likes')

        page_size = request.GET.get('page_size', 10)
        try:
            page_size = min(int(page_size), 100)
        except (TypeError, ValueError):
            page_size = 10

        paginator = Paginator(posts, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'user': user,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': page_obj.has_other_pages(),
            'request': request,
        }
        
        return render(request, self.template_name, context)

