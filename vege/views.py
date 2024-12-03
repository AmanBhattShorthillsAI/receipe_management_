from django.shortcuts import render, redirect
from .models import Receipe, Student, SubjectMarks
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum


# Create your views here.
@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        print(receipe_name, receipe_description)
        receipe_image = request.FILES.get("receipe_image")
        print(receipe_image)

        Receipe.objects.create(
            user=request.user,
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
        )

        return redirect("/receipes")

    queryset = Receipe.objects.filter(user=request.user)

    return render(request, "receipes.html", context={"receipes": queryset})


def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        return redirect("/receipes")

    context = {"receipe": queryset}

    return render(request, "update_receipe.html", context)


def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect("/receipes/")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Clear session data before logging in
        request.session.flush()

        checkuser = User.objects.filter(username=username)
        if not checkuser.exists():
            messages.error(request, "Invalid Username")
            return redirect("/login/")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Username")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/receipes/")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if user.exists():
            # messages.error(request, "User already exists")
            messages.info(request, "Username already exists")
            return redirect("/register/")

        user = User.objects.create(
            first_name=first_name, last_name=last_name, username=username
        )

        user.set_password(password)  ## this will set the password in encrypted format
        user.save()
        messages.info(request, "Account created Successfully")
        return redirect("/register/")

    return render(request, "register.html")


def get_students(request):
    students = Student.objects.all()
    
    if request.GET.get("search"):
        search = request.GET.get("search")
        students = students.filter(
            Q(student_name__icontains=search)
            | Q(student_email__icontains=search)
            | Q(student_address__icontains=search)
            | Q(department__department__icontains=search)
            | Q(student_id__student_id__icontains=search)
        )

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "report/students.html", context={"students": page_obj})


from .seed import generate_report_card  # noqa: E402
def see_marks(request, student_id):
    generate_report_card()
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = queryset.aggregate(total_marks = Sum('marks'))
    current_rank = -1
    if queryset.exists():
        ranks = Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks', '-student_age')
        i=1
        for rank in ranks:
            if student_id == rank.student_id.student_id:
                current_rank = i
                break
            i+=1
    else:
        current_rank = None
    return render(request, "report/see_marks.html", context={"queryset": queryset, 'total_marks': total_marks, 'current_rank': current_rank})
