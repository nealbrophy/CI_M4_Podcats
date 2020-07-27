from allauth.account.forms import LoginForm

def login_ctx_tag(request):
    return {'loginctx': LoginForm()}