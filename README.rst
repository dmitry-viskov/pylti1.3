LTI 1.3 Advantage Tool implementation in Python
===============================================

.. image:: https://img.shields.io/pypi/v/PyLTI1p3
    :scale: 100%
    :target: https://pypi.python.org/pypi/PyLTI1p3
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/PyLTI1p3
    :scale: 100%
    :target: https://www.python.org/
    :alt: Python

.. image:: https://travis-ci.org/dmitry-viskov/pylti1.3.svg?branch=master
    :scale: 100%
    :target: https://travis-ci.org/dmitry-viskov/pylti1.3
    :alt: Build Status

.. image:: https://img.shields.io/github/license/dmitry-viskov/pylti1.3
    :scale: 100%
    :target: https://raw.githubusercontent.com/dmitry-viskov/pylti1.3/master/LICENSE
    :alt: MIT


This project is a Python implementation of the similar `PHP tool`_.
Library contains adapter for usage from Django Web Framework but there is no difficult to adapt it to from other frameworks: you should just re-implement ``OIDCLogin`` and ``MessageLaunch`` classes as it already done for Django.

.. _PHP tool: https://github.com/IMSGlobal/lti-1-3-php-library

Example
=======

First of all choose and configure test LTI 1.3 Platform. It may be:

* `IMS Global test site`_
* `Canvas LMS`_ (Detailed `instruction`_ how to setup Canvas as LTI 1.3 Platform is `here`_)

.. _IMS Global test site: https://lti-ri.imsglobal.org
.. _Canvas LMS: https://github.com/instructure/canvas-lms
.. _instruction: https://github.com/dmitry-viskov/pylti1.3/wiki/Configure-Canvas-as-LTI-1.3-Platform
.. _here: https://github.com/dmitry-viskov/pylti1.3/wiki/Configure-Canvas-as-LTI-1.3-Platform

The most simple way to check example is to use ``docker`` + ``docker-compose``.
Change the necessary configs in the ``examples/configs/game.json`` (`here is instruction`_ how to generate your own public + private keys):

.. _here is instruction: https://github.com/dmitry-viskov/pylti1.3/wiki/How-to-generate-JWT-RS256-key-and-JWKS

.. code-block:: javascript

    {
        "<issuer>" : { // This will usually look something like 'http://example.com'
            "client_id" : "<client_id>", // This is the id received in the 'aud' during a launch
            "auth_login_url" : "<auth_login_url>", // The platform's OIDC login endpoint
            "auth_token_url" : "<auth_token_url>", // The platform's service authorization endpoint
            "key_set_url" : "<key_set_url>", // The platform's JWKS endpoint
            "key_set": null, // in case if platform's JWKS endpoint somehow unavailable you may paste JWKS here
            "private_key_file" : "<path_to_private_key>", // Relative path to the tool's private key
            "deployment_ids" : ["<deployment_id>"] // The deployment_id passed by the platform during launch
        }
    }

and execute:

.. code-block:: shell

    $ docker-compose up --build

You may use virtualenv instead of docker:

.. code-block:: shell

    $ virtualenv venv
    $ source venv/bin/activate
    $ cd examples
    $ pip install -r requirements.txt
    $ cd game
    $ python manage.py runserver 127.0.0.1:9001

Now there is game example tool you can launch into on the port 9001:

.. code-block:: shell

    OIDC Login URL: http://127.0.0.1:9001/login/
    LTI Launch URL: http://127.0.0.1:9001/launch/

Configuration & Usage
=====================

Accessing Registration Data
---------------------------

To configure your own tool you may use built-in adapters:

.. code-block:: python

    from pylti1p3.tool_config import
    tool_conf = ToolConfJsonFile('path/to/json')

    from pylti1p3.tool_config import ToolConfDict
    settings = {
        "<issuer_1>": { },
        "<issuer_2>": { }
    }
    private_key = '...'
    tool_conf = ToolConfDict(settings)
    tool_conf.set_private_key(iss, private_key)

or create your own implementation. The ``pylti1p3.tool_config.ToolConfAbstract`` interface must be fully implemented for this to work.

Open Id Connect Login Request
-----------------------------

LTI 1.3 uses a modified version of the OpenId Connect third party initiate login flow. This means that to do an LTI 1.3 launch, you must first receive a login initialization request and return to the platform.

To handle this request, you must first create a new ``OIDCLogin`` (or ``DjangoOIDCLogin``) object:

.. code-block:: python

    from pylti1p3.contrib.django import DjangoOIDCLogin

    oidc_login = DjangoOIDCLogin(request, tool_conf)

Now you must configure your login request with a return url (this must be preconfigured and white-listed on the tool).
If a redirect url is not given or the registration does not exist an ``pylti1p3.exception.OIDC_Exception`` will be thrown.

.. code-block:: python

    try:
        oidc_login.redirect(get_launch_url(request))
    except OIDC_Exception:
        # display error page
        log.error('Error doing OIDC login')

With the redirect, we can now redirect the user back to the tool.
There are three ways to do this:

This will add a HTTP 302 location header:

.. code-block:: python

    oidc_login.redirect(get_launch_url(request))

This will display some javascript to do the redirect instead of using a HTTP 302:

.. code-block:: python

    oidc_login.redirect(get_launch_url(request), js_redirect=True)

You can also get the url you need to redirect to, with all the necessary query parameters (if you would prefer to redirect in a custom way):

.. code-block:: python

    redirect_obj = oidc_login.get_redirect_object()
    redirect_url = redirect_obj.get_redirect_url()

Redirect is done, we can move onto the launch.

LTI Message Launches
--------------------

Now that we have done the OIDC log the platform will launch back to the tool. To handle this request, first we need to create a new ``MessageLaunch`` (or ``DjangoMessageLaunch``) object.

.. code-block:: python

    message_launch = DjangoMessageLaunch(request, tool_conf)

Once we have the message launch, we can validate it. Validation is transparent - it's done once before you try to access the message body:

.. code-block:: python

    try:
        launch_data = message_launch.get_launch_data()
    except LtiException:
        log.error('Launch validation failed')

You may do it more explicitly:

.. code-block:: python

    try:
        launch_data = message_launch.set_auto_validation(enable=False).validate()
    except LtiException:
        log.error('Launch validation failed')

Now we know the launch is valid we can find out more information about the launch.

Check if we have a resource launch or a deep linking launch:

.. code-block:: python

    if message_launch.is_resource_launch():
        # Resource Launch!
    elif message_launch.is_deep_link_launch():
        # Deep Linking Launch!
    else:
        # Unknown launch type

Check which services we have access to:

.. code-block:: python

    if message_launch.has_ags():
        # Has Assignments and Grades Service
    if message_launch.has_nrps():
        # Has Names and Roles Service

Accessing Cached Launch Requests
--------------------------------

It is likely that you will want to refer back to a launch later during subsequent requests. This is done using the launch id to identify a cached request. The launch id can be found using:

.. code-block:: python

    launch_id = message_launch.get_launch_id()

Once you have the launch id, you can link it to your session and pass it along as a query parameter.

**Make sure you check the launch id against the user session to prevent someone from making actions on another person's launch.**

Retrieving a launch using the launch id can be done using:

.. code-block:: python

    message_launch = DjangoMessageLaunch.from_cache(launch_id, request, tool_conf)

Once retrieved, you can call any of the methods on the launch object as normal, e.g.

.. code-block:: python

    if message_launch.has_ags():
        # Has Assignments and Grades Service

Deep Linking Responses
----------------------

If you receive a deep linking launch, it is very likely that you are going to want to respond to the deep linking request with resources for the platform.

To create a deep link response you will need to get the deep link for the current launch:

.. code-block:: python

    deep_link = message_launch.get_deep_link()

Now we need to create ``pylti1p3.deep_link_resource.DeepLinkResource`` to return:

.. code-block:: python

    resource = DeepLinkResource()
    resource.set_url("https://my.tool/launch")\
        .set_custom_params({'my_param': my_param})\
        .set_title('My Resource')

Everything is set to return the resource to the platform. There are two methods of doing this.

The following method will output the html for an aut-posting form for you.

.. code-block:: python

    deep_link.output_response_form([resource1, resource2])

Alternatively you can just request the signed JWT that will need posting back to the platform by calling.

.. code-block:: python

    deep_link.get_response_jwt([resource1, resource2])

Names and Roles Service
-----------------------

Before using names and roles you should check that you have access to it:

.. code-block:: python

    if not message_launch.has_nrps():
        raise Exception("Don't have names and roles!")

Once we know we can access it, we can get an instance of the service from the launch.

.. code-block:: python

    nrps = message_launch.get_nrps()

From the service we can get list of all members by calling:

.. code-block:: python

    members = nrps.get_members()

Assignments and Grades Service
------------------------------

Before using assignments and grades you should check that you have access to it:

.. code-block:: python

    if not launch.has_ags():
        raise Exception("Don't have assignments and grades!")

Once we know we can access it, we can get an instance of the service from the launch:

.. code-block:: python

    ags = launch.get_ags()

To pass a grade back to the platform, you will need to create a ``pylti1p3.grade.Grade`` object and populate it with the necessary information:

.. code-block:: python

    gr = Grade()
    gr.set_score_given(earned_score)\
         .set_score_maximum(100)\
         .set_timestamp(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000'))\
         .set_activity_progress('Completed')\
         .set_grading_progress('FullyGraded')\
         .set_user_id(external_user_id)

To send the grade to the platform we can call:

.. code-block:: python

    ags.put_grade(gr)

This will put the grade into the default provided lineitem. If no default lineitem exists it will create one.

If you want to send multiple types of grade back, that can be done by specifying a ``pylti1p3.lineitem.LineItem``:

.. code-block:: python

    line_item = LineItem()
    line_item.set_tag('grade')\
        .set_score_maximum(100)\
        .set_label('Grade')

    ags.put_grade(gr, line_item);

If a lineitem with the same ``tag`` exists, that lineitem will be used, otherwise a new lineitem will be created.
