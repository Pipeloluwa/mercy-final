from django.contrib import admin
from .models import Book,Borrower_User,Book_Return_And_History

# Register your models here.

class tc1(admin.ModelAdmin):
    list_display = ("added_or_issued_date","author","title","genre","isbn",
                    "description","book_cover_picture","privatize_book","maximum_no_of_borrowing_days",
                    "no_of_book_available","book_pdf_file",)
    list_filter = ("isbn",)

class tc2(admin.ModelAdmin):
    list_display = ("username","email","phone_no",)
    list_filter = ("username",)

class tc3(admin.ModelAdmin):
    list_display = ("username","author","title","genre","isbn","date_borrowed","expected_return_date" \
                    ,"return_date","late_return","book_cover_picture","book_pdf_file",
                    "borrowed_workaround_date","expected_workaround_date",)
    list_filter = ("isbn",)


admin.site.register(Book,tc1)
admin.site.register(Borrower_User,tc2)
admin.site.register(Book_Return_And_History,tc3)
