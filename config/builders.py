from zorg.buildbot.builders import ClangBuilder
reload(ClangBuilder)
from zorg.buildbot.builders import ClangBuilder

from zorg.buildbot.builders import LLVMBuilder
reload(LLVMBuilder)
from zorg.buildbot.builders import LLVMBuilder

from zorg.buildbot.builders import LLGoBuilder
reload(LLGoBuilder)
from zorg.buildbot.builders import LLGoBuilder

# Plain LLVM builders.
def _get_llvm_builders():
    return [
        {'name': "llvm-x86_64-ubuntu",
         'slavenames':["local-slave"],
         'builddir':"llvm-x86_64-ubuntu",
         'factory': LLVMBuilder.getLLVMBuildFactory("x86_64-pc-linux-gnu", jobs=4, timeout=30)},
        ]

# Clang builders.
def _get_clang_builders():
    return [
        {'name': "clang-x86_64-ubuntu",
         'slavenames':["local-slave"],
         'builddir':"clang-x86_64-ubuntu",
         'factory' : ClangBuilder.getClangBuildFactory(extra_configure_args=['--enable-shared'])},
        ]

# LLGo builders.
def _get_llgo_builders():
    return [
        {'name': "llgo-x86_64-ubuntu",
         'slavenames' :["local-slave"],
         'builddir':"llgo-x86_64-ubuntu",
         'factory': LLGoBuilder.getLLGoBuildFactory(),
         'category'   : 'llgo'},
    ]

def get_builders():
    for b in _get_llvm_builders():
        b['category'] = 'llvm'
        yield b

    for b in _get_clang_builders():
        b['category'] = 'clang'
        yield b

    for b in _get_llgo_builders():
        b['category'] = 'llgo'
        yield b

