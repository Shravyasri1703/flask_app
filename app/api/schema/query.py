from ariadne import QueryType
from app.auth.decorators import login_required, get_current_user

query = QueryType()


@query.field("me")
@login_required
def resolve_me(*_):
    """Resolver for the 'me' query - returns the current user"""
    user = get_current_user()
    if user:
        return user.to_dict()
    return None