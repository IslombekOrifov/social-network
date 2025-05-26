from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from post.models import Post


class FeedListView(LoginRequiredMixin, ListView):
    template_name = 'feed/index.html' 
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        subscribed_users = user.get_subscriptions()

        queryset = Post.objects.filter(
            owner__in=subscribed_users,
            is_archive=False,
            is_banned=False
        ).select_related('owner').prefetch_related(
            'media_files', 'tags', 'likes'
        )

        post_type = self.request.GET.get('type')
        if post_type:
            queryset = queryset.filter(post_type=post_type)
            
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        page_size = self.request.GET.get('page_size', self.paginate_by)
        try:
            page_size = min(int(page_size), 100) 
        except (TypeError, ValueError):
            page_size = self.paginate_by
            
        paginator = Paginator(self.get_queryset(), page_size)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = page_obj.has_other_pages()
        context['request'] = self.request
        
        return context