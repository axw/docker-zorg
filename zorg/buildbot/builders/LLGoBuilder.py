import os

import buildbot
import buildbot.process.factory
from buildbot.steps.source import SVN, Git
from buildbot.steps.shell import Configure, ShellCommand
from buildbot.process.properties import WithProperties

from zorg.buildbot.builders import LNTBuilder
from zorg.buildbot.builders import ClangBuilder

def getLLGoBuildFactory(
            build_type='Release+Asserts',
            test_libgo=True,             # run 'check-libgo' target if True
    ):
    llvm_srcdir = "llvm.src"
    llvm_objdir = "llvm.obj"
    llgo_srcdir = '%s/tools/llgo' % llvm_srcdir
    clang_srcdir = '%s/tools/clang' % llvm_srcdir

    f = buildbot.process.factory.BuildFactory()
    # Determine the build directory.
    f.addStep(buildbot.steps.shell.SetProperty(name="get_builddir",
                                               command=["pwd"],
                                               property="builddir",
                                               description="set build dir",
                                               workdir="."))
    # Get LLVM, clang and llgo
    f.addStep(SVN(name='svn-llvm',
                  mode='update',
                  baseURL='http://llvm.org/svn/llvm-project/llvm/',
                  defaultBranch='trunk',
                  workdir=llvm_srcdir))
    f.addStep(SVN(name='svn-clang',
                  mode='update',
                  baseURL='http://llvm.org/svn/llvm-project/cfe/',
                  defaultBranch='trunk',
                  workdir=clang_srcdir))
    f.addStep(SVN(name='svn-llgo',
                  mode='update',
                  baseURL='http://llvm.org/svn/llvm-project/llgo/',
                  defaultBranch='trunk',
                  workdir=llgo_srcdir))

    # Create configuration files with cmake
    f.addStep(ShellCommand(name="create-build-dir",
                               command=["mkdir", "-p", llvm_objdir],
                               haltOnFailure=False,
                               description=["create build dir"],
                               workdir="."))
    cmakeCommand = [
        "cmake", "-G", "Ninja",
        "../%s" %llvm_srcdir,
        "-DCMAKE_BUILD_TYPE=" + build_type,
    ]
    f.addStep(ShellCommand(name="cmake-configure",
                               command=cmakeCommand,
                               haltOnFailure=False,
                               description=["cmake configure"],
                               workdir=llvm_objdir))

    # Build llgo
    f.addStep(ShellCommand(name="build_llgo",
                               command=["ninja", "llgo"],
                               haltOnFailure=True,
                               description=["build llgo"],
                               workdir=llvm_objdir))
    # Test llgo
    f.addStep(ShellCommand(name="test_llgo",
                               command=["ninja", "check-llgo"],
                               haltOnFailure=True,
                               description=["test llgo"],
                               workdir=llvm_objdir))
    # Test libgo
    f.addStep(ShellCommand(name="test_libgo",
                               command=["ninja", "check-libgo"],
                               haltOnFailure=True,
                               description=["test libgo"],
                               workdir=llvm_objdir))
    return f

