from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Book, Review
from django.contrib.auth.mixins import LoginRequiredMixin


class ListBookView(LoginRequiredMixin ,ListView):
    template_name = 'bookapp/book_list.html'
    model = Book

class DetailBookView(LoginRequiredMixin, DetailView):
    template_name = 'bookapp/book_detail.html'
    model = Book

class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = 'bookapp/book_create.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')

class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'bookapp/book_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = 'bookapp/book_update.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')

def index_view(request):
    object_list = Book.objects.order_by('category')
    return render(request, 'bookapp/index.html', {'object_list': object_list})

class CreateReviewView(CreateView):
    model = Review
    fields = ('book', 'title', 'text', 'rate')
    template_name = 'bookapp/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('detail-book', kwargs={'pk': self.object.book.id})
