###############################################################
# pytest -v --capture=no tests/test_storage_azure.py
# pytest -v  tests/test_storage_azure.py
# pytest -v --capture=no tests/test_storage_azure..py::TestAzureStorage::<METHODNAME>
###############################################################
import os
from pathlib import Path
from pprint import pprint

from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile

print("this seems to be the same as in test_05_storage")

print("I sugget to delete all tests that are covered "
      "by 05 and only include tests here that are unique")

print("we exist now to makes usre this gets your attention")

sys.exit()

# cms set storage=parallelaws3


Benchmark.debug()

user = Config()["cloudmesh.profile.user"]
variables = Variables()
VERBOSE(variables.dict())

service = variables.parameter('storage')

print(f"Test run for {service}")

if service is None:
    raise ValueError("storage is not set")

provider = Provider(service=service)
print('provider:', provider, provider.kind)


@pytest.mark.incremental
class TestStorageParallelaws3(object):

    def create_file(self, location, content):
        Shell.mkdir(os.dirname(path_expand(location)))
        writefile(location, content)

    #
    # BUG: Please use location /tmp just like in 03 test
    #
    def test_create_local_source(self):
        HEADING()
        StopWatch.start("create source")
        self.sourcedir = path_expand("~/.cloudmesh/storage/test/")
        self.create_local_file("~/.cloudmesh/storage/test/a/a.txt",
                               "content of a")
        self.create_local_file("~/.cloudmesh/storage/test/a/b/b.txt",
                               "content of b")
        self.create_local_file("~/.cloudmesh/storage/test/a/b/c/c.txt",
                               "content of c")
        StopWatch.stop("create source")

        # test if the files are ok
        assert True

    def test_put(self):
        HEADING()

        # root="~/.cloudmesh"
        # src = "storage/test/a/a.txt"

        # src = f"local:{src}"
        # dst = f"aws:{src}"
        # test_file = self.p.put(src, dst)

        # src = "storage_a:test/a/a.txt"

        src = "~/.cloudmesh/storage/test/"
        dst = '/'
        StopWatch.start("put")
        test_file = provider.put(src, dst)
        StopWatch.stop("put")

        pprint(test_file)

        assert test_file is not None

    def test_put_recursive(self):
        HEADING()

        # root="~/.cloudmesh"
        # src = "storage/test/a/a.txt"

        # source = f"local:{src}"
        # destination = f"aws:{src}"
        # test_file = self.p.put(src, dst)

        # src = "storage_a:test/a/a.txt"

        src = "~/.cloudmesh/storage/test/"
        dst = '/'
        StopWatch.start("put")
        test_file = provider.put(src, dst, True)
        StopWatch.stop("put")

        pprint(test_file)

        assert test_file is not None

    def test_get(self):
        HEADING()
        src = "/a.txt"
        dst = "~/.cloudmesh/storage/test"
        StopWatch.start("get")
        file = provider.get(src, dst)
        StopWatch.stop("get")
        pprint(file)

        assert file is not None

    def test_list(self):
        HEADING()
        src = '/'
        StopWatch.start("list")
        contents = provider.list(src)
        StopWatch.stop("list")
        for c in contents:
            pprint(c)

        assert len(contents) > 0

    def test_list_dir_only(self):
        HEADING()
        src = '/'
        dir = "a"
        StopWatch.start("list")
        contents = provider.list(src, dir, True)
        StopWatch.stop("list")
        for c in contents:
            pprint(c)

        assert len(contents) > 0

    def test_search(self):
        HEADING()
        src = '/'
        filename = "a.txt"
        StopWatch.start("search")
        search_files = provider.search(src, filename, True)
        StopWatch.stop("search")
        pprint(search_files)
        assert len(search_files) > 0
        # assert filename in search_files[0]['cm']["name"]

    def test_create_dir(self):
        HEADING()
        src = 'created_dir'
        StopWatch.start("create dir")
        directory = provider.create_dir(src)
        StopWatch.stop("create dir")

        pprint(directory)

        assert directory is not None

    def test_delete(self):
        HEADING()
        src = '/created_dir'
        StopWatch.start("delete")
        provider.delete(src)
        StopWatch.stop("delete")

    def test_benchmark(self):
        Benchmark.print(sysinfo=False, csv=True, tag=service)
