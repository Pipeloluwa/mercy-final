from django.db import models

# Create your models here.

class Book(models.Model):
    added_or_issued_date = models.DateTimeField(auto_now_add=True)
    author= models.CharField(max_length=50)
    title= models.CharField(max_length=50)
    genre= models.CharField(max_length=50)
    isbn= models.PositiveIntegerField(unique=True)
    description= models.TextField(max_length=50)
    book_cover_picture= models.ImageField(upload_to="bookcover")
    privatize_book= models.BooleanField()
    maximum_no_of_borrowing_days= models.CharField(max_length=50)
    no_of_book_available= models.PositiveIntegerField()
    book_pdf_file= models.FileField(upload_to="book_pdf_file")

    def __str__(self):
        return f"{self.added_or_issued_date},{self.author},{self.title},{self.genre},{self.isbn}," \
            f"{self.description},{self.book_cover_picture},{self.privatize_book},{self.maximum_no_of_borrowing_days}," \
            f"{self.no_of_book_available},{self.book_pdf_file}"


class Book_Return_And_History(models.Model):
    username= models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50,null=True,blank=True)
    isbn= models.CharField(max_length=50)
    date_borrowed= models.DateTimeField(blank=True,null=True)
    expected_return_date= models.DateTimeField(blank=True,null=True)
    return_date= models.DateTimeField(blank=True,null=True)
    late_return= models.CharField(max_length=3,blank=True,null=True)
    book_cover_picture= models.ImageField(upload_to="individual_cover",blank=True,null=True)
    book_pdf_file = models.FileField(upload_to="book_pdf_file")
    borrowed_workaround_date= models.CharField(max_length=50, blank=True,null=True)
    expected_workaround_date = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username},{self.author},{self.title},{self.genre},{self.isbn},{self.date_borrowed},{self.expected_return_date}" \
            f",{self.return_date},{self.late_return},{self.book_cover_picture},{self.book_pdf_file}," \
            f"{self.borrowed_workaround_date},{self.expected_workaround_date}"

class Borrower_User(models.Model):
    username= models.CharField(max_length=50, unique=True)
    email= models.EmailField()
    phone_no= models.CharField(max_length=15)
    user_details= models.ManyToManyField(Book_Return_And_History,blank=True)

    def __str__(self):
        return f"{self.username},{self.email},{self.phone_no}"



