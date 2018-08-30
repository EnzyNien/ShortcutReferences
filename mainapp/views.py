
from urllib.parse import unquote

from django.shortcuts import render, HttpResponse
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.sites.shortcuts import get_current_site
from mainapp.models import ShortcutRef, ReferencesToLinks



def main(request):

    context = dict()
    context['min_mf'] = ShortcutRef.MIN_mf
    context['max_mf'] = ShortcutRef.MAX_mf

    render_result = render(request, 'mainapp/index.html', context)
    return HttpResponse(render_result)


def shortcut(request, url='', *args, **kwargs):

    obj_ShortcutRef = ShortcutRef.objects.filter(short_url=url).first()
    if not obj_ShortcutRef:
        raise Http404("Короткая ссылка не зарегистрирована в базе")
    if not obj_ShortcutRef.active:
        raise Http404(
            "Короткая ссылка уже не активная так как имеет максимальное количество переходов")

    obj_ReferencesToLinks = ReferencesToLinks()
    obj_ReferencesToLinks.parent = obj_ShortcutRef
    obj_ReferencesToLinks.ip = request.META.get("REMOTE_ADDR", "")
    obj_ReferencesToLinks.user_agent = request.META.get("HTTP_USER_AGENT", "")
    obj_ReferencesToLinks.save()

    if obj_ShortcutRef.get_the_remaining_transitions == 0:
        obj_ShortcutRef.active = False
        obj_ShortcutRef.save()

    return HttpResponseRedirect(obj_ShortcutRef.real_url)


def add_url(request, *args, **kwargs):

    if request.is_ajax():
        real_url_ = request.POST.get('real_url', None)
        max_following_ = request.POST.get('max_following', 5)

    elif request.method == "GET":
        real_url_ = request.GET.get('real_url', None)
        max_following_ = request.GET.get('max_following', 5)

    else:
        raise Http404("Не верные параметры запроса")

    result = dict()
    accept = True
    errors = []

    try:
        max_following_ = int(max_following_)
    except ValueError:
        accept = False
        errors.append({'name': 'max_following_err',
                       'err': 'ошибка значения количества переходов'})
    else:
        if max_following_ < ShortcutRef.MIN_mf:
            max_following_ = ShortcutRef.MIN_mf
        elif max_following_ > ShortcutRef.MAX_mf:
            max_following_ = ShortcutRef.MAX_mf
        errors.append({'name': 'max_following_err', 'err': ''})

    if real_url_ is None or not real_url_:
        accept = False
        errors.append({'name': 'real_url_err',
                       'err': 'ошибка значение сокращаемой ссылки'})
    else:
        errors.append({'name': 'real_url_err', 'err': ''})

    real_url_ = unquote(real_url_)
    result['real_url'] = real_url_
    result['max_following'] = max_following_
    result['short_url'] = ''
    if accept:
        obj_ShortcutRef = ShortcutRef.objects.filter(
            short_url=ShortcutRef.create_short_url(real_url_)).first()
        if not obj_ShortcutRef:
            obj_ShortcutRef = ShortcutRef.objects.create(**result)
            obj_ShortcutRef.save()
            errors.append({'name': 'short_url_create', 'err': ''})
        else:
            errors.append({'name': 'short_url_create',
                           'err': 'Короткая ссылка по данному адресу уже создана ранее'})
        short_url_full = obj_ShortcutRef.get_short_url_full(
            request.build_absolute_uri())
        result['short_url'] = short_url_full
        result['max_following_ret'] = obj_ShortcutRef.get_the_remaining_transitions

    result['accept'] = accept
    result['errors'] = errors
    return JsonResponse(result)
