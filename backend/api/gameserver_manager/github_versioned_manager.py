from abc import ABC

from api.gameserver_manager.base_manager import AbstractGameServerManager
from os import getcwd
from pathlib import Path
from subprocess import run, PIPE
from os import path

REPOS_DIR: str = 'repos'


class GitHubVersionedManager(AbstractGameServerManager, ABC):

    version_commit_map: dict[str, str] = None  # TODO Kevin: This smells bad, we shouldn't have 2 places of truth.
    repo: str = None

    def __init_subclass__(cls) -> None:
        """ GitHubVersionedManager.__init_subclass__()
            ensures that subclasses specify required class attributes and inherit in the correct order """

        super().__init_subclass__()

        assert cls.version_commit_map is not None, \
            f"Subclassed GitHubSourcedManager {cls} must specify a version_commit_map"
        assert cls.repo is not None, \
            f"Subclassed GitHubSourcedManager {cls} must specify a repo"

        # Only non-abstract classes should be registered to the manager dictionary.
        # They may be better ways to check if the subclass is still abstract.
        #   What if the user doesn't know to subclass ABC ?
        #   inspect.isabstract() doesn't appear to work for AbstractDockerComposeGameServer sadly
        if ABC in cls.__bases__:
            return

        assert not (unknown_commit_versions := set(cls.game_versions).difference(set(cls.version_commit_map.keys()))), \
            f"No commit has been specified for the following version(s) {unknown_commit_versions}"
        assert next(basecls for basecls in cls.mro() if ABC in basecls.__bases__) is GitHubVersionedManager, \
            'GitHubVersionedManager must be subclassed before other base GameServerManagers (when using multiple inheretance)'

    def _get_repo_dir(self) -> str:
        repo_dir_name: str = path.split(self.repo)[-1].removesuffix('.git')  # Get the name (not path) of the repo dir
        return path.join(REPOS_DIR, repo_dir_name)

    def checkout(self, commit: str):
        run(['git', '-C', REPOS_DIR, 'clone', self.repo])  # We expect this to fail when the commit already exists
        # TODO Kevin: We should check if the repo is clean here
        run(['git', '-C', self._get_repo_dir(), 'checkout', commit])

    def set_version(self, version: str):
        try:
            commit: str = self.version_commit_map[version]
        except KeyError as e:
            raise KeyError(f"Commit not found for version {version}, available versions are {self.version_commit_map}") from e
        self.checkout(commit)

    def get_version(self) -> str:
        # TODO Kevin: What if the repo dir doesn't exist yet?
        cur_sha: str = run(['git', '-C', self._get_repo_dir(), 'rev-parse', 'HEAD'], stdout=PIPE).stdout.decode().strip('\n')
        try:
            return next(version for version, version_sha in self.version_commit_map.items() if version_sha == cur_sha)
        except StopIteration:
            assert False, 'Server repo is somehow using a commit we have no knowledge of'
