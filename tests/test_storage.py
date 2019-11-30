###############################################################
# pytest -v --capture=no tests/test_storage.py
# pytest -v  tests/test_storage.py
# pytest -v --capture=no tests/test_storage.py::TestStorage::<METHIDNAME>
###############################################################
import os
import shutil
from pathlib import Path
from pprint import pprint

import pytest
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile
from cloudmesh.common.variables import Variables
from cloudmesh.common3.Benchmark import Benchmark
#from cloudmesh_installer.install.util import util
from cloudmesh.storage.Provider import Provider
from cloudmesh.storage.provider.awss3.Provider import Provider as awsprovider
#from cloudmesh.configuration.Config import Config
cloud = 'AWS'

@pytest.mark.incremental
class TestStorage(object):

    #def __init__(self, service=None, config="~/.cloudmesh/cloudmesh.yaml"):
        #pprint(service)
    #    super().__init__(service=service, config=config)



    def create_file(self, location, content):
        d = Path(os.path.dirname(path_expand(location)))
        print()
        print("TESTDIR:", d)

        d.mkdir(parents=True, exist_ok=True)

        writefile(path_expand(location), content)

    def setup(self):
        variables = Variables()
        service = Parameter.expand(variables['storage'])[0]

        self.p = Provider(service=service)
        # Please modify the specific provider for running the pytest
        self.aws = awsprovider(service=service)

    def test_create_source(self):
        util.banner()
        StopWatch.start("create source")
        self.sourcedir = path_expand("~/.cloudmesh/storage/test/")
        self.create_file("~/.cloudmesh/storage/test/a/a.txt", "content of a")
        self.create_file("~/.cloudmesh/storage/test/a/b/b.txt", "content of b")
        self.create_file("~/.cloudmesh/storage/test/a/b/c/c.txt",
                         "content of c")
        StopWatch.stop("create source")

        # test if the files are ok
        assert True



    def test_put(self):
        HEADING()

        #root="~/.cloudmesh"
        #src = "storage/test/a/a.txt"

        #src = f"local:{src}"
        #dst = f"aws:{src}"
        # test_file = self.p.put(src, dst)

        #src = "storage_a:test/a/a.txt"


        src = "~/.cloudmesh/storage/test/"
        dst = '/'
        StopWatch.start("put")
        test_file = self.p.put(src, dst)
        StopWatch.stop("put")

        pprint(test_file)

        assert test_file is not None

    def test_put_recursive(self):
        HEADING()

        #root="~/.cloudmesh"
        #src = "storage/test/a/a.txt"

        # source = f"local:{src}"
        # destination = f"aws:{src}"
        # test_file = self.p.put(src, dst)

        #src = "storage_a:test/a/a.txt"


        src = "~/.cloudmesh/storage/test/"
        dst = '/'
        StopWatch.start("put")
        test_file = self.p.put(src, dst,True)
        StopWatch.stop("put")

        pprint(test_file)

        assert test_file is not None

    def test_get(self):
        HEADING()
        src = "/a.txt"
        dst = "~/.cloudmesh/storage/test"
        StopWatch.start("get")
        file = self.p.get(src, dst)
        StopWatch.stop("get")
        pprint(file)

        assert file is not None

    def test_list(self):
        HEADING()
        src = '/'
        StopWatch.start("list")
        contents = self.p.list(src)
        StopWatch.stop("list")
        for c in contents:
            pprint(c)

        assert len(contents) > 0

    def test_list_dir_only(self):
        HEADING()
        src = '/'
        dir = "a"
        StopWatch.start("list")
        contents = self.p.list(src,dir,True)
        StopWatch.stop("list")
        for c in contents:
            pprint(c)

        assert len(contents) > 0

    def test_search(self):
        HEADING()
        src = '/'
        filename = "a.txt"
        StopWatch.start("search")
        search_files = self.p.search(src, filename, True)
        StopWatch.stop("search")
        pprint(search_files)
        assert len(search_files) > 0
        #assert filename in search_files[0]['cm']["name"]

    def test_create_dir(self):
        HEADING()
        src = 'created_dir'
        StopWatch.start("create dir")
        directory = self.p.create_dir(src)
        StopWatch.stop("create dir")

        pprint(directory)

        assert directory is not None

    def test_delete(self):
        HEADING()
        src = '/created_dir'
        StopWatch.start("delete")
        self.p.delete(src)
        StopWatch.stop("delete")

    # this pytest is specifically for AWS,AZURE and Google only
    def test_create_bucket(self):
        HEADING()
        src = 'cloudmeshtest2'
        StopWatch.start("create bucket")
        bucket = self.aws.bucket_create(src)
        StopWatch.stop("create bucket")

        pprint(bucket)

        assert bucket is not None

    def test_benchmark(self):
        Benchmark.print(sysinfo=False, csv=True, tag=cloud)
