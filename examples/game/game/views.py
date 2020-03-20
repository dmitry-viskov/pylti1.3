import datetime
import os
import pprint
import uuid

from django.core.cache import caches
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.urls import reverse
from pylti1p3.contrib.django import DjangoOIDCLogin, DjangoMessageLaunch
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from pylti1p3.tool_config import ToolConfJsonFile


PAGE_TITLE = 'Game Example'


class ExtendedDjangoMessageLaunch(DjangoMessageLaunch):

    def validate_nonce(self):
        """
        Probably it is bug on "https://lti-ri.imsglobal.org":
        site passes invalid "nonce" value during deep links launch.
        Because of this in case of iss == http://imsglobal.org just skip nonce validation.

        """
        iss = self._get_iss()
        deep_link_launch = self.is_deep_link_launch()
        if iss == "http://imsglobal.org" and deep_link_launch:
            return self
        return super(ExtendedDjangoMessageLaunch, self).validate_nonce()


class DjangoFakeRequest(object):

    GET = {}
    POST = {}
    COOKIES = {}
    session = None
    _is_secure = False

    def __init__(self, GET, POST, COOKIES, session, is_secure):
        self.GET = GET
        self.POST = POST
        self.COOKIES = COOKIES
        self._is_secure = is_secure
        self.session = session

    def is_secure(self):
        return self._is_secure


def get_lti_config_path():
    return os.path.join(settings.BASE_DIR, '..', 'configs', 'game.json')


def get_launch_url(request):
    target_link_uri = request.POST.get('target_link_uri', request.GET.get('target_link_uri'))
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')
    return target_link_uri


def check_cookies_allowed(request):
    test_cookie_val = request.COOKIES.get('test_cookie', None)
    request_ts = request.GET.get('ts', None)
    cookie_sent = bool(request_ts and test_cookie_val and request_ts == test_cookie_val)
    return JsonResponse({'cookies_allowed': cookie_sent})


def login(request):
    cache = caches['default']
    cookies_allowed = str(request.GET.get('cookies_allowed', ''))
    if cookies_allowed:
        login_unique_id = str(request.GET.get('login_unique_id', ''))
        if not login_unique_id:
            raise Exception('Missing "login_unique_id" param')

        login_data = cache.get(login_unique_id)
        if not login_data:
            raise Exception("Can't restore login data from cache")

        tool_conf = ToolConfJsonFile(get_lti_config_path())
        request_like_obj = DjangoFakeRequest(
            login_data['GET'], login_data['POST'],
            request.COOKIES, request.session, request.is_secure())
        oidc_login = DjangoOIDCLogin(request_like_obj, tool_conf)
        target_link_uri = get_launch_url(request_like_obj)
        return oidc_login.redirect(target_link_uri)
    else:
        login_unique_id = str(uuid.uuid4())
        cache.set(login_unique_id, {
            'GET': {k: v for k, v in request.GET.items()},
            'POST': {k: v for k, v in request.POST.items()}
        }, 3600)
        return render(request, 'check_cookie.html', {
            'login_unique_id': login_unique_id,
            'same_site': getattr(settings, 'SESSION_COOKIE_SAMESITE'),
            'page_title': PAGE_TITLE
        })


def launch(request):
    cache = caches['default']
    launch_unique_id = str(request.GET.get('launch_id', ''))

    # reload page in case if cookie is unavailable (chrome samesite issue)
    if not request.session.session_key and not launch_unique_id:
        launch_unique_id = str(uuid.uuid4())
        cache.set(launch_unique_id, {
            'GET': {k: v for k, v in request.GET.items()},
            'POST': {k: v for k, v in request.POST.items()}
        }, 3600)
        current_url = request.build_absolute_uri()
        if '?' in current_url:
            current_url += '&'
        else:
            current_url += '?'
        current_url = current_url + 'launch_id=' + launch_unique_id
        return HttpResponse('<script type="text/javascript">window.location="%s";</script>' % current_url)

    request_like_obj = None
    if request.method == "GET":
        launch_data = cache.get(launch_unique_id)
        if not launch_data:
            raise Exception("Can't restore launch data from cache")
        request_like_obj = DjangoFakeRequest(
            launch_data['GET'], launch_data['POST'],
            request.COOKIES, request.session, request.is_secure())

    tool_conf = ToolConfJsonFile(get_lti_config_path())
    message_launch = ExtendedDjangoMessageLaunch(request_like_obj if request_like_obj else request, tool_conf)
    message_launch_data = message_launch.get_launch_data()
    pprint.pprint(message_launch_data)

    return render(request, 'game.html', {
        'page_title': PAGE_TITLE,
        'is_deep_link_launch': message_launch.is_deep_link_launch(),
        'launch_data': message_launch.get_launch_data(),
        'launch_id': message_launch.get_launch_id(),
        'curr_user_name': message_launch_data.get('name', ''),
        'curr_diff': message_launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {})
                  .get('difficulty', 'normal')})


def configure(request, launch_id, difficulty):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    message_launch = ExtendedDjangoMessageLaunch.from_cache(launch_id, request, tool_conf)

    if not message_launch.is_deep_link_launch():
        return HttpResponseForbidden('Must be a deep link!')

    launch_url = request.build_absolute_uri(reverse('game-launch'))

    resource = DeepLinkResource()
    resource.set_url(launch_url)\
        .set_custom_params({'difficulty': difficulty})\
        .set_title('Breakout ' + difficulty + ' mode!')

    html = message_launch.get_deep_link().output_response_form([resource])
    return HttpResponse(html)


@require_POST
def score(request, launch_id, earned_score, time_spent):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    message_launch = ExtendedDjangoMessageLaunch.from_cache(launch_id, request, tool_conf)

    if not message_launch.has_ags():
        return HttpResponseForbidden("Don't have grades!")

    sub = message_launch.get_launch_data().get('sub')
    timestamp = datetime.datetime.utcnow().isoformat()
    earned_score = int(earned_score)
    time_spent = int(time_spent)

    grades = message_launch.get_ags()
    sc = Grade()
    sc.set_score_given(earned_score)\
        .set_score_maximum(100)\
        .set_timestamp(timestamp)\
        .set_activity_progress('Completed')\
        .set_grading_progress('FullyGraded')\
        .set_user_id(sub)

    sc_line_item = LineItem()
    sc_line_item.set_tag('score')\
        .set_score_maximum(100)\
        .set_label('Score')

    grades.put_grade(sc, sc_line_item)

    tm = Grade()
    tm.set_score_given(time_spent)\
        .set_score_maximum(999)\
        .set_timestamp(timestamp)\
        .set_activity_progress('Completed')\
        .set_grading_progress('FullyGraded')\
        .set_user_id(sub)

    tm_line_item = LineItem()
    tm_line_item.set_tag('time')\
        .set_score_maximum(999)\
        .set_label('Time Taken')

    result = grades.put_grade(tm, tm_line_item)

    return JsonResponse({'success': True, 'result': result.get('body')})


def scoreboard(request, launch_id):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    message_launch = ExtendedDjangoMessageLaunch.from_cache(launch_id, request, tool_conf)

    if not message_launch.has_nrps():
        return HttpResponseForbidden("Don't have names and roles!")

    if not message_launch.has_ags():
        return HttpResponseForbidden("Don't have grades!")

    ags = message_launch.get_ags()

    score_line_item = LineItem()
    score_line_item.set_tag('score') \
        .set_score_maximum(100) \
        .set_label('Score')
    scores = ags.get_grades(score_line_item)

    time_line_item = LineItem()
    time_line_item.set_tag('time') \
        .set_score_maximum(999) \
        .set_label('Time Taken')
    times = ags.get_grades(time_line_item)

    members = message_launch.get_nrps().get_members()
    scoreboard_result = []

    for sc in scores:
        result = {'score': sc['resultScore']}
        for tm in times:
            if tm['userId'] == sc['userId']:
                result['time'] = tm['resultScore']
                break
        for member in members:
            if member['user_id'] == sc['userId']:
                result['name'] = member.get('name', 'Unknown')
                break
        scoreboard_result.append(result)

    return JsonResponse(scoreboard_result, safe=False)
