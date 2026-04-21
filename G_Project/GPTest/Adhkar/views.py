from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404, redirect
from django.http import  HttpResponse
from .models import *
from django.views import View
from .form import RegisterForm
from django.urls import reverse_lazy
#view in the brain between the models and the template بياخد من الموديلز ويعرض في التمبليت
#FBV
#def home(request):
 #   return HttpResponse("Hello Habiba ")
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def home2(request):
    total=UserProfile.objects.get(user=request.user).total_points
    return render(request,'pages/home.html', {'total': total})

def morning(reqest):
    data1=Category.objects.filter(name='Morning')
    adhkars1 = Adhkar.objects.filter(category=data1.first())
    return render(reqest,'pages/morning.html',{'data1':data1, 'adhkars1': adhkars1})
def evening(reqest):
    data2=Category.objects.filter(name='Evening')
    adhkars2 = Adhkar.objects.filter(category=data2.first())
    return render(reqest,'pages/evening.html',{'data2':data2, 'adhkars2': adhkars2})
def sleep(reqest):
    data3=Category.objects.filter(name='Sleep')
    adhkars3 = Adhkar.objects.filter(category=data3.first())
    return render(reqest,'pages/sleep.html',{'data3':data3, 'adhkars3': adhkars3})
class CompleteAdhkarView(LoginRequiredMixin, View):
    def post(self, request, adhkhar_id):
        adhkar_obj = get_object_or_404(Adhkar, id=adhkhar_id)
        UserProgress.objects.create(
            user=request.user,
            adhkar=adhkar_obj,
            points_earned=adhkar_obj.points_value
        )
        profile = request.user.userprofile 
        profile.total_points += adhkar_obj.points_value
        profile.save()
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
def profile_view(request):
    user_reminder = Notification.objects.filter(user=request.user).first()
    all_categories = Category.objects.all()
    my_rewards = UserReward.objects.filter(user=request.user)
    
    context = {
        'user_reminder': user_reminder,
        'all_categories': all_categories,
        'my_rewards': my_rewards,
    }
    return render(request, 'pages/profile.html', context)

def save_reminder(request):
    if request.method == "POST":
        time_val = request.POST.get('reminder_time')
        cat_id = request.POST.get('category_id')
        category_obj = get_object_or_404(Category, id=cat_id)

        Notification.objects.update_or_create(
            user=request.user,
            category=category_obj,
            defaults={'reminder_time': time_val, 'is_enabled': True}
        )
        return redirect('profile')
#ListView:بدل م اعمل FBV واعمل .all()دي بتسهلها عليا
class AdhkarList(ListView):
   model=Adhkar
   template_name='pages/AdhkarList.html'
   context_object_name='adhkarL'
#لو عاوز اعرض تفاصيل ذكر واحد بس بعمل DetailView
class AdhkarDetail(DetailView):
    model=Adhkar
    template_name='pages/AdhkarDetail.html'
    context_object_name='adhkarD'
#لو عاوز ا create بعمل CreateView
class AdhkarCreate(CreateView):
    model=Adhkar
    fields=['Category','title','content','points_value']
    template_name='pages/createad.html'
    success_url=reverse_lazy('adkar_list')
    def test_func(self):
        return self.request.user.is_superuser

class AdhkarUpdate(UpdateView):    
    model=Adhkar
    fields=['Category','title','content','points_value']
    template_name='pages/updatead.html'
    success_url=reverse_lazy('adkar_list')
    def test_func(self):
        return self.request.user.is_superuser
class AdhkarDelete(DeleteView):
    model=Adhkar
    template_name='pages/deletead.html'
    success_url=reverse_lazy('adkar_list')
    def test_func(self):
        return self.request.user.is_superuser
     