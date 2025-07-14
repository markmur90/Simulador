
NoReverseMatch at /gpt4/deudores/1/

Reverse for 'account_statement_pdfGPT4' not found. 'account_statement_pdfGPT4' is not a valid view function or pattern name.

Request Method: 	GET
Request URL: 	http://80.78.30.242:9181/gpt4/deudores/1/
Django Version: 	5.2
Exception Type: 	NoReverseMatch
Exception Value: 	

Reverse for 'account_statement_pdfGPT4' not found. 'account_statement_pdfGPT4' is not a valid view function or pattern name.

Exception Location: 	/home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/resolvers.py, line 831, in _reverse_with_prefix
Raised during: 	banco.gpt_views.DebtorDetailView
Python Executable: 	/home/markmur88/envAPP/bin/python3
Python Version: 	3.11.2
Python Path: 	

['/home/markmur88/Simulador/simulador_banco',
 '/home/markmur88/Simulador/simulador_banco',
 '/home/markmur88/Simulador',
 '/home/markmur88/envAPP/bin',
 '/usr/lib/python311.zip',
 '/usr/lib/python3.11',
 '/usr/lib/python3.11/lib-dynload',
 '/home/markmur88/envAPP/lib/python3.11/site-packages']

Server time: 	Mon, 14 Jul 2025 00:32:39 +0000
Error during template rendering

In template /home/markmur88/Simulador/simulador_banco/banco/templates/api/GPT4/debtor_detail.html, error at line 58
Reverse for 'account_statement_pdfGPT4' not found. 'account_statement_pdfGPT4' is not a valid view function or pattern name.
48 	    <div class="card-body custom-card-body">
49 	      {% for account in accounts %}
50 	      <div class="card mb-3">
51 	        <div class="card-body">
52 	          <div class="d-flex justify-content-between align-items-center">
53 	            <div>
54 	              <h5 class="card-title">{{ account.iban }}</h5>
55 	              <h6 class="card-subtitle mb-2 text-muted">Saldo: {{ account.balance }} {{ account.currency }}</h6>
56 	            </div>
57 	            <div class="btn-group">
58 	              <a href="{% url 'account_statement_pdfGPT4' account.id %}" class="btn btn-outline-primary">
59 	                <i class="bi bi-file-earmark-pdf"></i> Estado de Cuenta
60 	              </a>
61 	              <button type="button" class="btn btn-outline-primary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown">
62 	                <span class="visually-hidden">Toggle Dropdown</span>
63 	              </button>
64 	              <ul class="dropdown-menu">
65 	                <li>
66 	                  <a class="dropdown-item" href="{% url 'account_statement_pdfGPT4' account.id %}?start={{ today|date:'Y-m-d' }}&end={{ today|date:'Y-m-d' }}">
67 	                    <i class="bi bi-calendar-day"></i> Movimientos de Hoy
68 	                  </a>
Traceback Switch to copy-and-paste view

    /home/markmur88/envAPP/lib/python3.11/site-packages/django/core/handlers/exception.py, line 55, in inner

                        response = get_response(request)
                                       ^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/core/handlers/base.py, line 220, in _get_response

                        response = response.render()
                                        ^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/response.py, line 114, in render

                    self.content = self.rendered_content
                                        ^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/response.py, line 92, in rendered_content

                return template.render(context, self._request)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/backends/django.py, line 107, in render

                    return self.template.render(context)
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 171, in render

                            return self._render(context)
                                        ^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 163, in _render

                return self.nodelist.render(context)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 1016, in render

                return SafeString("".join([node.render_annotated(context) for node in self]))
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 1016, in <listcomp>

                return SafeString("".join([node.render_annotated(context) for node in self]))
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 977, in render_annotated

                    return self.render(context)
                                ^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/loader_tags.py, line 159, in render

                    return compiled_parent._render(context)
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 163, in _render

                return self.nodelist.render(context)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 1016, in render

                return SafeString("".join([node.render_annotated(context) for node in self]))
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 1016, in <listcomp>

                return SafeString("".join([node.render_annotated(context) for node in self]))
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 977, in render_annotated

                    return self.render(context)
                                ^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/loader_tags.py, line 65, in render

                        result = block.nodelist.render(context)
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 1016, in render

                return SafeString("".join([node.render_annotated(context) for node in self]))
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 1016, in <listcomp>

                return SafeString("".join([node.render_annotated(context) for node in self]))
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 977, in render_annotated

                    return self.render(context)
                                ^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/defaulttags.py, line 243, in render

                            nodelist.append(node.render_annotated(context))
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/base.py, line 977, in render_annotated

                    return self.render(context)
                                ^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/template/defaulttags.py, line 480, in render

                    url = reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/base.py, line 98, in reverse

            resolved_url = resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/resolvers.py, line 831, in _reverse_with_prefix

                raise NoReverseMatch(msg)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars

Request information
USER

markmur88
GET

No GET data
POST

No POST data
FILES

No FILES data
COOKIES
Variable 	Value
csrftoken 	

'********************'

sessionid 	

'********************'

messages 	

'.eJzVzLEKwjAQgOFXCbd0OSRKXdykuDu4xRCO9JSIvZS7WHx8i2_g6PgP_xcCpPSwKmliM7ozoMfdHuGiJHZjZcmFXFamkRy_S6tGE0vjDSBAxP_4WZbyA9B7hNCdrNFYXZHl-vKet8-y1kxKbtaa2UgP7jgM5y5-pfgB-HVwGw:1ub6AF:bzeno6cwxKAtCYBll8TaZyxTJ7TreIvmfFirwYxtj0s'

META
Variable 	Value
CSRF_COOKIE 	

's5K7KOwzpCg0d9vee6Y6kvwIpdHm55tp'

HTTP_ACCEPT 	

'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

HTTP_ACCEPT_ENCODING 	

'gzip, deflate'

HTTP_ACCEPT_LANGUAGE 	

'es-CO'

HTTP_CONNECTION 	

'keep-alive'

HTTP_COOKIE 	

'********************'

HTTP_DNT 	

'1'

HTTP_HOST 	

'80.78.30.242:9181'

HTTP_PRIORITY 	

'u=0, i'

HTTP_REFERER 	

'http://80.78.30.242:9181/gpt4/deudores/'

HTTP_UPGRADE_INSECURE_REQUESTS 	

'1'

HTTP_USER_AGENT 	

'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'

PATH_INFO 	

'/gpt4/deudores/1/'

QUERY_STRING 	

''

RAW_URI 	

'/gpt4/deudores/1/'

REMOTE_ADDR 	

'149.88.24.201'

REMOTE_PORT 	

'44558'

REQUEST_METHOD 	

'GET'

SCRIPT_NAME 	

''

SERVER_NAME 	

'0.0.0.0'

SERVER_PORT 	

'9181'

SERVER_PROTOCOL 	

'HTTP/1.1'

SERVER_SOFTWARE 	

'gunicorn/23.0.0'

gunicorn.socket 	

<socket.socket fd=3, family=2, type=1, proto=0, laddr=('80.78.30.242', 9181), raddr=('149.88.24.201', 44558)>

wsgi.errors 	

<gunicorn.http.wsgi.WSGIErrorsWrapper object at 0x7f8b95006ce0>

wsgi.file_wrapper 	

<class 'gunicorn.http.wsgi.FileWrapper'>

wsgi.input 	

<gunicorn.http.body.Body object at 0x7f8b950a4310>

wsgi.input_terminated 	

True

wsgi.multiprocess 	

True

wsgi.multithread 	

False

wsgi.run_once 	

False

wsgi.url_scheme 	

'http'

wsgi.version 	

(1, 0)

Settings
Using settings module simulador_banco.settings
Setting 	Value
ABSOLUTE_URL_OVERRIDES 	

{}

ADMINS 	

[]

ALLOWED_HOSTS 	

['localhost', '127.0.0.1', '0.0.0.0', '80.78.30.242']

APPEND_SLASH 	

True

AUTHENTICATION_BACKENDS 	

'********************'

AUTH_PASSWORD_VALIDATORS 	

'********************'

AUTH_USER_MODEL 	

'********************'

BASE_DIR 	

PosixPath('/home/markmur88/Simulador/simulador_banco')

CACHES 	

{'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

CACHE_MIDDLEWARE_ALIAS 	

'default'

CACHE_MIDDLEWARE_KEY_PREFIX 	

'********************'

CACHE_MIDDLEWARE_SECONDS 	

600

CSRF_COOKIE_AGE 	

31449600

CSRF_COOKIE_DOMAIN 	

None

CSRF_COOKIE_HTTPONLY 	

False

CSRF_COOKIE_NAME 	

'csrftoken'

CSRF_COOKIE_PATH 	

'/'

CSRF_COOKIE_SAMESITE 	

'Lax'

CSRF_COOKIE_SECURE 	

False

CSRF_FAILURE_VIEW 	

'django.views.csrf.csrf_failure'

CSRF_HEADER_NAME 	

'HTTP_X_CSRFTOKEN'

CSRF_TRUSTED_ORIGINS 	

[]

CSRF_USE_SESSIONS 	

False

DATABASES 	

{'default': {'ATOMIC_REQUESTS': False,
             'AUTOCOMMIT': True,
             'CONN_HEALTH_CHECKS': False,
             'CONN_MAX_AGE': 0,
             'ENGINE': 'django.db.backends.sqlite3',
             'HOST': '',
             'NAME': PosixPath('/home/markmur88/Simulador/simulador_banco/db.sqlite3'),
             'OPTIONS': {},
             'PASSWORD': '********************',
             'PORT': '',
             'TEST': {'CHARSET': None,
                      'COLLATION': None,
                      'MIGRATE': True,
                      'MIRROR': None,
                      'NAME': None},
             'TIME_ZONE': None,
             'USER': ''}}

DATABASE_ROUTERS 	

[]

DATA_UPLOAD_MAX_MEMORY_SIZE 	

2621440

DATA_UPLOAD_MAX_NUMBER_FIELDS 	

1000

DATA_UPLOAD_MAX_NUMBER_FILES 	

100

DATETIME_FORMAT 	

'N j, Y, P'

DATETIME_INPUT_FORMATS 	

['%Y-%m-%d %H:%M:%S',
 '%Y-%m-%d %H:%M:%S.%f',
 '%Y-%m-%d %H:%M',
 '%m/%d/%Y %H:%M:%S',
 '%m/%d/%Y %H:%M:%S.%f',
 '%m/%d/%Y %H:%M',
 '%m/%d/%y %H:%M:%S',
 '%m/%d/%y %H:%M:%S.%f',
 '%m/%d/%y %H:%M']

DATE_FORMAT 	

'N j, Y'

DATE_INPUT_FORMATS 	

['%Y-%m-%d',
 '%m/%d/%Y',
 '%m/%d/%y',
 '%b %d %Y',
 '%b %d, %Y',
 '%d %b %Y',
 '%d %b, %Y',
 '%B %d %Y',
 '%B %d, %Y',
 '%d %B %Y',
 '%d %B, %Y']

DEBUG 	

True

DEBUG_PROPAGATE_EXCEPTIONS 	

False

DECIMAL_SEPARATOR 	

'.'

DEFAULT_AUTO_FIELD 	

'django.db.models.BigAutoField'

DEFAULT_CHARSET 	

'utf-8'

DEFAULT_EXCEPTION_REPORTER 	

'django.views.debug.ExceptionReporter'

DEFAULT_EXCEPTION_REPORTER_FILTER 	

'django.views.debug.SafeExceptionReporterFilter'

DEFAULT_FROM_EMAIL 	

'webmaster@localhost'

DEFAULT_INDEX_TABLESPACE 	

''

DEFAULT_TABLESPACE 	

''

DISALLOWED_USER_AGENTS 	

[]

EMAIL_BACKEND 	

'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST 	

'localhost'

EMAIL_HOST_PASSWORD 	

'********************'

EMAIL_HOST_USER 	

''

EMAIL_PORT 	

25

EMAIL_SSL_CERTFILE 	

None

EMAIL_SSL_KEYFILE 	

'********************'

EMAIL_SUBJECT_PREFIX 	

'[Django] '

EMAIL_TIMEOUT 	

None

EMAIL_USE_LOCALTIME 	

False

EMAIL_USE_SSL 	

False

EMAIL_USE_TLS 	

False

FIELD_ENCRYPTION_FALLBACK_KEYS 	

'********************'

FIELD_ENCRYPTION_KEY 	

'********************'

FIELD_ENCRYPTION_KEYS 	

'********************'

FILE_UPLOAD_DIRECTORY_PERMISSIONS 	

None

FILE_UPLOAD_HANDLERS 	

['django.core.files.uploadhandler.MemoryFileUploadHandler',
 'django.core.files.uploadhandler.TemporaryFileUploadHandler']

FILE_UPLOAD_MAX_MEMORY_SIZE 	

2621440

FILE_UPLOAD_PERMISSIONS 	

420

FILE_UPLOAD_TEMP_DIR 	

None

FIRST_DAY_OF_WEEK 	

0

FIXTURE_DIRS 	

[]

FORCE_SCRIPT_NAME 	

None

FORMAT_MODULE_PATH 	

None

FORMS_URLFIELD_ASSUME_HTTPS 	

False

FORM_RENDERER 	

'django.forms.renderers.DjangoTemplates'

IGNORABLE_404_URLS 	

[]

INSTALLED_APPS 	

['django.contrib.staticfiles',
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'banco.apps.BancoConfig',
 'django_bootstrap5']

INTERNAL_IPS 	

[]

JWT_SECRET_KEY 	

'********************'

LANGUAGES 	

[('af', 'Afrikaans'),
 ('ar', 'Arabic'),
 ('ar-dz', 'Algerian Arabic'),
 ('ast', 'Asturian'),
 ('az', 'Azerbaijani'),
 ('bg', 'Bulgarian'),
 ('be', 'Belarusian'),
 ('bn', 'Bengali'),
 ('br', 'Breton'),
 ('bs', 'Bosnian'),
 ('ca', 'Catalan'),
 ('ckb', 'Central Kurdish (Sorani)'),
 ('cs', 'Czech'),
 ('cy', 'Welsh'),
 ('da', 'Danish'),
 ('de', 'German'),
 ('dsb', 'Lower Sorbian'),
 ('el', 'Greek'),
 ('en', 'English'),
 ('en-au', 'Australian English'),
 ('en-gb', 'British English'),
 ('eo', 'Esperanto'),
 ('es', 'Spanish'),
 ('es-ar', 'Argentinian Spanish'),
 ('es-co', 'Colombian Spanish'),
 ('es-mx', 'Mexican Spanish'),
 ('es-ni', 'Nicaraguan Spanish'),
 ('es-ve', 'Venezuelan Spanish'),
 ('et', 'Estonian'),
 ('eu', 'Basque'),
 ('fa', 'Persian'),
 ('fi', 'Finnish'),
 ('fr', 'French'),
 ('fy', 'Frisian'),
 ('ga', 'Irish'),
 ('gd', 'Scottish Gaelic'),
 ('gl', 'Galician'),
 ('he', 'Hebrew'),
 ('hi', 'Hindi'),
 ('hr', 'Croatian'),
 ('hsb', 'Upper Sorbian'),
 ('hu', 'Hungarian'),
 ('hy', 'Armenian'),
 ('ia', 'Interlingua'),
 ('id', 'Indonesian'),
 ('ig', 'Igbo'),
 ('io', 'Ido'),
 ('is', 'Icelandic'),
 ('it', 'Italian'),
 ('ja', 'Japanese'),
 ('ka', 'Georgian'),
 ('kab', 'Kabyle'),
 ('kk', 'Kazakh'),
 ('km', 'Khmer'),
 ('kn', 'Kannada'),
 ('ko', 'Korean'),
 ('ky', 'Kyrgyz'),
 ('lb', 'Luxembourgish'),
 ('lt', 'Lithuanian'),
 ('lv', 'Latvian'),
 ('mk', 'Macedonian'),
 ('ml', 'Malayalam'),
 ('mn', 'Mongolian'),
 ('mr', 'Marathi'),
 ('ms', 'Malay'),
 ('my', 'Burmese'),
 ('nb', 'Norwegian Bokmål'),
 ('ne', 'Nepali'),
 ('nl', 'Dutch'),
 ('nn', 'Norwegian Nynorsk'),
 ('os', 'Ossetic'),
 ('pa', 'Punjabi'),
 ('pl', 'Polish'),
 ('pt', 'Portuguese'),
 ('pt-br', 'Brazilian Portuguese'),
 ('ro', 'Romanian'),
 ('ru', 'Russian'),
 ('sk', 'Slovak'),
 ('sl', 'Slovenian'),
 ('sq', 'Albanian'),
 ('sr', 'Serbian'),
 ('sr-latn', 'Serbian Latin'),
 ('sv', 'Swedish'),
 ('sw', 'Swahili'),
 ('ta', 'Tamil'),
 ('te', 'Telugu'),
 ('tg', 'Tajik'),
 ('th', 'Thai'),
 ('tk', 'Turkmen'),
 ('tr', 'Turkish'),
 ('tt', 'Tatar'),
 ('udm', 'Udmurt'),
 ('ug', 'Uyghur'),
 ('uk', 'Ukrainian'),
 ('ur', 'Urdu'),
 ('uz', 'Uzbek'),
 ('vi', 'Vietnamese'),
 ('zh-hans', 'Simplified Chinese'),
 ('zh-hant', 'Traditional Chinese')]

LANGUAGES_BIDI 	

['he', 'ar', 'ar-dz', 'ckb', 'fa', 'ug', 'ur']

LANGUAGE_CODE 	

'en-us'

LANGUAGE_COOKIE_AGE 	

None

LANGUAGE_COOKIE_DOMAIN 	

None

LANGUAGE_COOKIE_HTTPONLY 	

False

LANGUAGE_COOKIE_NAME 	

'django_language'

LANGUAGE_COOKIE_PATH 	

'/'

LANGUAGE_COOKIE_SAMESITE 	

None

LANGUAGE_COOKIE_SECURE 	

False

LOCALE_PATHS 	

[]

LOGGING 	

{'disable_existing_loggers': False,
 'handlers': {'console': {'class': 'logging.StreamHandler'}},
 'loggers': {'simulador_banco.middleware.allow_internal_network': {'handlers': ['console'],
                                                                   'level': 'WARNING'}},
 'version': 1}

LOGGING_CONFIG 	

'logging.config.dictConfig'

LOGIN_REDIRECT_URL 	

'/accounts/profile/'

LOGIN_URL 	

'/login/'

LOGOUT_REDIRECT_URL 	

None

MANAGERS 	

[]

MEDIA_ROOT 	

'/home/markmur88/Simulador/simulador_banco/media'

MEDIA_URL 	

'/media/'

MESSAGE_STORAGE 	

'django.contrib.messages.storage.fallback.FallbackStorage'

MIDDLEWARE 	

['django.middleware.security.SecurityMiddleware',
 'simulador_banco.middleware.jwt_auth.JWTAuthenticationMiddleware',
 'whitenoise.middleware.WhiteNoiseMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']

MIGRATION_MODULES 	

{}

MONTH_DAY_FORMAT 	

'F j'

NUMBER_GROUPING 	

0

OPENAI_API_KEY 	

'********************'

PASSWORD_HASHERS 	

'********************'

PASSWORD_RESET_TIMEOUT 	

'********************'

PREPEND_WWW 	

False

ROOT_URLCONF 	

'simulador_banco.urls'

SECRET_KEY 	

'********************'

SECRET_KEY_FALLBACKS 	

'********************'

SECURE_CONTENT_TYPE_NOSNIFF 	

True

SECURE_CROSS_ORIGIN_OPENER_POLICY 	

'same-origin'

SECURE_HSTS_INCLUDE_SUBDOMAINS 	

False

SECURE_HSTS_PRELOAD 	

False

SECURE_HSTS_SECONDS 	

0

SECURE_PROXY_SSL_HEADER 	

None

SECURE_REDIRECT_EXEMPT 	

[]

SECURE_REFERRER_POLICY 	

'same-origin'

SECURE_SSL_HOST 	

None

SECURE_SSL_REDIRECT 	

False

SERVER_EMAIL 	

'root@localhost'

SESSION_CACHE_ALIAS 	

'default'

SESSION_COOKIE_AGE 	

1209600

SESSION_COOKIE_DOMAIN 	

None

SESSION_COOKIE_HTTPONLY 	

True

SESSION_COOKIE_NAME 	

'sessionid'

SESSION_COOKIE_PATH 	

'/'

SESSION_COOKIE_SAMESITE 	

'Lax'

SESSION_COOKIE_SECURE 	

False

SESSION_ENGINE 	

'django.contrib.sessions.backends.db'

SESSION_EXPIRE_AT_BROWSER_CLOSE 	

False

SESSION_FILE_PATH 	

None

SESSION_SAVE_EVERY_REQUEST 	

False

SESSION_SERIALIZER 	

'django.contrib.sessions.serializers.JSONSerializer'

SETTINGS_MODULE 	

'simulador_banco.settings'

SHORT_DATETIME_FORMAT 	

'm/d/Y P'

SHORT_DATE_FORMAT 	

'm/d/Y'

SIGNING_BACKEND 	

'django.core.signing.TimestampSigner'

SILENCED_SYSTEM_CHECKS 	

[]

SIMULADOR_API_URL 	

'********************'

SIMULADOR_TOKEN_URL 	

'********************'

SIMULADOR_VERIFY_URL 	

'http://80.78.30.242:9181/api/transferencia/verify/'

SIMULATOR_NOTIFY_URL 	

'http://localhost/notify'

STATICFILES_DIRS 	

[PosixPath('/home/markmur88/Simulador/simulador_banco/static')]

STATICFILES_FINDERS 	

['django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.AppDirectoriesFinder']

STATICFILES_STORAGE 	

'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT 	

PosixPath('/home/markmur88/Simulador/simulador_banco/staticfiles')

STATIC_URL 	

'/static/'

STORAGES 	

{'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
 'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}}

TELEGRAM_BOT_TOKEN 	

'********************'

TELEGRAM_CHAT_ID 	

'769077177'

TEMPLATES 	

[{'APP_DIRS': True,
  'BACKEND': 'django.template.backends.django.DjangoTemplates',
  'DIRS': [PosixPath('/home/markmur88/Simulador/simulador_banco/templates')],
  'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                     'django.template.context_processors.request',
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages']}}]

TEST_NON_SERIALIZED_APPS 	

[]

TEST_RUNNER 	

'django.test.runner.DiscoverRunner'

THOUSAND_SEPARATOR 	

','

TIME_FORMAT 	

'P'

TIME_INPUT_FORMATS 	

['%H:%M:%S', '%H:%M:%S.%f', '%H:%M']

TIME_ZONE 	

'UTC'

TOTP_SECRET 	

'********************'

USE_I18N 	

True

USE_THOUSAND_SEPARATOR 	

False

USE_TZ 	

True

USE_X_FORWARDED_HOST 	

False

USE_X_FORWARDED_PORT 	

False

WSGI_APPLICATION 	

'simulador_banco.wsgi.application'

X_FRAME_OPTIONS 	

'DENY'

YEAR_MONTH_FORMAT 	

'F Y'

_DEFAULT_FALLBACK 	

'DbQG9CWLvBRa8Iu9pv9fJDVURCdKYQQErlZ9oCYGsY8='

You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard page generated by the handler for this status code.
