
NameError at /gpt4/transferencias/397600/verificar/

name 'OTPChallenge' is not defined

Request Method: 	GET
Request URL: 	http://127.0.0.1:3000/gpt4/transferencias/397600/verificar/
Django Version: 	5.2.3
Exception Type: 	NameError
Exception Value: 	

name 'OTPChallenge' is not defined

Exception Location: 	/home/markmur88/Simulador/simulador_banco/banco/gpt_views.py, line 598, in get_context_data
Raised during: 	banco.gpt_views.TransferSCAView
Python Executable: 	/home/markmur88/envAPP/bin/python
Python Version: 	3.13.5
Python Path: 	

['/home/markmur88/Simulador/simulador_banco',
 '/usr/lib/python313.zip',
 '/usr/lib/python3.13',
 '/usr/lib/python3.13/lib-dynload',
 '/home/markmur88/envAPP/lib/python3.13/site-packages']

Server time: 	Mon, 21 Jul 2025 05:38:20 +0000
Traceback Switch to copy-and-paste view

    /home/markmur88/envAPP/lib/python3.13/site-packages/django/core/handlers/exception.py, line 55, in inner

                        response = get_response(request)
                                       ^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.13/site-packages/django/core/handlers/base.py, line 197, in _get_response

                        response = wrapped_callback(request, *callback_args, **callback_kwargs)
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.13/site-packages/django/views/generic/base.py, line 105, in view

                    return self.dispatch(request, *args, **kwargs)
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.13/site-packages/django/contrib/auth/mixins.py, line 73, in dispatch

                return super().dispatch(request, *args, **kwargs)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.13/site-packages/django/views/generic/base.py, line 144, in dispatch

                return handler(request, *args, **kwargs)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/envAPP/lib/python3.13/site-packages/django/views/generic/base.py, line 228, in get

                context = self.get_context_data(**kwargs)
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         …
    Local vars
    /home/markmur88/Simulador/simulador_banco/banco/gpt_views.py, line 598, in get_context_data

                context['otp_challenge'] = OTPChallenge.objects.filter(
                                                ^^^^^^^^^^^^

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

'.eJwNyzsKgDAMANCrhMwdih5EQbcqJZRUIv2ZqufXtz_n0Puz1-Iz904Ho7FmsAYXBuXrEVaGl1WiBAqyPdbGscC0ztBICULNLfFNCongVio9_qMEITSI-_4BQkwhEg:1udjEB:Ojg_pfkm7ZpDitXJD0gQkEnkseeXRNAYIQTvFmtbOio'

META
Variable 	Value
ALLOWED_HOSTS 	

'localhost,127.0.0.1,0.0.0.0,80.78.30.242,api.coretransapi.com'

API_PATH 	

'********************'

API_URL 	

'********************'

AUTHORIZE_PATH 	

'********************'

AUTHORIZE_URL 	

'********************'

AUTH_PATH 	

'********************'

AUTH_URL 	

'********************'

BASE_URL 	

'http://80.78.30.242:9181'

BUN_INSTALL 	

'/home/markmur88/.bun'

CLUTTER_IM_MODULE 	

'ibus'

COLORFGBG 	

'15;0'

COLORTERM 	

'truecolor'

COMMAND_NOT_FOUND_INSTALL_PROMPT 	

'1'

CONTENT_LENGTH 	

''

CONTENT_TYPE 	

'text/plain'

CSRF_COOKIE 	

'3qfK4ZdDyjhxWOKeKj4jEyeTk3iydAI0'

DBUS_SESSION_BUS_ADDRESS 	

'unix:path=/run/user/1000/bus'

DEBUG 	

'True'

DESKTOP_SESSION 	

'lightdm-xsession'

DISPLAY 	

':0.0'

DJANGO_SECRET_KEY 	

'********************'

DJANGO_SETTINGS_MODULE 	

'simulador_banco.settings'

DOTNET_CLI_TELEMETRY_OPTOUT 	

'1'

GATEWAY_INTERFACE 	

'CGI/1.1'

GDMSESSION 	

'lightdm-xsession'

GTK_IM_MODULE 	

'ibus'

HOME 	

'/home/markmur88'

HTTP_ACCEPT 	

'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

HTTP_ACCEPT_ENCODING 	

'gzip, deflate, br, zstd'

HTTP_ACCEPT_LANGUAGE 	

'es-CO'

HTTP_CONNECTION 	

'keep-alive'

HTTP_COOKIE 	

'********************'

HTTP_DNT 	

'1'

HTTP_HOST 	

'127.0.0.1:3000'

HTTP_PRIORITY 	

'u=0, i'

HTTP_REFERER 	

'http://127.0.0.1:3000/gpt4/transferencias/nuevo/'

HTTP_SEC_FETCH_DEST 	

'document'

HTTP_SEC_FETCH_MODE 	

'navigate'

HTTP_SEC_FETCH_SITE 	

'same-origin'

HTTP_SEC_FETCH_USER 	

'?1'

HTTP_UPGRADE_INSECURE_REQUESTS 	

'1'

HTTP_USER_AGENT 	

'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'

JWT_SECRET_KEY 	

'********************'

LANG 	

'es_CO.UTF-8'

LANGUAGE 	

'es_CO:es'

LESS_TERMCAP_mb 	

'\x1b[1;31m'

LESS_TERMCAP_md 	

'\x1b[1;36m'

LESS_TERMCAP_me 	

'\x1b[0m'

LESS_TERMCAP_se 	

'\x1b[0m'

LESS_TERMCAP_so 	

'\x1b[01;33m'

LESS_TERMCAP_ue 	

'\x1b[0m'

LESS_TERMCAP_us 	

'\x1b[1;32m'

LOGNAME 	

'markmur88'

LS_COLORS 	

'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=00:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.7z=01;31:*.ace=01;31:*.alz=01;31:*.apk=01;31:*.arc=01;31:*.arj=01;31:*.bz=01;31:*.bz2=01;31:*.cab=01;31:*.cpio=01;31:*.crate=01;31:*.deb=01;31:*.drpm=01;31:*.dwm=01;31:*.dz=01;31:*.ear=01;31:*.egg=01;31:*.esd=01;31:*.gz=01;31:*.jar=01;31:*.lha=01;31:*.lrz=01;31:*.lz=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.lzo=01;31:*.pyz=01;31:*.rar=01;31:*.rpm=01;31:*.rz=01;31:*.sar=01;31:*.swm=01;31:*.t7z=01;31:*.tar=01;31:*.taz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tgz=01;31:*.tlz=01;31:*.txz=01;31:*.tz=01;31:*.tzo=01;31:*.tzst=01;31:*.udeb=01;31:*.war=01;31:*.whl=01;31:*.wim=01;31:*.xz=01;31:*.z=01;31:*.zip=01;31:*.zoo=01;31:*.zst=01;31:*.avif=01;35:*.jpg=01;35:*.jpeg=01;35:*.jxl=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:*~=00;90:*#=00;90:*.bak=00;90:*.crdownload=00;90:*.dpkg-dist=00;90:*.dpkg-new=00;90:*.dpkg-old=00;90:*.dpkg-tmp=00;90:*.old=00;90:*.orig=00;90:*.part=00;90:*.rej=00;90:*.rpmnew=00;90:*.rpmorig=00;90:*.rpmsave=00;90:*.swp=00;90:*.tmp=00;90:*.ucf-dist=00;90:*.ucf-new=00;90:*.ucf-old=00;90::ow=30;44:'

NMAP_PRIVILEGED 	

''

OLDPWD 	

'/home/markmur88/AI/nerd-dictation'

OPENAI_API_KEY 	

'********************'

OTP_PATH 	

'/otp/single'

OTP_URL 	

'http://80.78.30.242:9181/otp/single'

PANEL_GDK_CORE_DEVICE_EVENTS 	

'0'

PATH 	

'/home/markmur88/envAPP/bin:/home/markmur88/.bun/bin:/home/markmur88/.bun/bin:/home/markmur88/.bun/bin:/home/markmur88/.bun/bin:/home/markmur88/.bun/bin:/home/markmur88/.bun/bin:/home/markmur88/.cargo/bin:/home/markmur88/.local/bin:/usr/share/pyenv/shims:/usr/share/pyenv/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/snap/bin:/home/markmur88/.dotnet/tools:/home/markmur88/.lmstudio/bin'

PATH_INFO 	

'/gpt4/transferencias/397600/verificar/'

POWERSHELL_TELEMETRY_OPTOUT 	

'1'

POWERSHELL_UPDATECHECK 	

'Off'

PWD 	

'/home/markmur88/Simulador/simulador_banco'

PYENV_ROOT 	

'/usr/share/pyenv'

QT_ACCESSIBILITY 	

'1'

QT_AUTO_SCREEN_SCALE_FACTOR 	

'0'

QT_IM_MODULE 	

'ibus'

QT_QPA_PLATFORMTHEME 	

'qt5ct'

QUERY_STRING 	

''

REMOTE_ADDR 	

'127.0.0.1'

REMOTE_HOST 	

''

REQUEST_METHOD 	

'GET'

RUN_MAIN 	

'true'

SCRIPT_NAME 	

''

SERVER_NAME 	

'localhost'

SERVER_PORT 	

'3000'

SERVER_PROTOCOL 	

'HTTP/1.1'

SERVER_SOFTWARE 	

'WSGIServer/0.2'

SESSION_MANAGER 	

'local/local:@/tmp/.ICE-unix/1708,unix/local:/tmp/.ICE-unix/1708,inet6/local:40779,inet/local:41025'

SHELL 	

'/usr/bin/zsh'

SHLVL 	

'1'

SIMULADOR_API_URL 	

'********************'

SIMULADOR_AUTHORIZE_URL 	

'********************'

SIMULADOR_AUTH_URL 	

'********************'

SIMULADOR_LOGIN_URL 	

'http://80.78.30.242:9181/api/login/'

SIMULADOR_OTP_URL 	

'http://localhost:3000/api/transferencia/otp/'

SIMULADOR_SECRET_KEY 	

'********************'

SIMULADOR_VERIFY_URL 	

'http://80.78.30.242:9181/api/transferencia/verify/'

SIMULATOR_NOTIFY_URL 	

'http://localhost/notify'

SSH_AGENT_PID 	

'1921'

SSH_AUTH_SOCK 	

'********************'

SSH_KEY 	

'********************'

TELEGRAM_BOT_TOKEN 	

'********************'

TELEGRAM_CHAT_ID 	

'769077177'

TERM 	

'xterm-256color'

TOKEN_PATH 	

'********************'

TOKEN_URL 	

'********************'

TOTP_SECRET 	

'********************'

TZ 	

'UTC'

USER 	

'markmur88'

VIRTUAL_ENV 	

'/home/markmur88/envAPP'

VIRTUAL_ENV_PROMPT 	

'envAPP'

VPS_API_DIR 	

'********************'

VPS_IP 	

'80.78.30.242'

VPS_PORT 	

'22'

VPS_SSH_KEY 	

'********************'

VPS_USER 	

'markmur88'

WINDOWID 	

'0'

XAUTHORITY 	

'********************'

XDG_CACHE_HOME 	

'/home/markmur88/.cache'

XDG_CONFIG_DIRS 	

'/etc/xdg'

XDG_CONFIG_HOME 	

'/home/markmur88/.config'

XDG_CURRENT_DESKTOP 	

'XFCE'

XDG_DATA_DIRS 	

'/usr/share/xfce4:/usr/share/gnome:/usr/local/share:/usr/share:/var/lib/snapd/desktop:/usr/share'

XDG_GREETER_DATA_DIR 	

'/var/lib/lightdm/data/markmur88'

XDG_MENU_PREFIX 	

'xfce-'

XDG_RUNTIME_DIR 	

'/run/user/1000'

XDG_SEAT 	

'seat0'

XDG_SEAT_PATH 	

'/org/freedesktop/DisplayManager/Seat0'

XDG_SESSION_CLASS 	

'user'

XDG_SESSION_DESKTOP 	

'lightdm-xsession'

XDG_SESSION_ID 	

'4'

XDG_SESSION_PATH 	

'/org/freedesktop/DisplayManager/Session0'

XDG_SESSION_TYPE 	

'x11'

XDG_VTNR 	

'7'

XMODIFIERS 	

'@im=ibus'

_ 	

'/home/markmur88/envAPP/bin/python'

wsgi.errors 	

<_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>

wsgi.file_wrapper 	

<class 'wsgiref.util.FileWrapper'>

wsgi.input 	

<django.core.handlers.wsgi.LimitedStream object at 0x7f4e9cd7e920>

wsgi.multiprocess 	

False

wsgi.multithread 	

True

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
 'banco.apps.BancoConfig']

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
 'formatters': {'debug': {'format': '[{levelname}] {message}', 'style': '{'},
                'simple': {'format': '[{levelname}] {asctime} {message}',
                           'style': '{'},
                'verbose': {'format': '{levelname} {asctime} {module} '
                                      '{process:d} {thread:d} {message}',
                            'style': '{'}},
 'handlers': {'console': {'class': 'logging.StreamHandler',
                          'formatter': 'debug',
                          'level': 'DEBUG'},
              'file': {'class': 'logging.FileHandler',
                       'filename': '/home/markmur88/Simulador/simulador_banco/debug.log',
                       'formatter': 'simple',
                       'level': 'DEBUG'}},
 'loggers': {'': {'handlers': ['console', 'file'], 'level': 'DEBUG'},
             'banco': {'handlers': ['console', 'file'],
                       'level': 'DEBUG',
                       'propagate': False},
             'django': {'handlers': ['console', 'file'],
                        'level': 'INFO',
                        'propagate': False},
             'services': {'handlers': ['console', 'file'],
                          'level': 'DEBUG',
                          'propagate': False}},
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
