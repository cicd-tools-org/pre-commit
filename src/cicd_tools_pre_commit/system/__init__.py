"""Interface CICD-Tools with the underlying system."""

from __future__ import annotations

from .call import CALL_ERROR as CALL_ERROR
from .call import call as call
from .fs import rmtree as rmtree
from .git import git_ls_untracked as git_ls_untracked
