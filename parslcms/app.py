import os
from functools import wraps

from parsl.app.app import python_app, bash_app
from parsl.data_provider.files import File


def cmssw_bash_app(function=None, cache=False, executors='all'):
    import os
    import parslcms.data
    import random
    import string

    wrapper = os.path.join(parslcms.data.__path__[0], 'wrapper.sh')
    builder = os.path.join(parslcms.data.__path__[0], 'vc3-builder')
    install = '{}/.parslcms'.format(os.environ['HOME'])
    distfiles = '{}/.parslcms/vc3-distfiles'.format(os.environ['HOME'])

    def decorator(func):
        wdir = '{}/.parslcms/{}'.format(
            os.environ['HOME'],
            'tasks/{}_{}'.format(
                func.__name__,
                ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8)))
        )
        @wraps(func)
        def w(*args, **kwargs):

            # print('submitting: {}'.format(' '.join([str(x) for x in args])))

            prologue = [
                builder,
                '--install {}'.format(install),
                '--distfiles {}'.format(distfiles),
                '--require cvmfs',
                '--home {}'.format(wdir),
                '--require-os centos:v6.9:v6.9'
            ]
            rename = kwargs.get('rename', [])
            outputs = kwargs.get('outputs', [])
            epilogue = []
            for output in outputs:
                epilogue += ["mkdir -p `dirname {}`".format(output)]
            for source, destination in [x.split('->') for x in rename]:
                epilogue += ["cp {}/{} {}".format(wdir, source, destination)]

            return '{} {} "{}" {}'.format(' '.join(prologue), wrapper, func(*args, **kwargs), '; ' + '; '.join(epilogue))
        return bash_app(
            data_flow_kernel=None,
            walltime=None,
            cache=cache,
            executors=executors)(w)
    if function is not None:
        return decorator(function)
    return decorator

