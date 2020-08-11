from rest_framework.pagination import PageNumberPagination


class CustomPostsPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 50


class CustomCommentsPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 20
