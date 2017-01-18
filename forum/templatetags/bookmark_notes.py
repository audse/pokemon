from django.template import Library

from forum.models import Bookmark, Reply

register = Library()

@register.filter(name="bookmark_notes")
def bookmark_notes(user):
	notifications = 0
	bookmarks = Bookmark.objects.filter(bookmarker=user)
	for bookmark in bookmarks:
		new_replies = Reply.objects.filter(original=bookmark.post, deleted=False, post_time__gt=bookmark.last_viewed).count()
		if new_replies > 0:
			notifications = notifications + 1
	return notifications
