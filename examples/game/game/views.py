import datetime
import os

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from pylti1p3.contrib.django import DjangoOIDCLogin, DjangoMessageLaunch
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from pylti1p3.tool_config import ToolConfJsonFile


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


def get_lti_config_path():
    return os.path.join(settings.BASE_DIR, '..', 'configs', 'game.json')


def get_launch_url(request):
    return request.build_absolute_uri(reverse('game-launch'))


def login(request):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    oidc_login = DjangoOIDCLogin(request, tool_conf)
    return oidc_login.redirect(get_launch_url(request))


@require_POST
def launch(request):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    message_launch = ExtendedDjangoMessageLaunch(request, tool_conf)
    message_launch_data = message_launch.get_launch_data()

    return render(request, 'game.html', {
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
        raise Exception('Must be a deep link!')

    resource = DeepLinkResource()
    resource.set_url(get_launch_url(request))\
        .set_custom_params({'difficulty': difficulty})\
        .set_title('Breakout ' + difficulty + ' mode!')

    html = message_launch.get_deep_link().output_response_form([resource])
    return HttpResponse(html)


@require_POST
def score(request, launch_id, earned_score, time_spent):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    message_launch = ExtendedDjangoMessageLaunch.from_cache(launch_id, request, tool_conf)

    if not message_launch.has_ags():
        raise Exception("Don't have grades!")

    sub = message_launch.get_launch_data().get('sub')
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000')

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
        raise Exception("Don't have names and roles!")

    if not message_launch.has_ags():
        raise Exception("Don't have grades!")

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
