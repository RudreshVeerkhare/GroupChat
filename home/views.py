from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Group, Messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    GroupUpdateForm,
    GroupProfileUpdateForm,
    MessageCreateForm,
    GroupCreateForm,
    GroupProfileCreateForm,
    SearchUserForm,
    AddMemberForm
)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
import json
from django.utils.safestring import mark_safe

# Create your views here.


@login_required
def home(request):
    groups = request.user.all_groups.all()
    if request.method == "POST":
        g_form = GroupCreateForm(request.POST)

        if g_form.is_valid():
            group = g_form.save(commit=False)
            group.creater = request.user
            group.save()
            group.members.add(request.user)
            return redirect("home:group_profile", grp_name=group.group_name)
    else:
        g_form = GroupCreateForm()

    context = {
        "groups": groups,
        "g_form" : g_form
    }
    return render(request, "home/home.html", context)


# class GroupCreateView(LoginRequiredMixin, CreateView):

#     template_name = "home/home.html"
#     fields = ['group_name' , 'group_info']

#     def get_queryset(self):
#         return self.request.user.all_groups.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["groups"] = self.request.user.all_groups.all()
#         return context

    
    


# @login_required
# def group(request, grp_name):
#     group = get_object_or_404(Group, group_name=grp_name)
#     # To check wether user is member of group or not
#     try:
#         request.user.all_groups.get(group_name=grp_name)
#         # above line will throw exception if user is not permitted for the view
#         msgs = Messages.objects.filter(parent_group=group).all()
#         context = {"msgs": msgs, "group_name": grp_name}
#         return render(request, "home/group.html", context)

#     except Group.DoesNotExist:
#         raise Http404("Group Does not exist")


# class MessageCreateView(LoginRequiredMixin, CreateView):
    
#     # queryset = Messages.objects.filter(group_name=grp_name)
#     form_class = MessageCreateForm
#     model = Messages
#     template_name = 'home/group.html'


#     def dispatch(self, request, *args, **kwargs):
#         self.grp_name = kwargs['grp_name']
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         grp = Group.objects.get(group_name=self.grp_name)
#         context["msgs"] = reversed(grp.messages.order_by('date_posted')[:50])
#         context["group_name"] = self.grp_name
#         return context

#     def form_valid(self, form):
#         form.instance.parent_group = Group.objects.get(group_name=self.grp_name)
#         form.instance.parent_user = self.request.user
#         return super().form_valid(form)
    
@login_required
def group(request, grp_name):

    try:
        group = request.user.all_groups.get(group_name=grp_name)
    except Group.DoesNotExist:
        raise Http404("Group Does not exist or You are not member of this group")

    return render(request, 'home/group.html', {
        'room_name_json': mark_safe(json.dumps(grp_name)),
        'group' : group
        })

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserRegisterForm()

    return render(request, "home/register.html", {"form": form})


@login_required
def profile(request, user_name):

    # This will allow us to show updation form only if user is on own profile
    if request.user.username == user_name:
        if request.method == "POST":
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.profile
            )

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect("home:profile", user_name=user_name)

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {"required_user": request.user, "u_form": u_form, "p_form": p_form}

    else:
        required_user = get_object_or_404(User, username=user_name)
        context = {"required_user": required_user}

    return render(request, "home/profile.html", context)


@login_required
def group_profile(request, grp_name):
    try:
        group = request.user.all_groups.get(group_name=grp_name)
        # above line will throw exception if user is not permitted for the view
        members = group.members.all()

        if request.user.username == group.creater.username:
            if request.method == "POST":
                g_form = GroupUpdateForm(request.POST, instance=group)
                gp_form = GroupProfileUpdateForm(
                    request.POST, request.FILES, instance=group.group_profile
                )

                if g_form.is_valid() and gp_form.is_valid():
                    g_form.save()
                    gp_form.save()

                    return redirect("home:group_profile", grp_name=group.group_name)

            else:
                g_form = GroupUpdateForm(instance=group)
                gp_form = GroupProfileUpdateForm(instance=group.group_profile)

            context = {
                "members": members,
                "group": group,
                "g_form": g_form,
                "gp_form": gp_form,
            }

        else:
            context = {"members": members, "group": group}

        return render(request, "home/group_profile.html", context)

    except Group.DoesNotExist:
        raise Http404("Group Does not exist")

@login_required
def search_user(request):
    if request.method == 'POST':
        form = SearchUserForm(request.POST)

        if form.is_valid():
            users = User.objects.filter(username__startswith=form.cleaned_data.get("user_name"))

            context = {
                "users" : users,
                "form" : form
            }
            return render(request, "home/search_user.html", context)
    else:
        form = SearchUserForm()
        context = {
            "form" : form
        }

    return render(request, "home/search_user.html", context)



@login_required
def add_member(request, grp_name):
    
    

    try:
        global group
        group = Group.objects.get(group_name=grp_name)
        flag = group.members.get(username=request.user.username)
    except Group.DoesNotExist:
        raise Http404("Group Does not exist")



    if  flag:
        print(group.group_profile.image.url)
        if request.method == 'POST':
            if 'user_name' in request.POST and 'users' not in request.POST:

                form = SearchUserForm(request.POST)
                userlistform = AddMemberForm()

                if form.is_valid():
                    global users_for_choices # To access it accross if statements
                    users_for_choices = [ (user.id, user.username) for user in User.objects.filter(username__startswith=form.cleaned_data.get("user_name"))]
                    userlistform.fields['users'].choices = users_for_choices
                    form = SearchUserForm()
                    context = {
                        "group" : group,
                        "form" : form
                    }
                    if len(users_for_choices) > 0:
                        context["list"] = userlistform
                    print(users_for_choices)
                    return render(request, "home/add_members.html", context)
            
            # else:
            if 'users' in request.POST:
                userlist = AddMemberForm(request.POST)
                userlist.fields['users'].choices = users_for_choices

                if userlist.is_valid():
                    users = userlist.cleaned_data.get('users')
                    for user in users:
                        group.members.add(User.objects.get(id=user[0]))

                    return redirect('home:group', grp_name=grp_name)


                else:
                    print(userlist.errors.as_text())
                    form = SearchUserForm()
                    context = {
                        "form" : form,
                        "group" : group
                    }
                    
                    

            

        else:
            form = SearchUserForm()
            context = {
                "form" : form,
                "group" : group
            }
            

        return render(request, "home/add_members.html", context)
