from django.urls import path,include, re_path
from . import views
from .views import *

urlpatterns = [
    path('',views.index,name='index'),
    path('error404', views.error404, name='error404'),

    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('index/books/borrow/str:<isbn>', views.borrow_book_index, name='borrow-book-index'),
    path('sign-in',views.sign_in, name="signin"),
    path('register', views.sign_up, name="signup"),

    path('alert', views.alert, name="alert"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.log_out, name="logout"),
    path('dashboard/edit-account', views.edit_account, name="edit-account"),
    path('dashboard/edit-password', views.edit_password, name="edit-password"),

    path('books', views.books, name="books"),
    path("books/next-page/<int:nmbr>", views.npage, name="npage"),
    path("books/previous-page/<int:nmbr>", views.ppage, name="ppage"),

    path('books-play', views.books_play, name="books-play"),
    path("books/next-page-play/<int:nmbr>", views.npagepl, name="npagepl"),
    path("books/previous-page-play/<int:nmbr>", views.ppagepl, name="ppagepl"),

    path('books-novel', views.books_novel, name="books-novel"),
    path("books/next-page-novel/<int:nmbr>", views.npagenv, name="npagenv"),
    path("books/previous-page-novel/<int:nmbr>", views.ppagenv, name="ppagenv"),

    path('books-poetry', views.books_poetry, name="books-poetry"),
    path("books/next-page-poetry/<int:nmbr>", views.npagepy, name="npagepy"),
    path("books/previous-page-poetry/<int:nmbr>", views.ppagepy, name="ppagepy"),

    path('search', views.search, name="search"),
    path('books/borrow/str:<isbn>', views.borrow_book, name='borrow-book'),
    path('books/release/str:<isbn>', views.release_book, name='release-book')
]