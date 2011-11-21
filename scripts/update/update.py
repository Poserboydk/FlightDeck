import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commander.deploy import hostgroups, task

import commander_settings as settings


_src_dir = lambda *p: os.path.join(settings.SRC_DIR, *p)


def manage_cmd(ctx, command):
    """Call a manage.py command."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("python2.6 manage.py %s" % command)


@task
def schematic(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("python2.6 ./vendor/src/schematic/schematic migrations")


@task
def update_code(ctx, ref):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("git fetch && git fetch -t")
        ctx.local("git checkout -f %s" % ref)
        ctx.local("git submodule sync")
        # submodule sync doesn't do --recursive yet.
        with ctx.lcd("vendor"):
            ctx.local("git submodule sync")
        ctx.local("git submodule update --init --recursive")


@task
def update_info(ctx, ref):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("git status")
        ctx.local("git log -1")
        ctx.local("/bin/bash -c 'source /etc/bash_completion.d/git && __git_ps1'")
        ctx.local('git show -s {0} --pretty="format:%h" > media/git-rev.txt'.format(ref))


@task
def checkin_changes(ctx):
    ctx.local("/usr/bin/rsync -aq --exclude '.git*' --delete %s/ %s/" % (settings.SRC_DIR, settings.WWW_DIR))


@task
def disable_cron(ctx):
    ctx.local("rm -f /etc/cron.d/%s" % settings.CRON_NAME)


@task
def install_cron(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('python2.6 ./scripts/crontab/gen-cron.py -w %s -u apache > /etc/cron.d/.%s' %
                  (settings.SRC_DIR, settings.CRON_NAME))
        ctx.local('mv /etc/cron.d/.%s /etc/cron.d/%s' % (settings.CRON_NAME, settings.CRON_NAME))


@hostgroups(settings.WEB_HOSTGROUP, remote_kwargs={'ssh_key': settings.SSH_KEY})
def deploy_app(ctx):
    ctx.remote(settings.REMOTE_UPDATE_SCRIPT)
    ctx.remote("/bin/touch %s" % settings.REMOTE_WSGI)


@hostgroups(settings.CELERY_HOSTGROUP, remote_kwargs={'ssh_key': settings.SSH_KEY})
def update_celery(ctx):
    ctx.remote(settings.REMOTE_UPDATE_SCRIPT)
    ctx.remote("/sbin/service %s restart" % settings.CELERY_SERVICE_PREFIX)
    ctx.remote("/sbin/service %s-bulk restart" % settings.CELERY_SERVICE_PREFIX)


_shipyard_cmd = 'node ./media/lib/shipyard/bin/shipyard build %s -d ./media/jetpack/js/ide'


@task
def shipyard_min(ctx):
    manage_cmd(ctx, 'cache_bust')
    minify = '--non-minify' if getattr(settings, 'BUILDER_DEV', False) else '--minify'
    with ctx.lcd(settings.SRC_DIR):
        ctx.local(_shipyard_cmd % minify)


@task
def deploy(ctx):
    install_cron()
    checkin_changes()
    deploy_app()
    update_celery()


@task
def pre_update(ctx, ref=settings.UPDATE_REF):
    ctx.local('date')
    disable_cron()
    update_code(ref)
    update_info(ref)


@task
def update(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("rm `find . -name '*.pyc'`")
    schematic()
    shipyard_min()

    # Run management commands like this:
    # manage_cmd(ctx, 'cmd')
