from django.shortcuts import render

def base(request):
    # template_name = 'templates/base.html'
    return render(request, 'base.html')