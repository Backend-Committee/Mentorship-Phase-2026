def is_owner(user, post):
    return user.id == post.owner_id