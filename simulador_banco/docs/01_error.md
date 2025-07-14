                                                                                        
┌──(envAPP)─(markmur88㉿coretransapi)-[~/Simulador/simulador_banco]
└─$ d_mig
Traceback (most recent call last):
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/checks/urls.py", line 136, in check_custom_error_handlers
    handler = resolver.resolve_error_handler(status_code)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/resolvers.py", line 732, in resolve_error_handler
    callback = getattr(self.urlconf_module, "handler%s" % view_type, None)
                       ^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/utils/functional.py", line 47, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
    return import_module(self.urlconf_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/markmur88/Simulador/simulador_banco/simulador_banco/urls.py", line 23, in <module>
    path('', include('banco.urls')),
             ^^^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/conf.py", line 39, in include
    urlconf_module = import_module(urlconf_module)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/markmur88/Simulador/simulador_banco/banco/urls.py", line 7, in <module>
    from . import gpt_views
  File "/home/markmur88/Simulador/simulador_banco/banco/gpt_views.py", line 13, in <module>
    from django.db import ProtectedError
ImportError: cannot import name 'ProtectedError' from 'django.db' (/home/markmur88/envAPP/lib/python3.11/site-packages/django/db/__init__.py)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/markmur88/Simulador/simulador_banco/manage.py", line 22, in <module>
    main()
  File "/home/markmur88/Simulador/simulador_banco/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/management/base.py", line 416, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/management/base.py", line 457, in execute
    self.check(**check_kwargs)
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/management/base.py", line 492, in check
    all_issues = checks.run_checks(
                 ^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/checks/registry.py", line 89, in run_checks
    new_errors = check(app_configs=app_configs, databases=databases)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/core/checks/urls.py", line 138, in check_custom_error_handlers
    path = getattr(resolver.urlconf_module, "handler%s" % status_code)
                   ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/utils/functional.py", line 47, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
    return import_module(self.urlconf_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/markmur88/Simulador/simulador_banco/simulador_banco/urls.py", line 23, in <module>
    path('', include('banco.urls')),
             ^^^^^^^^^^^^^^^^^^^^^
  File "/home/markmur88/envAPP/lib/python3.11/site-packages/django/urls/conf.py", line 39, in include
    urlconf_module = import_module(urlconf_module)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/markmur88/Simulador/simulador_banco/banco/urls.py", line 7, in <module>
    from . import gpt_views
  File "/home/markmur88/Simulador/simulador_banco/banco/gpt_views.py", line 13, in <module>
    from django.db import ProtectedError
ImportError: cannot import name 'ProtectedError' from 'django.db' (/home/markmur88/envAPP/lib/python3.11/site-packages/django/db/__init__.py)
