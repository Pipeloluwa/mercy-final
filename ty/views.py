from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from django.shortcuts import render, redirect
#from .models import

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from .models import Book,Borrower_User,Book_Return_And_History
from django.contrib.auth.models import User

from datetime import datetime, timedelta



def error404(request,exception):
    data={}
    return render(request,"404.html")


def index(request):
    notice=None
    ax = False
    try:
        if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
            ax = True

    except:
        pass




    obj= Book.objects.all()
    total_book=len(obj)
    play=0
    novel=0
    poetry=0
    for i in obj:
        if i.genre=="Play":
            play+=1
        elif i.genre=="Novel":
            novel+=1
        elif i.genre=="Poetry":
            poetry+=1


    book_8=[]
    nb=len(obj)
    for i in obj:
        nb-=1
        book_8.append(obj[nb])
        if nb+8 == len(obj):
            break

    try:
        info = Borrower_User.objects.get(username=request.user)
        info2 = info.user_details.all()
        bookList = []
        bookList2 = []
        for i in info2:
            bookList2.append(int(i.isbn))
    except:
        bookList2=[]
    return render(request,'index.html',{'total_book':total_book,'play':play,'novel':novel,'poetry':poetry,'book_8':book_8,
                        'bookList2':bookList2, "ax":ax})


def about(request):
    # ax= False
    # if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
    #     ax = True

    return render(request,"about.html",{"ax":ax})

def contact(request):
    ax= False
    try:
        if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
            ax = True
    except:
        pass
    return render(request,"contact.html",{"ax":ax})



@login_required(login_url="signin")
def borrow_book_index(request,isbn):
    if request.user.is_authenticated:
        try:
            getBook = Book.objects.get(isbn=isbn)
            if Book_Return_And_History.objects.get(isbn=isbn).username == str(request.user):
                Book_Return_And_History.objects.get(isbn=isbn).delete()

                dNOW = datetime.now()
                onth1 = datetime.strptime(f"{dNOW.month}", "%m").strftime("%b")

                dNOW2 = dNOW + timedelta(days=int(getBook.maximum_no_of_borrowing_days))
                onth2 = datetime.strptime(f"{dNOW2.month}", "%m").strftime("%b")

                workaround1 = f"{onth1} {dNOW.day}, {dNOW.year}" \
                    f" {dNOW.hour}:{dNOW.minute}:{dNOW.second}"
                workaround2 = f"{onth2} {dNOW2.day}, {dNOW2.year}" \
                    f" {dNOW2.hour}:{dNOW2.minute}:{dNOW2.second}"

                infob = Book_Return_And_History.objects.create(username=request.user,
                                                               author=getBook.author, title=getBook.title,
                                                               genre=getBook.genre,
                                                               isbn=getBook.isbn, date_borrowed=dNOW,
                                                               expected_return_date=dNOW2,
                                                               book_cover_picture=getBook.book_cover_picture,
                                                               book_pdf_file=getBook.book_pdf_file,
                                                               borrowed_workaround_date=workaround1,
                                                               expected_workaround_date=workaround2)

                gu = Borrower_User.objects.get(username=request.user)
                gu.user_details.add(infob)

                getBook.no_of_book_available = int(getBook.no_of_book_available) - 1
                getBook.save()
                return redirect('index')
        except:
            dNOW = datetime.now()
            onth1 = datetime.strptime(f"{dNOW.month}", "%m").strftime("%b")

            dNOW2 = dNOW + timedelta(days=int(getBook.maximum_no_of_borrowing_days))
            onth2 = datetime.strptime(f"{dNOW2.month}", "%m").strftime("%b")

            workaround1 = f"{onth1} {dNOW.day}, {dNOW.year}" \
                f" {dNOW.hour}:{dNOW.minute}:{dNOW.second}"
            workaround2 = f"{onth2} {dNOW2.day}, {dNOW2.year}" \
                f" {dNOW2.hour}:{dNOW2.minute}:{dNOW2.second}"

            infob = Book_Return_And_History.objects.create(username=request.user,
                                                           author=getBook.author, title=getBook.title,
                                                           genre=getBook.genre,
                                                           isbn=getBook.isbn, date_borrowed=dNOW,
                                                           expected_return_date=dNOW2,
                                                           book_cover_picture=getBook.book_cover_picture,
                                                           book_pdf_file=getBook.book_pdf_file,
                                                           borrowed_workaround_date=workaround1,
                                                           expected_workaround_date=workaround2)

            gu = Borrower_User.objects.get(username=request.user)
            gu.user_details.add(infob)

            getBook.no_of_book_available = int(getBook.no_of_book_available) - 1
            getBook.save()
            return redirect('index')
        return redirect('index')
    else:
        return redirect('signin')



def sign_in(request):
    ax= False
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        try:
            if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
                ax = True
        except:
            pass

        if request.method == "POST":
            login_user= authenticate(request, username= request.POST.get("username").lower(), password= request.POST.get("password"))
            try:
                login(request,login_user)
                return redirect("dashboard")
            except:
                try:
                    User.objects.get_by_natural_key(username=request.POST.get("username").lower())
                    return render(request,"signin.html",{"err":"Your password is not correct.","ax":ax})
                except:
                    return render(request, "signin.html", {"err": "This Username is not Recognized","ax":ax})
        return render(request,'signin.html')



def sign_up(request):
    ax= False
    try:
        if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
            ax = True
    except:
        pass

    if request.method == "POST":
        control=True
        try:
            #EXCEPTION FOR USERNAME IF ALREADY EXISTS
            username= request.POST.get("username").lower()
            email=request.POST.get("email")
            phone_no=request.POST.get("phoneno")
            password= request.POST.get("password1")
            password2 = request.POST.get("password2")
            try:
                Borrower_User.objects.get(username=username.lower())
                control= False
                return render(request,'signup.html',{"signup":True, "namefail":True,"ax":ax})
            except:
                #EXCEPTION FOR PASSWORD IF THEY DO NOT MATCH
                if password != password2:
                    control= False
                    return render(request, 'signup.html', {"signup": True, "passwordfail": True,"ax":ax})
                else:
                    #CREATING ACOOUNT
                    #TRYING TP MAKE Django User Creation ABIDE BY MY RULE
                    if control:
                        Borrower_User.objects.create(username=username,
                                                     email=email,
                                                     phone_no=phone_no)
                        User.objects.create_user(username=username,email=email,password=password)
                        return render(request, 'signup.html', {"signup":False,"ssuccess": True,"ax":ax})
                    return render(request, 'signup.html', {"signup": True, "sfailure": True,"ax":ax})
        except:
            return render(request, 'signup.html',{"signup":True,"sfailure": True,"ax":ax})
    return render(request,'signup.html',{"signup":True})



@login_required (login_url="signin")
def edit_password(request):
    ax= False
    if request.user.is_authenticated:
        try:
            if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
                ax = True
        except:
            pass

        if request.method== "POST":
            try:
                p1=request.POST.get("password1")
                p2 = request.POST.get("password2")

                getU = User.objects.get(username=request.user)
                print(getU.password)

                if authenticate(request,username= request.user, password= request.POST.get("passwordc")):
                    if p1 == p2:
                        u_EL= getU.email
                        u_S= request.user
                        getU.delete()
                        User.objects.create_user(username=u_S, email=u_EL, password=p1)
                        return render(request, "edit-password.html", {"success": True,"ax":ax})
                    else:
                        return render(request, "edit-password.html", {"failure2": True,"ax":ax})
                else:
                    return render(request, "edit-password.html", {"failure": True,"ax":ax})
            except:
                return HttpResponse("Something went wrong")
        return render(request,"edit-password.html",{"ax":ax})
    else:
        return redirect('signin')


@login_required (login_url="signin")
def edit_account(request):
    ax= False
    if request.user.is_authenticated:
        try:
            if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
                ax = True
        except:
            pass
        if request.method=="POST":
            try:
                if not request.POST.get("email") and not request.POST.get("phoneno"):
                    return render(request, "edit-account.html", {"failure": True})
                if request.POST.get("email"):
                    getU=User.objects.get(username=request.user)
                    getU.email= request.POST.get("email")
                    getU2 = Borrower_User.objects.get(username=request.user)
                    getU2.email = request.POST.get("email")
                    getU.save(),getU2.save()
                if request.POST.get("phoneno"):
                    getU3=Borrower_User.objects.get(username=request.user)
                    getU3.phone_no= request.POST.get("phoneno")
                    getU3.save()
                return render(request, "edit-account.html",{"success":True,"ax":ax})
            except:
                return HttpResponse("Soething went wrong")
        return render(request,"edit-account.html",{"ax":ax})
    else:
        return redirect('signin')



@login_required (login_url="signin")
def alert(request):
    ax=False
    if request.user.is_authenticated:
        try:
            if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
                ax = True
        except:
            pass
        try:
            info = Borrower_User.objects.get(username=request.user)
            info2 = info.user_details.all()
        except:
            pass
        return render(request,"alert.html",{"info2":info2,"ax":ax})
    return redirect('signin')


@login_required(login_url='signin')
def log_out(request):
    try:
        logout(request)
        return redirect('index')
    except:
        return redirect('index')


@login_required (login_url="signin")
def dashboard(request):
    ax= False
    if request.user.is_authenticated:
        ax=False
        try:
            info= Borrower_User.objects.get(username= request.user)
            info2= info.user_details.all()
            bookNo = len(info2)
            exp= datetime.now()
        except:
            pass

        try:
            if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
                ax = True
        except:
            pass

        try:
            return render(request,'dashboard.html',{"info2":info2,"info":info,'bookNo':bookNo,'exp':exp,
                                "ax":(ax)})
        except:
            return render(request, 'dashboard.html', {"ax": (ax)})
    else:
        return redirect('signin')


def books_play(request):
    try:
        book = Book.objects.all()

        global keeprowpl
        keeprowpl = []
        all_c = book
        keepobj = []
        keepno = 0
        nmbr = 0
        for i in all_c:
            keepno += 1
            keepobj.append(i)
            if keepno == 9:
                keepno = 0
                keeprowpl.append(keepobj)
                keepobj = []

        if request.user.is_authenticated:
            try:
                try:
                    if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
                        ax = True
                except:
                    pass

                user_activity = None
                info=""
                info2=""
                try:
                    info = Borrower_User.objects.get(username=request.user)
                    info2 = info.user_details.all()
                except:
                    pass
                bookListp = list(book)
                bookList = []
                bookList2 = []
                bookNo = len(info2)
                for i in info2:
                    bookList2.append(int(i.isbn))




                if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
                    keeprowpl.append(keepobj)
                if len(keeprowpl) > 1:  # to enable page
                    return render(request, "books-play.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                          "pageno": len(keeprowpl),
                                                          "book": keeprowpl[0], 'bookList2': bookList2, 'bookNo': bookNo,
                                                               "ax":ax,
                                                          })
                return render(request, "books-play.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                           "book": keeprowpl[0], 'bookList2': bookList2,
                                                           'bookNo': bookNo,
                                                           "ax": ax,
                                                           })
            except:
                pass
        else:
            if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
                keeprowpl.append(keepobj)
            if len(keeprowpl) > 1:  # to enable page
                return render(request, "books-play.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                           "pageno": len(keeprowpl),
                                                           "book": keeprowpl[0],
                                                           })
            return render(request, "books-play.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                       "book": keeprowpl[0]
                                                       })
    except:
        return render(request, "books-play.html")

def npagepl(request, nmbr):
    try:
        if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
            ax = True
    except:
        pass

    global keeprowpl
    nmbr += 1
    return render(request, "books-play.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprowpl[nmbr], "pageno": len(keeprowpl),
                   "curr_page": nmbr + 1,"ax":ax})

def ppagepl(request, nmbr):
    try:
        if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
            ax = True
    except:
        pass

    global keeprowpl
    nmbr -= 1
    return render(request, "books-play.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprowpl[nmbr], "pageno": len(keeprowpl),
                   "curr_page": nmbr + 1, "ax":ax})





def books_novel(request):
    ax= False
    try:
        try:
            if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
                ax = True
        except:
            pass

        book = Book.objects.all()
        global keeprownv
        keeprownv = []
        all_c = book
        keepobj = []
        keepno = 0
        nmbr = 0
        for i in all_c:
            keepno += 1
            keepobj.append(i)
            if keepno == 9:
                keepno = 0
                keeprownv.append(keepobj)
                keepobj = []

        if request.user.is_authenticated:
            user_activity = None
            try:
                info = Borrower_User.objects.get(username=request.user)
                info2 = info.user_details.all()
                bookListp = list(book)
                bookList = []
                bookList2 = []
                bookNo = len(info2)
                for i in info2:
                    bookList2.append(int(i.isbn))

                if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
                    keeprownv.append(keepobj)
                if len(keeprownv) > 1:  # to enable page
                    return render(request, "books-novel.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                                "pageno": len(keeprownv),
                                                                "book": keeprownv[0], 'bookList2': bookList2,
                                                                'bookNo': bookNo,
                                                                "ax": ax
                                                                })
                return render(request, "books-novel.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                            "book": keeprownv[0], 'bookList2': bookList2,
                                                            'bookNo': bookNo,
                                                            "ax": ax
                                                            })
            except:
                pass
        else:
            if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
                keeprownv.append(keepobj)
            if len(keeprownv) > 1:  # to enable page
                return render(request, "books-novel.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                      "pageno": len(keeprownv),
                                                      "book": keeprownv[0],
                                                      })
            return render(request, "books-novel.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                        "book": keeprownv[0],
                                                        })
    except:
        return render(request, "books-novel.html")

def npagenv(request, nmbr):
    ax = False
    if Borrower_User.objects.get(username=str(request.user)).user_details.all():
        ax = True

    global keeprownv
    nmbr += 1
    return render(request, "books-novel.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprownv[nmbr], "pageno": len(keeprownv),
                   "curr_page": nmbr + 1, "ax":ax})

def ppagenv(request, nmbr):
    ax = False
    if Borrower_User.objects.get(username=str(request.user)).user_details.all():
        ax = True

    global keeprownv
    nmbr -= 1
    return render(request, "books-novel.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprownv[nmbr], "pageno": len(keeprownv),
                   "curr_page": nmbr + 1, "ax":ax})







def books_poetry(request):
    ax= False
    try:
        ax = False
        try:
            if Borrower_User.objects.get(username=str(request.user)).user_details.all():
                ax = True
        except:
            pass

        book = Book.objects.all()

        global keeprowpy
        keeprowpy = []
        all_c = book
        keepobj = []
        keepno = 0
        nmbr = 0
        for i in all_c:
            keepno += 1
            keepobj.append(i)
            if keepno == 9:
                keepno = 0
                keeprowpy.append(keepobj)
                keepobj = []

        if request.user.is_authenticated:
            try:
                user_activity = None
                info = Borrower_User.objects.get(username=request.user)
                info2 = info.user_details.all()
                bookListp = list(book)
                bookList = []
                bookList2 = []
                bookNo = len(info2)
                for i in info2:
                    bookList2.append(int(i.isbn))


                if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
                    keeprowpy.append(keepobj)
                if len(keeprowpy) > 1:  # to enable page
                    return render(request, "books-poetry.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                          "pageno": len(keeprowpy),
                                                          "book": keeprowpy[0], 'bookList2': bookList2, 'bookNo': bookNo,
                                                            "ax":ax,
                                                          })
                return render(request, "books-poetry.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                      "book": keeprowpy[0], 'bookList2': bookList2, 'bookNo': bookNo,
                                                             "ax":ax})
            except:
                pass

        if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
            keeprowpy.append(keepobj)
        if len(keeprowpy) > 1:  # to enable page
            return render(request, "books-poetry.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                         "pageno": len(keeprowpy),
                                                         "book": keeprowpy[0],
                                                         "ax": ax,
                                                         })
        return render(request, "books-poetry.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                     "book": keeprowpy[0],
                                                     "ax": ax,})
    except:
        return render(request, "books-poetry.html")

def npagepy(request, nmbr):
    ax = False
    if Borrower_User.objects.get(username=str(request.user)).user_details.all():
        ax = True

    global keeprowpy
    nmbr += 1
    return render(request, "books-poetry.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprowpy[nmbr], "pageno": len(keeprowpy),
                   "curr_page": nmbr + 1, "ax":ax})

def ppagepy(request, nmbr):
    ax = False
    if Borrower_User.objects.get(username=str(request.user)).user_details.all():
        ax = True

    global keeprowpy
    nmbr -= 1
    return render(request, "books-poetry.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprowpy[nmbr], "pageno": len(keeprowpy),
                   "curr_page": nmbr + 1, "ax":ax})





def books(request):
    ax= False
    try:
        ax = False
        try:
            if Borrower_User.objects.get(username=str(request.user)).user_details.all():
                ax = True
        except:
            pass

        book= Book.objects.all()
        global keeprow
        keeprow = []
        all_c = book
        keepobj = []
        keepno = 0
        nmbr = 0
        for i in all_c:
            keepno += 1
            keepobj.append(i)
            if keepno == 9:
                keepno = 0
                keeprow.append(keepobj)
                keepobj = []


        if request.user.is_authenticated:
            try:
                user_activity= None
                info = Borrower_User.objects.get(username=request.user)
                info2 = info.user_details.all()
                bookList=[]
                bookList2=[]
                bookNo = len(info2)
                for i in info2:
                    bookList2.append(int(i.isbn))

                if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
                    keeprow.append(keepobj)
                if len(keeprow) > 1:  # to enable page
                    return render(request, "books.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                         "pageno": len(keeprow),
                                                          "book": keeprow[0],'bookList2': bookList2, 'bookNo': bookNo,
                                                          "ax":ax,"ax":ax
                                                    })
                return render(request, "books.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                      "book": keeprow[0],'bookList2': bookList2, 'bookNo': bookNo,
                                                      "ax":ax, "ax":ax})
            except:
                pass

        if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
            keeprow.append(keepobj)
        if len(keeprow) > 1:  # to enable page
            return render(request, "books.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,
                                                  "pageno": len(keeprow),
                                                  "book": keeprow[0],  "ax": ax
                                                  })
        return render(request, "books.html", {"enablepage": False, "nmbr": nmbr, "curr_page": nmbr + 1,
                                              "book": keeprow[0], "ax": ax})
    except:
        return render(request, "books.html")

def npage(request, nmbr):
    ax = False
    if Borrower_User.objects.get(username=str(request.user)).user_details.all():
        ax = True

    global keeprow
    nmbr += 1
    return render(request, "books.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprow[nmbr], "pageno": len(keeprow),
                   "curr_page": nmbr + 1,"ax":ax})

def ppage(request, nmbr):
    ax = False
    if Borrower_User.objects.get(username=str(request.user)).user_details.all():
        ax = True

    global keeprow
    nmbr -= 1
    return render(request, "books.html",
                  {"enablepage": True, "nmbr": nmbr, "book": keeprow[nmbr], "pageno": len(keeprow),
                   "curr_page": nmbr + 1, "ax":ax})



@login_required(login_url="signin")
def borrow_book(request,isbn):
    ax= False
    if request.user.is_authenticated:
        ax = False
        if Borrower_User.objects.get(username=str(request.user)).user_details.all():
            ax = True

        getBook= Book.objects.get(isbn=isbn)
        # dt.replace(dt.year, dt.month, dt.day + 3, dt.hour, dt.minute, dt.second, dt.microsecond)
        # dt.replace(2022,5,3,21,22,42,774445)

        try:
            if Book_Return_And_History.objects.get(isbn=isbn).username== str(request.user):
                Book_Return_And_History.objects.get(isbn=isbn).delete()

                dNOW = datetime.now()
                onth1 = datetime.strptime(f"{dNOW.month}", "%m").strftime("%b")

                dNOW2 = dNOW + timedelta(days=int(getBook.maximum_no_of_borrowing_days))
                onth2 = datetime.strptime(f"{dNOW2.month}", "%m").strftime("%b")

                workaround1 = f"{onth1} {dNOW.day}, {dNOW.year}" \
                    f" {dNOW.hour}:{dNOW.minute}:{dNOW.second}"
                workaround2 = f"{onth2} {dNOW2.day}, {dNOW2.year}" \
                    f" {dNOW2.hour}:{dNOW2.minute}:{dNOW2.second}"

                infob = Book_Return_And_History.objects.create(username=request.user,
                                                               author=getBook.author, title=getBook.title,
                                                               genre=getBook.genre,
                                                               isbn=getBook.isbn, date_borrowed=dNOW,
                                                               expected_return_date=dNOW2,
                                                               book_cover_picture=getBook.book_cover_picture,
                                                               book_pdf_file=getBook.book_pdf_file,
                                                               borrowed_workaround_date=workaround1,
                                                               expected_workaround_date=workaround2)

                gu = Borrower_User.objects.get(username=request.user)
                gu.user_details.add(infob)

                getBook.no_of_book_available = int(getBook.no_of_book_available) - 1
                getBook.save()
                return redirect('books')
        except:
            dNOW = datetime.now()
            onth1= datetime.strptime(f"{dNOW.month}","%m").strftime("%b")

            dNOW2= dNOW + timedelta(days=int(getBook.maximum_no_of_borrowing_days))
            onth2 = datetime.strptime(f"{dNOW2.month}", "%m").strftime("%b")

            workaround1 = f"{onth1} {dNOW.day}, {dNOW.year}" \
                f" {dNOW.hour}:{dNOW.minute}:{dNOW.second}"
            workaround2 = f"{onth2} {dNOW2.day}, {dNOW2.year}" \
                f" {dNOW2.hour}:{dNOW2.minute}:{dNOW2.second}"

            infob= Book_Return_And_History.objects.create(username=request.user,
                        author=getBook.author,title=getBook.title,genre=getBook.genre,
                        isbn=getBook.isbn,date_borrowed=dNOW,expected_return_date=dNOW2,
                        book_cover_picture=getBook.book_cover_picture,book_pdf_file= getBook.book_pdf_file,
                        borrowed_workaround_date=workaround1,expected_workaround_date=workaround2)

            gu= Borrower_User.objects.get(username=request.user)
            gu.user_details.add(infob)

            getBook.no_of_book_available = int(getBook.no_of_book_available) - 1
            getBook.save()
            return redirect('books')
        return HttpResponse("You can not borrow book, it is out of Stock")
    else:
        return redirect("signin")

def release_book(request,isbn):
    ax= False
    if request.user.is_authenticated:
        ax = False
        if Borrower_User.objects.get(username=str(request.user)).user_details.all():
            ax = True

        try:
            if Book_Return_And_History.objects.get(isbn=isbn).username== str(request.user):
                gBr= Book_Return_And_History.objects.get(isbn=isbn)
                # Book_Return_And_History.objects.get(isbn=isbn).delete()
                Us= Borrower_User.objects.get(username=str(request.user))
                gUsd= Borrower_User.objects.get(username= str(request.user)).user_details.get(isbn=isbn)
                Us.user_details.remove(gUsd)

                getBook = Book.objects.get(isbn=isbn)
                getBook.no_of_book_available = int(getBook.no_of_book_available) + 1
                getBook.save()
                return redirect('dashboard')
            return HttpResponse("This Book has already been removed from your dashboard")
        except:
            return HttpResponse("This Book has already been removed from your dashboard")

        return redirect('dashboard')



def search(request):
    ax = False
    if Borrower_User.objects.get(username=str(request.user)).user_details.all():
        ax = True

    if request.method == "POST":
        ax = False
        if len(Borrower_User.objects.get(username=request.user).user_details.all()) >= 1:
            ax = True

        token = ""
        getSearch = request.POST.get("keywords")
        # getSearch= getSearch.lower()
        news_obj = Book.objects.all()
        object_store = []

        # SEARCH ALGORITHM
        # GETTING DIFFERENT CATEGORY BY TITLE OR AUTHOR OR GENRE
        if (request.POST.get("category")) == "Search Category By Title":


            # INTELLIGENT SEARCH ALORITHM SPLIT SEARCH TOKEN
            # SPLIT SEARCH TOKEN
            getSearchList = []
            compilelist = ""
            for i in getSearch.lower():
                if i == " ":
                    getSearchList.append(compilelist)
                    compilelist = ""
                else:
                    compilelist += i
            getSearchList.append(compilelist)

            # INTELLIGENT SEARCH ALORITHM
            appendletter = []
            storeletter = ""
            countletter = -1
            object_store2=[]
            for i in news_obj:
                for j in i.title.lower():
                    # print(len(i.title))
                    countletter += 1
                    if j == " ":
                        # print(storeletter)
                        if storeletter in getSearchList:
                            object_store.append(i)
                            object_store2.append(i.isbn)
                            appendletter.append(storeletter)
                            break
                        storeletter = ""
                    else:
                        storeletter += j
                        if countletter == len(i.title) - 1:
                            if storeletter in getSearchList:
                                object_store.append(i)
                                object_store2.append(i.isbn)
                            appendletter.append(storeletter)
                storeletter = ""
                countletter = -1


            if object_store != []:
                # RECENT NEWS
                related_genre_list = []
                cn=0

                for i in Book.objects.all():
                    if i.genre == object_store[0].genre and i.isbn not in object_store2:
                        related_genre_list.append(i)
                # END


                related_genre = []
                for i in range(len(related_genre_list)):
                    def change():
                        rd = random.choice(related_genre_list)
                        if rd in related_genre:
                            change()
                        else:
                            related_genre.append(rd)

                    change()
                return render(request, "search section.html", {"s_result": object_store,
                                                           "related_genre": related_genre,"ax":ax,
                                                               "ax":ax})
            # END
            return render(request, "search section.html", {"s_result": None,
                                                           "related_genre": None, "ax": ax,
                                                           "ax":ax})



        elif (request.POST.get("category"))== "Search Category By Author":

            # INTELLIGENT SEARCH ALORITHM SPLIT SEARCH TOKEN
            # SPLIT SEARCH TOKEN
            getSearchList = []
            compilelist = ""
            for i in getSearch.lower():
                if i == " ":
                    getSearchList.append(compilelist)
                    compilelist = ""
                else:
                    compilelist += i
            getSearchList.append(compilelist)
            print(getSearchList)

            # INTELLIGENT SEARCH ALORITHM
            appendletter = []
            storeletter = ""
            countletter = -1
            object_store2=[]
            for i in news_obj:
                for j in i.author.lower():
                    # print(len(i.title))
                    countletter += 1
                    if j == " ":
                        # print(storeletter)
                        if storeletter in getSearchList:
                            object_store.append(i)
                            print(storeletter)
                            appendletter.append(storeletter)
                            object_store2.append(i.isbn)
                            break
                        storeletter = ""
                    else:
                        storeletter += j
                        if countletter == len(i.author) - 1:
                            print(storeletter)
                            if storeletter in getSearchList:
                                object_store.append(i)
                                object_store2.append(i.isbn)
                            appendletter.append(storeletter)
                            # print(storeletter)
                storeletter = ""
                countletter = -1

            print(appendletter)

            if object_store != []:
                # RECENT NEWS
                related_genre_list = []
                for i in Book.objects.all():
                    if i.genre == object_store[0].genre and i.isbn not in object_store2:
                        related_genre_list.append(i)
                    # END


                related_genre = []
                for i in range(len(related_genre_list)):
                    def change():
                        rd = random.choice(related_genre_list)
                        if rd in related_genre:
                            change()
                        else:
                            related_genre.append(rd)
                    change()
                return render(request, "search section.html", {"s_result": object_store,
                                                               "related_genre": related_genre, "ax": ax,
                                                               "ax":ax})
            # END
            return render(request, "search section.html", {"s_result": None,
                                                           "related_genre": None, "ax": ax,
                                                           "ax":ax})


        elif (request.POST.get("category")) == "Search Category By Genre":

            # INTELLIGENT SEARCH ALORITHM SPLIT SEARCH TOKEN
            # SPLIT SEARCH TOKEN
            getSearchList = []
            compilelist = ""
            for i in getSearch.lower():
                if i == " ":
                    getSearchList.append(compilelist)
                    compilelist = ""
                else:
                    compilelist += i
            getSearchList.append(compilelist)
            print(getSearchList)

            # INTELLIGENT SEARCH ALORITHM
            appendletter = []
            storeletter = ""
            countletter = -1

            for i in news_obj:
                for j in i.genre.lower():
                    # print(len(i.title))
                    countletter += 1
                    if j == " ":
                        # print(storeletter)
                        if storeletter in getSearchList:
                            object_store.append(i)
                            print(storeletter)
                            appendletter.append(storeletter)
                            break
                        storeletter = ""
                    else:
                        storeletter += j
                        if countletter == len(i.genre) - 1:
                            print(storeletter)
                            if storeletter in getSearchList:
                                object_store.append(i)
                            appendletter.append(storeletter)
                            # print(storeletter)
                storeletter = ""
                countletter = -1

            print(appendletter)

            if object_store != []:
                # RECENT NEWS
                return render(request, "search section.html", {"s_result": object_store,
                                                                "ax": ax, "ax":ax})
            # END
            return render(request, "search section.html", {"s_result": object_store,
                                                           "ax": ax, "ax":ax})

    return render(request,"search section.html",{"ax":ax})
