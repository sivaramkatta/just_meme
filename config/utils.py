from django.db import models
from django.shortcuts import render


class TimestampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def error_404(request, exception):
    return render(request, 'error.html', status=404, context={"msg": "Page you requesting is not found"})


def error_500(request):
    return render(request, 'error.html', status=500, context={"msg": "Some error occurred please try after sometime"})
