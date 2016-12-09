from fabric.api import task, env, run, sudo, cd, local, put, execute
from fabric.contrib.files import upload_template, exists
from os.path import join

GIT_REPO = 'git@github.com:binder-cms/binder-site.git'


@task
def live():
    """
    Run subsequent tasks on the live environment.
    """
    env.forward_agent = True
    env.use_ssh_config = True
    env.hosts = ['dinky']
    env.basedir = '/home/ianfp'
    env.appdir = join(env.basedir, 'binder-site')


@task
def setup():
    """
    Full remote system setup.
    """
    execute(clone)
    execute(composer)
    execute(cache)
    execute(apache)


@task()
def apache():
    """
    Configure apache2.
    """
    install_packages('apache2 libapache2-mod-php5')
    upload_template(
        filename='apache2.conf.template',
        destination='/etc/apache2/sites-enabled/binder-site.conf',
        use_sudo=True,
        context={'appdir': env.appdir})
    sudo('apache2ctl restart')


@task
def clone():
    """
    Clone this repo on the remote system, or update it if it already exists.
    """
    install_packages('git')
    if exists(env.appdir):
        execute(update)
    else:
        with cd(env.basedir):
            run('git clone {}'.format(GIT_REPO))


@task
def update():
    """
    Pull the latest changes to the repository.
    """
    with cd(env.appdir):
        run('git fetch --prune')
        run('git reset --hard origin/master')


@task
def composer():
    """
    Install PHP Composer.
    """
    install_packages('php5-cli')
    with cd(env.appdir):
        if not exists(join(env.appdir, 'composer')):
            run('. install_composer.sh')
        run('SYMFONY_ENV=prod php composer install --no-dev')


@task
def cache():
    """
    Delete the Symfony cache.
    """
    with cd(env.appdir):
        sudo('chgrp -R www-data var/cache var/logs var/sessions')
        sudo('chmod -R g+rwX var/cache var/logs var/sessions')
        sudo('rm -rf var/cache/prod var/cache/dev var/cache/test')
        sudo('bin/console cache:clear --env=prod', user='www-data')


def install_packages(names):
    sudo('apt-get install -y --no-install-recommends {}'.format(names))
