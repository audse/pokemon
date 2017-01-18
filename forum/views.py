from django.template.defaultfilters import slugify

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
import datetime

from .models import Bookmark, Category, Post, Reply
from django.contrib.auth.models import User

from core import views as core_views

# Create your views here.

def forum_index(request):
	action = "Viewing the forums"
	core_views.update_online(request, action)

	# gets just the core categories

	core_categories = Category.objects.filter(overarching_category="core")
	for category in core_categories:
		posts = Post.objects.filter(category=category, deleted=False)
		category.posts = posts.count()

		if posts.count() is not 0:
			category.last_post = posts.latest('post_time')

	# gets the general categories

	general_categories = Category.objects.filter(overarching_category="general")
	for category in general_categories:
		posts = Post.objects.filter(category=category, deleted=False)
		category.posts = posts.count()

		if posts.count() is not 0:
			category.last_post = posts.latest('post_time')

	return render(request, 'forum/index.html', {'core_categories':core_categories, 'general_categories':general_categories});

def category(request, category):
	action = "Viewing the "+category+" forum"
	core_views.update_online(request, action)

	stickied_posts = Post.objects.filter(category__name=category, stickied=True, deleted=False).order_by('-post_time')
	posts = Post.objects.filter(category__name=category, stickied=False, deleted=False).order_by('-post_time')

	display = True
	if category == "Announcements":
		display = False

	for post in posts:
		replies = Reply.objects.filter(original=post, deleted=False)
		post.replies = replies.count()

		if replies.count() is not 0:
			post.last_reply = replies.latest('post_time')


	for post in stickied_posts:
		replies = Reply.objects.filter(original=post, deleted=False)
		post.replies = replies.count()

		if replies.count() is not 0:
			post.last_reply_time = replies.latest('post_time')

	# pagination
	paginator = Paginator(posts, 20)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if not int, show first page
		posts = paginator.page(1)
	except EmptyPage:
		# out of range, show last page
		posts = paginator.page(paginator.num_pages)

	return render(request, 'forum/category.html', {'posts':posts, 'category':category, 'stickied_posts':stickied_posts, 'display':display})

def view_post(request, pk):

	post = get_object_or_404(Post, pk=pk)

	action = "Viewing the forum post &quot;"+post.title+"&quot;"
	core_views.update_online(request, action)

	replies = Reply.objects.filter(original=post)

	# check for if its bookmarked, if so update last_viewed
	if request.user.is_authenticated():

		bookmark = Bookmark.objects.filter(post=post, bookmarker=request.user).first()
		if bookmark:
			bookmark.last_viewed = datetime.datetime.now()
			bookmark.save()

	# pagination
	paginator = Paginator(replies, 20)
	page = request.GET.get('page')
	try:
		replies = paginator.page(page)
	except PageNotAnInteger:
		replies = paginator.page(1)
	except EmptyPage:
		replies = paginator.page(paginator.num_pages)

	return render(request, 'forum/view_post.html', {'post':post, 'replies':replies})

def edit_post_page(request, pk):

	action = "Editing a Forum Post"
	core_views.update_online(request, action)

	post = get_object_or_404(Post, pk=pk)
	if request.user.is_authenticated():
		if request.user == post.author:
			return render(request, 'forum/edit_post.html', {'post':post})
		else:
			return redirect(core_views.must_be_logged_in)
	else:
		return redirect(core_views.must_be_logged_in)

def edit_post(request, pk):
	post = Post.objects.get(pk=pk)
	new_title = request.POST.get('title')
	new_body_text = request.POST.get('body_text')

	if request.user.is_authenticated():
		if request.user == post.author:

			post.title = new_title
			post.body_text = new_body_text
			post.save(update_fields=['title', 'body_text'])

			return redirect(view_post, pk=post.pk) 

		else:
			return redirect(core_views.must_be_logged_in)
	else:
		return redirect(core_views.must_be_logged_in)

def reply(request, pk):
	post = get_object_or_404(Post, pk=pk)
	reply_text = request.POST.get('reply_text')

	if request.user.is_authenticated():
		if reply_text:
			if not post.locked:
				reply = Reply.objects.create(author=request.user, original=post, body_text=reply_text)
				return redirect(view_post, pk=post.pk)
			else:
				return redirect(view_post, pk=post.pk)
		else:
			return redirect(view_post, pk=post.pk)

def edit_reply(request, pk):
	reply = Reply.objects.get(pk=pk)
	post = reply.original
	new_body_text = request.POST.get('body_text')

	if request.user.is_authenticated():
		if request.user == reply.author:
			reply.body_text = new_body_text
			reply.save()
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(core_views.must_be_logged_in)
	else:
		return redirect(core_views.must_be_logged_in)

def lock(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.user.is_authenticated():
		if request.user.is_staff:
			post.locked = True
			post.save()
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(staff_only)
	else:
		return redirect(must_be_logged_in)

def unlock(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.user.is_authenticated():
		if request.user.is_staff:
			post.locked = False
			post.save()
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(staff_only)
	else:
		return redirect(must_be_logged_in)

def sticky(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.user.is_authenticated():
		if request.user.is_staff:
			post.stickied = True
			post.save()
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(staff_only)
	else:
		return redirect(must_be_logged_in)

def unsticky(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.user.is_authenticated():
		if request.user.is_staff:
			post.stickied = False
			post.save()
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(core_views.staff_only)
	else:
		return redirect(must_be_logged_in)

def delete(request, pk):
	post = get_object_or_404(Post, pk=pk)

	if request.user.is_authenticated():
		if request.user.is_staff:
			post.deleted = True
			post.save()
			return redirect(forum_index)
		else:
			return redirect(core_views.staff_only)
	else:
		return redirect(core_views.must_be_logged_in)

def delete_reply(request, pk):
	reason = request.POST.get('reason')

	reply = Reply.objects.get(pk=pk)
	post = reply.original

	if request.user.is_authenticated():
		if request.user.is_staff:
			reply.deleted = True
			reply.deleted_reason = reason
			reply.save()
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(core_views.staff_only)
	else:
		return redirect(core_views.must_be_logged_in)

def delete_reply_true(request, pk):
	reply = Reply.objects.get(pk=pk)
	post = reply.original
	if request.user.is_authenticated():
		if request.user.is_staff:
			reply.delete()
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(core_views.staff_only)
	else:
		return redirect(core_views.must_be_logged_in)

def new_post_page(request, category):
	action = "Creating a forum post"
	core_views.update_online(request, action)

	if request.user.is_authenticated():
		category = get_object_or_404(Category, name=category)
		return render(request, 'forum/new_post.html', {'category':category})
	else:
		return redirect(core_views.must_be_logged_in)

def new_post(request):
	title = request.POST.get('title')
	body_text = request.POST.get('body_text')
	category = request.POST.get('category')
	category = get_object_or_404(Category, name=category)

	if request.user.is_authenticated():
		if category.name == "Announcements" and request.user.is_staff == False:
			return redirect(core_views.staff_only)
		if title and body_text and category:
			post = Post.objects.create(title=title, author=request.user, body_text=body_text, category=category)
			return redirect(view_post, pk=post.pk)
		else:
			return redirect(new_post_page, category=category.name)
	else:
		return redirect(core_views.must_be_logged_in)

def view_bookmarks(request):
	action = "Viewing bookmarked post"
	core_views.update_online(request, action)

	if request.user.is_authenticated():
		bookmarks = Bookmark.objects.filter(bookmarker=request.user)
		for bookmark in bookmarks:
			new_replies = Reply.objects.filter(original=bookmark.post, deleted=False, post_time__gt=bookmark.last_viewed)
			bookmark.new = new_replies.count()

		return render(request, "forum/view_bookmarks.html", {'bookmarks':bookmarks})
	else:
		return redirect(core_views.must_be_logged_in)

def bookmark(request, pk):
	if request.user.is_authenticated():
		post = Post.objects.filter(pk=pk).first()
		bookmark = Bookmark.objects.filter(bookmarker=request.user, post=post)
		if bookmark.count() is 0:
			bookmark =  Bookmark.objects.create(bookmarker=request.user, post=post)
			return redirect(view_post, pk=pk)
		else:
			return redirect(view_post, pk=pk)
	else:
		return redirect(core_views.must_be_logged_in)

def delete_bookmark(request, pk):
	if request.user.is_authenticated():
		bookmark = Bookmark.objects.filter(pk=pk).first()
		bookmark.delete()
		return redirect(view_bookmarks)
	else:
		return redirect(core_views.must_be_logged_in)










