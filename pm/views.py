from django.shortcuts import render, redirect
from .models import PM
from core.views import must_be_logged_in, user_not_found, cannot_access, update_online

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def pm_index(request):
	if request.user.is_authenticated():
		action = "Viewing private messages"
		update_online(request, action)

		sent_pms = PM.objects.filter(sending_user=request.user, removed_by_sender=False).order_by("-send_time")
		received_pms = PM.objects.filter(receiving_user=request.user, removed_by_receiver=False).order_by("-send_time")
		return render(request, 'pm/index.html', {'sent_pms':sent_pms, 'received_pms':received_pms})
	else:
		return redirect(must_be_logged_in)

def send_pm_page(request, username):
	if request.user.is_authenticated():
		action = "Sending a private messages"
		update_online(request, action)

		return render(request, 'pm/send_pm.html', {'username':username})	
	else:
		return redirect(must_be_logged_in)

def send_pm(request):
	if request.user.is_authenticated():
		action = "Sending a private messages"
		update_online(request, action)

		receiving_user_username = request.POST.get("username")
		subject = request.POST.get("subject")
		message = request.POST.get("message")

		receiving_user = User.objects.filter(username=receiving_user_username)
		if receiving_user.count() != 0:
			receiving_user = receiving_user.first()
			pm = PM.objects.create(sending_user=request.user, receiving_user=receiving_user, subject=subject, message=message)
			return redirect(pm_index)
		else:
			return redirect(user_not_found)
	else:
		return redirect(must_be_logged_in)

def reply_page(request, pk):
	if request.user.is_authenticated():
		action = "Replying to a private messages"
		update_online(request, action)

		pm = PM.objects.filter(pk=pk)
		if pm.count() != 0:
			pm = pm.first()
			if pm.receiving_user == request.user:
				return render(request, 'pm/reply.html', {'pm':pm})
			else:
				return redirect(cannot_access)
		else:
			return redirect(pm_index)
	else:
		return redirect(must_be_logged_in)

def reply(request):
	if request.user.is_authenticated():
		action = "Replying to a private messages"
		update_online(request, action)

		parent_pm_pk = request.POST.get("parent")
		message = request.POST.get("message")
		parent_pm = PM.objects.filter(pk=parent_pm_pk)
		if parent_pm.count() != 0:
			parent_pm = parent_pm.first()
			if parent_pm.receiving_user == request.user:
				parent_pm.seen = True
				parent_pm.replied = True
				parent_pm.save()
				pm = PM.objects.create(sending_user=request.user, receiving_user=parent_pm.sending_user, subject=parent_pm.subject, message=message, parent_pm=parent_pm)
				return redirect(pm_index)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pm_index)
	else:
		return redirect(must_be_logged_in)

def mark_as_read(request, pk):
	if request.user.is_authenticated():
		action = "Viewing private messages"
		update_online(request, action)

		pm = PM.objects.filter(pk=pk)
		if pm.count() != 0:
			pm = pm.first()
			if pm.receiving_user == request.user:
				pm.seen = True
				pm.save()
				return redirect(pm_index)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pm_index)
	else:
		return redirect(must_be_logged_in)

def remove_from_sent(request, pk):
	if request.user.is_authenticated():
		action = "Viewing private messages"
		update_online(request, action)

		pm = PM.objects.filter(pk=pk)
		if pm.count() != 0:
			pm = pm.first()
			if pm.sending_user == request.user:
				pm.removed_by_sender = True
				pm.save()
				return redirect(pm_index)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pm_index)
	else:
		return redirect(must_be_logged_in)

def remove_from_received(request, pk):
	if request.user.is_authenticated():
		action = "Viewing private messages"
		update_online(request, action)
		
		pm = PM.objects.filter(pk=pk)
		if pm.count() != 0:
			pm = pm.first()
			if pm.receiving_user == request.user:
				pm.removed_by_receiver = True
				pm.save()
				return redirect(pm_index)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pm_index)
	else:
		return redirect(must_be_logged_in)









