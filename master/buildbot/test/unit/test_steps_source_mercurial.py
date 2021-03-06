# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from twisted.trial import unittest
from buildbot.steps.source import mercurial
from buildbot.status.results import SUCCESS
from buildbot.test.util import sourcesteps
from buildbot.test.fake.remotecommand import ExpectShell, ExpectLogged

class TestMercurial(sourcesteps.SourceStepMixin, unittest.TestCase):

    def setUp(self):
        return self.setUpSourceStep()

    def tearDown(self):
        return self.tearDownSourceStep()

    def test_repourl_and_baseURL(self):
        self.assertRaises(ValueError, lambda :
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    baseURL="http://hg.mozilla.org"))

    def test_neither_repourl_nor_baseURL(self):
        self.assertRaises(ValueError, lambda :
                mercurial.Mercurial(mode="full"))

    def test_mode_full_clean(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='full', method='clean', branchType='inrepo'))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', '--config',
                                 'extensions.purge=', 'purge'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'pull',
                                 'http://hg.mozilla.org'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify', '--branch'])
            + ExpectShell.log('stdio',
                stdout='default')
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update',
                                 '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
        )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_full_clean_no_existing_repo(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='full', method='clean', branchType='inrepo'))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 1,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'clone',
                                    'http://hg.mozilla.org', '.'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
        )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_full_clobber(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='full', method='clobber', branchType='inrepo'))
        self.expectCommands(
            ExpectLogged('rmdir', dict(dir='wkdir'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'clone', '--noupdate',
                                    'http://hg.mozilla.org', '.'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update',
                                 '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
        )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_full_fresh(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='full', method='fresh', branchType='inrepo'))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', '--config',
                                 'extensions.purge=', 'purge', '--all'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'pull',
                                 'http://hg.mozilla.org'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify', '--branch'])
            + ExpectShell.log('stdio',
                stdout='default')
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update',
                                 '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
        )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_full_fresh_no_existing_repo(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='full', method='fresh', branchType='inrepo'))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 1,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'clone',
                                    'http://hg.mozilla.org', '.'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
        )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_incremental_no_existing_repo_dirname(self):
        self.setupStep(
                mercurial.Mercurial(baseURL='http://hg.mozilla.org',
                                    mode='incremental', branchType='dirname'),
            )
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 1, # does not exist
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'clone',
                                 'http://hg.mozilla.org', '.', '--noupdate'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update', '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio', 
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
            )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()


    def test_mode_incremental_branch_change_dirname(self):
        self.setupStep(
                mercurial.Mercurial(baseURL='http://hg.mozilla.org/',
                                    mode='incremental', branchType='dirname', defaultBranch='devel'),
            dict(branch='stable')
            )
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'pull',
                                 'http://hg.mozilla.org/stable', '--update'])
            + 0,
            ExpectLogged('rmdir', dict(dir='wkdir'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'clone', '--noupdate',
                                    'http://hg.mozilla.org/stable', '.'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update',
                                 '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio', 
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
            )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_incremental_no_existing_repo_inrepo(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='incremental', branchType='inrepo'))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 1, # does not exist
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'clone',
                                 'http://hg.mozilla.org', '.', '--noupdate'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify', '--branch'])
            + ExpectShell.log('stdio', stdout='default')
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update', '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
            )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_incremental_existing_repo(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='incremental', branchType='inrepo'))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 0, # directory exists
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'pull',
                                 'http://hg.mozilla.org', '--update'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify', '--branch'])
            + ExpectShell.log('stdio', stdout='default')
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update', '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
            )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_incremental_given_revision(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='incremental', branchType='inrepo'), dict(
                revision='abcdef01',
                ))

        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'pull',
                                 'http://hg.mozilla.org', '--update'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify', '--branch'])
            + ExpectShell.log('stdio', stdout='default')
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update', '--clean',
                                 '--rev', 'abcdef01'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
            )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_incremental_branch_change(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='incremental', branchType='inrepo'), dict(
                branch='stable',
                ))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'pull',
                                 'http://hg.mozilla.org', '--update'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify', '--branch'])
            + ExpectShell.log('stdio', stdout='default')
            + 0,
            ExpectLogged('rmdir', dict(dir='wkdir'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'clone', '--noupdate',
                                    'http://hg.mozilla.org', '.'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update',
                                 '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
            )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()

    def test_mode_incremental_branch_change_no_clobberOnBranchChange(self):
        self.setupStep(
                mercurial.Mercurial(repourl='http://hg.mozilla.org',
                                    mode='incremental', branchType='inrepo',
                                    clobberOnBranchChange=False), dict(
                branch='stable',
                ))
        self.expectCommands(
            ExpectLogged('stat', dict(file='wkdir/.hg'))
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'pull',
                                 'http://hg.mozilla.org', '--update'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify', '--branch'])
            + ExpectShell.log('stdio', stdout='default')
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'update',
                                 '--clean'])
            + 0,
            ExpectShell(workdir='wkdir',
                        command=['hg', '--verbose', 'identify',
                                    '--id', '--debug'])
            + ExpectShell.log('stdio', stdout='\n')
            + ExpectShell.log('stdio',
                stdout='f6ad368298bd941e934a41f3babc827b2aa95a1d')
            + 0,
            )
        self.expectOutcome(result=SUCCESS, status_text=["update"])
        return self.runStep()
